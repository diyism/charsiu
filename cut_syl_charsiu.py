#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Realtime-ish Mandarin syllable cutting with Charsiu.

This script records from a PulseAudio/PipeWire source with `parec`, runs the
Charsiu predictive Mandarin aligner on a sliding audio window, then merges
predicted Mandarin initials and finals into rough syllable intervals.
"""

import argparse
import collections
import re
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


SR = 16000
INITIALS = {
    "b", "p", "m", "f", "d", "t", "n", "l", "g", "k", "h", "j", "q", "x",
    "zh", "ch", "sh", "r", "z", "c", "s",
}
SILENCE = {"[SIL]", "[PAD]", "[UNK]", "|", ""}


@dataclass
class Source:
    index: str
    name: str
    driver: str
    spec: str
    state: str


class AudioBuffer:
    def __init__(self, max_samples):
        self.samples = collections.deque(maxlen=max_samples)
        self.total_samples = 0
        self.lock = threading.Lock()

    def append_pcm16(self, chunk):
        data = np.frombuffer(chunk, dtype=np.int16).astype(np.float32) / 32768.0
        if data.size == 0:
            return
        with self.lock:
            self.samples.extend(data.tolist())
            self.total_samples += int(data.size)

    def snapshot(self):
        with self.lock:
            audio = np.asarray(self.samples, dtype=np.float32)
            total = self.total_samples
        start_sample = max(0, total - audio.size)
        return audio, start_sample, total


def run_text(cmd):
    return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)


def list_sources(include_monitors=False):
    try:
        output = run_text(["pactl", "list", "short", "sources"])
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise SystemExit("Could not run `pactl list short sources`: %s" % exc)

    sources = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) < 5:
            continue
        source = Source(
            index=parts[0],
            name=parts[1],
            driver=parts[2],
            spec=" ".join(parts[3:-1]),
            state=parts[-1],
        )
        if include_monitors or not source.name.endswith(".monitor"):
            sources.append(source)
    return sources


def choose_source(args):
    if args.source:
        return Source(
            index=args.source,
            name=args.source,
            driver="manual",
            spec="manual",
            state="unknown",
        )

    sources = list_sources(include_monitors=args.include_monitors)
    if not sources:
        raise SystemExit("No input sources found. Try --include-monitors if you want monitor devices.")

    print("Available microphone sources:")
    for i, source in enumerate(sources, 1):
        print("  %d. %s  [%s, %s, %s]" % (i, source.name, source.index, source.spec, source.state))

    while True:
        raw = input("Select microphone [1]: ").strip() or "1"
        if raw.isdigit() and 1 <= int(raw) <= len(sources):
            return sources[int(raw) - 1]
        print("Please enter a number from 1 to %d." % len(sources))


def start_parec(source_name):
    cmd = [
        "parec",
        "--device=%s" % source_name,
        "--rate=%d" % SR,
        "--channels=1",
        "--format=s16le",
        "--raw",
    ]
    try:
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError as exc:
        raise SystemExit("Could not run `parec`: %s" % exc)


def reader_thread(proc, audio_buffer, chunk_bytes, stop_event):
    while not stop_event.is_set():
        chunk = proc.stdout.read(chunk_bytes)
        if not chunk:
            break
        audio_buffer.append_pcm16(chunk)


def clean_phone(phone):
    if phone is None:
        return ""
    return str(phone).strip()


def is_silence(phone):
    phone = clean_phone(phone)
    return phone in SILENCE or phone.startswith("[")


def is_initial(phone):
    return clean_phone(phone) in INITIALS


def is_final(phone):
    phone = clean_phone(phone)
    return bool(re.search(r"\d$", phone)) or (phone and not is_initial(phone) and not is_silence(phone))


def phones_to_syllables(phone_intervals):
    syllables = []
    pending_initial = None

    for start, end, raw_phone in phone_intervals:
        phone = clean_phone(raw_phone)
        if is_silence(phone):
            pending_initial = None
            continue

        if is_initial(phone):
            if pending_initial is not None:
                ps, pe, pp = pending_initial
                syllables.append((ps, pe, pp))
            pending_initial = (float(start), float(end), phone)
            continue

        if is_final(phone):
            if pending_initial is not None:
                ps, _pe, pp = pending_initial
                syllables.append((ps, float(end), pp + phone))
                pending_initial = None
            else:
                syllables.append((float(start), float(end), phone))

    if pending_initial is not None:
        syllables.append(pending_initial)

    return syllables


def format_syllable(start, end, label, lag):
    return "%8.2f  %8.2f  %-12s lag=%5.2fs" % (start, end, label, lag)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Use Charsiu to test realtime Mandarin syllable cutting from a microphone."
    )
    parser.add_argument("--source", help="PulseAudio/PipeWire source index or name. If omitted, prompt.")
    parser.add_argument("--include-monitors", action="store_true", help="Also show *.monitor loopback sources.")
    parser.add_argument("--aligner", default="charsiu/zh_xlsr_fc_10ms", help="Charsiu/HuggingFace aligner id.")
    parser.add_argument("--device", default=None, help="torch device, e.g. cuda or cpu. Default: auto.")
    parser.add_argument("--window", type=float, default=1.50, help="Sliding analysis window in seconds.")
    parser.add_argument("--hop", type=float, default=0.05, help="Sliding hop in seconds. Default matches 50 ms.")
    parser.add_argument("--right-context", type=float, default=0.25, help="Delay before emitting a syllable.")
    parser.add_argument("--min-audio", type=float, default=0.50, help="Seconds to collect before first inference.")
    parser.add_argument("--print-phones", action="store_true", help="Print raw Charsiu phone intervals too.")
    return parser.parse_args()


def main():
    args = parse_args()
    source = choose_source(args)

    max_samples = int(max(args.window, args.min_audio) * SR)
    hop_samples = max(1, int(args.hop * SR))
    chunk_bytes = hop_samples * 2
    audio_buffer = AudioBuffer(max_samples=max_samples)
    stop_event = threading.Event()

    print("Loading Charsiu model: %s" % args.aligner)
    try:
        from Charsiu import charsiu_predictive_aligner
    except ModuleNotFoundError as exc:
        missing = exc.name or str(exc)
        raise SystemExit(
            "Missing Python dependency `%s`. Install the Charsiu runtime dependencies "
            "in this Python environment before running realtime cutting." % missing
        )
    charsiu = charsiu_predictive_aligner(aligner=args.aligner, lang="zh", device=args.device)

    print("Recording from: %s" % source.name)
    print("window=%.2fs hop=%.2fs right_context=%.2fs sr=%d" % (args.window, args.hop, args.right_context, SR))
    print("Press Ctrl-C to stop.")

    proc = start_parec(source.name)
    thread = threading.Thread(
        target=reader_thread,
        args=(proc, audio_buffer, chunk_bytes, stop_event),
        daemon=True,
    )
    thread.start()

    last_emit_end = 0.0
    next_tick = time.monotonic() + args.hop

    try:
        while True:
            sleep_for = next_tick - time.monotonic()
            if sleep_for > 0:
                time.sleep(sleep_for)
            next_tick += args.hop

            audio, start_sample, total_sample = audio_buffer.snapshot()
            if audio.size < int(args.min_audio * SR):
                continue

            window_start = start_sample / SR
            stream_time = total_sample / SR

            try:
                phones = charsiu.align(audio=audio)
            except Exception as exc:
                print("align failed: %s" % exc, file=sys.stderr)
                time.sleep(0.5)
                continue

            if args.print_phones:
                phone_line = " ".join("%s:%.2f-%.2f" % (p, window_start + s, window_start + e) for s, e, p in phones)
                print("phones:", phone_line)

            syllables = phones_to_syllables(phones)
            emit_before = stream_time - args.right_context

            for start, end, label in syllables:
                abs_start = window_start + start
                abs_end = window_start + end
                if abs_end <= emit_before and abs_end > last_emit_end + 0.015:
                    print(format_syllable(abs_start, abs_end, label, stream_time - abs_end), flush=True)
                    last_emit_end = abs_end

    except KeyboardInterrupt:
        print("\nStopping.")
    finally:
        stop_event.set()
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
