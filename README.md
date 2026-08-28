    $ ./cut_syl_charsiu.py --aligner charsiu/zh_w2v2_tiny_fc_10ms
    Available microphone sources:
      1. Audio  [32, Sink.monitor PipeWire float32le 2ch 48000Hz, RUNNING]
      2. Dummy  [33, PipeWire float32le 2ch 48000Hz, SUSPENDED]
      3. android-e3b0c44  [16975, s16le 1ch 44100Hz, SUSPENDED]
      4. alsa_input.usb-Generic_USB2.0_Device_20220701093623-00.mono-fallback  [18666, s16le 1ch 48000Hz, SUSPENDED]
      5. bluez_input.84:AC:60:12:C9:0E  [39781, float32le 1ch 48000Hz, SUSPENDED]
    Select microphone [1]: 4
    Loading Charsiu model: charsiu/zh_w2v2_tiny_fc_10ms
    Recording from: alsa_input.usb-Generic_USB2.0_Device_20220701093623-00.mono-fallback
    window=1.50s hop=0.05s right_context=0.25s sr=16000
    Press Ctrl-C to stop.
        0.63      0.66  l            lag= 1.34s
        0.66      0.85  mou2         lag= 1.15s
        0.85      1.15  tai4         lag= 0.85s
        1.33      1.47  mao2         lag= 0.53s
        1.47      1.49  ao1          lag= 0.51s
        1.49      1.51  ao2          lag= 0.49s
        1.51      1.54  ou2          lag= 0.46s
        2.56      2.68  me5          lag= 1.32s
        2.68      2.71  o2           lag= 1.29s
        2.72      2.83  ta1          lag= 1.17s
        2.83      2.93  ai4          lag= 1.07s
        2.93      3.16  mao4         lag= 0.84s
        3.16      3.46  tai4         lag= 0.54s
        4.50      4.53  ai2          lag= 1.47s
        4.54      4.61  ai2          lag= 1.39s
        4.63      4.64  j            lag= 1.36s
        4.64      4.66  p            lag= 1.34s
        4.66      4.68  t            lag= 1.32s
        4.68      4.70  j            lag= 1.30s

    $ ./cut_syl_charsiu.py \
      --aligner charsiu/zh_xlsr_fc_10ms \
      --source alsa_input.usb-Generic_USB2.0_Device_20220701093623-00.mono-fallback \
      --window 0.75 \
      --hop 0.05 \
      --infer-interval 0.05 \
      --right-context 0.12 \
      --latency-msec 30 \
      --process-time-msec 10 \
      --profile
    Loading Charsiu model: charsiu/zh_xlsr_fc_10ms
    Recording from: alsa_input.usb-Generic_USB2.0_Device_20220701093623-00.mono-fallback
    window=0.75s hop=0.05s infer_interval=0.05s right_context=0.12s latency=30ms process_time=10ms sr=16000
    Press Ctrl-C to stop.
    # infer= 236.0ms window=0.45s realtime_x=0.52 stream=0.45s
    # infer= 278.7ms window=0.70s realtime_x=0.40 stream=0.70s
    # infer= 354.2ms window=0.75s realtime_x=0.47 stream=1.05s
    # infer= 293.6ms window=0.75s realtime_x=0.39 stream=1.45s
    # infer= 313.9ms window=0.75s realtime_x=0.42 stream=1.80s
    # infer= 285.3ms window=0.75s realtime_x=0.38 stream=2.15s
        1.81      1.91  uo3          lag= 0.24s
    # infer= 285.9ms window=0.75s realtime_x=0.38 stream=2.45s
    # infer= 489.4ms window=0.75s realtime_x=0.65 stream=2.85s
        2.31      2.43  da1          lag= 0.42s
        2.43      2.58  da2          lag= 0.27s
        2.58      2.72  da3          lag= 0.13s
    # infer= 382.3ms window=0.75s realtime_x=0.51 stream=3.35s
        2.72      3.00  da4          lag= 0.35s
    # infer= 397.9ms window=0.75s realtime_x=0.53 stream=3.80s
    # infer= 287.6ms window=0.75s realtime_x=0.38 stream=4.25s
    # infer= 349.9ms window=0.75s realtime_x=0.47 stream=4.60s
        4.07      4.20  ga1          lag= 0.40s
        4.20      4.34  da2          lag= 0.26s
    # infer= 375.9ms window=0.75s realtime_x=0.50 stream=5.00s
        4.35      4.49  da3          lag= 0.51s
        4.49      4.78  ga4          lag= 0.22s


## Charsiu: A transformer-based phonetic aligner [[arXiv]](https://arxiv.org/abs/2110.03876)

### Updates
- 2.10.2022. We release phone- and word-level alignments for 860k utterances from the English subset of Common Voice. Check out [this link](misc/data.md#alignments-for-english-datasets).  
- 1.31.2022. We release phone- and word-level alignments for over a million Mandarin utterances. Check out [this link](misc/data.md#alignments-for-mandarin-speech-datasets).  
- 1.26.2022. Word alignment functionality has been added to `charsiu_forced_aligner` .

### Intro
**Charsiu** is a phonetic alignment tool, which can:
- recognise phonemes in a given audio file
- perform forced alignment using phone transcriptions created in the previous step or provided by the user.
- directly predict the phone-to-audio alignment from audio (text-independent alignment)  

The aligner is under active development. New functions, new languages and detailed documentation will be added soon! Give us a star if you like our project!  
**Fun fact**: Char Siu is one of the most representative dishes of Cantonese cuisine 🍲 (see [wiki](https://en.wikipedia.org/wiki/Char_siu)). 



### Table of content
- [Tutorial](README.md#Tutorial)  
- [Usage](README.md#Usage)  
- [Pretrained models](README.md#Pretrained-models)
- [Development plan](README.md#Development-plan)  
- [Dependencies](README.md#Dependencies)  
- [Training](README.md#Training)  
- [Attribution and Citation](README.md#attribution-and-citation)  
- [References](README.md#References)  
- [Disclaimer](README.md#Disclaimer)  
- [Support or Contact](README.md#support-or-contact)




### Tutorial 
**[!NEW]** A step-by-step tutorial for linguists: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lingjzhu/charsiu/blob/development/charsiu_tutorial.ipynb)

You can directly run our model in the cloud via Google Colab!  
 - Forced alignment:   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lingjzhu/charsiu/blob/development/charsiu_forced_alignment_demo.ipynb)  
 - Textless alignment: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lingjzhu/charsiu/blob/development/charsiu_textless_demo.ipynb)  

### Usage
```
git clone  https://github.com/lingjzhu/charsiu
cd charsiu
```
#### Forced alignment
```Python
from Charsiu import charsiu_forced_aligner
# if there are errors importing, uncomment the following lines and add path to charsiu
# import sys
# sys.path.append('path_to_charsiu/src')

# initialize model
charsiu = charsiu_forced_aligner(aligner='charsiu/en_w2v2_fc_10ms')
# perform forced alignment
alignment = charsiu.align(audio='./local/SA1.WAV',
                          text='She had your dark suit in greasy wash water all year.')
# perform forced alignment and save the output as a textgrid file
charsiu.serve(audio='./local/SA1.WAV',
              text='She had your dark suit in greasy wash water all year.',
              save_to='./local/SA1.TextGrid')


# Chinese
charsiu = charsiu_forced_aligner(aligner='charsiu/zh_w2v2_tiny_fc_10ms',lang='zh')
charsiu.align(audio='./local/SSB00050015_16k.wav',text='经广州日报报道后成为了社会热点。')
charsiu.serve(audio='./local/SSB00050015_16k.wav', text='经广州日报报道后成为了社会热点。',
              save_to='./local/SSB00050015.TextGrid')
              
# An numpy array of speech signal can also be passed to the model.
import soundfile as sf
y, sr = sf.read('./local/SSB00050015_16k.wav')
charsiu.align(audio=y,text='经广州日报报道后成为了社会热点。')
```


#### Textless alignment
```Python
from Charsiu import charsiu_predictive_aligner
# English
# initialize a model
charsiu = charsiu_predictive_aligner(aligner='charsiu/en_w2v2_fc_10ms')
# perform textless alignment
alignment = charsiu.align(audio='./local/SA1.WAV')
# Or
# perform textless alignment and output the results to a textgrid file
charsiu.serve(audio='./local/SA1.WAV', save_to='./local/SA1.TextGrid')


# Chinese
charsiu = charsiu_predictive_aligner(aligner='charsiu/zh_xlsr_fc_10ms',lang='zh')

charsiu.align(audio='./local/SSB16240001_16k.wav')
# Or
charsiu.serve(audio='./local/SSB16240001_16k.wav', save_to='./local/SSB16240001.TextGrid')
```

### Pretrained models  
Pretrained models are available at the 🤗 *HuggingFace* model hub: https://huggingface.co/charsiu.


### Development plan

 - Package  

|     Items          | Progress |
|:------------------:|:--------:|
|  Documentation     | Nov 2021 |    
|  Textgrid support  |     √    |
| Word Segmentation  |     √    |
| Model compression  |   TBD    |
|  IPA support       |   TBD    |

 - Multilingual support

|      Language      | Progress |
|:------------------:|:--------:|
| English (American) |     √    |
|  Mandarin Chinese  |     √    |
|       German       | TBD |
|       Spanish      | TBD |
|  English (British) |    TBD   |
|    Cantonese       |    TBD   |
|    AAVE            |    TBD   |





### Dependencies
pytorch  
transformers  
datasets  
librosa  
g2pe  
praatio  
g2pM


### Training
The training pipeline is coming soon!

Note.Training code is in `experiments/`. Those were original research code for training the model. They still need to be reorganized. 


### Attribution and Citation
For now, you can cite this tool as:

```
@article{zhu2022charsiu,
  title={Phone-to-audio alignment without text: A Semi-supervised Approach},
  author={Zhu, Jian and Zhang, Cong and Jurgens, David},
  journal={IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  year={2022}
 }
```
Or


To share a direct web link: https://github.com/lingjzhu/charsiu/.

### References
[Transformers](https://huggingface.co/transformers/)  
[s3prl](https://github.com/s3prl/s3prl)  
[Montreal Forced Aligner](https://montreal-forced-aligner.readthedocs.io/en/latest/)


### Disclaimer

This tool is a beta version and is still under active development. It may have bugs and quirks, alongside the difficulties and provisos which are described throughout the documentation. 
This tool is distributed under MIT license. Please see [license](https://github.com/lingjzhu/charsiu/blob/main/LICENSE) for details. 

By using this tool, you acknowledge:

* That you understand that this tool does not produce perfect camera-ready data, and that all results should be hand-checked for sanity's sake, or at the very least, noise should be taken into account.

* That you understand that this tool is a work in progress which may contain bugs.  Future versions will be released, and bug fixes (and additions) will not necessarily be advertised.

* That this tool may break with future updates of the various dependencies, and that the authors are not required to repair the package when that happens.

* That you understand that the authors are not required or necessarily available to fix bugs which are encountered (although you're welcome to submit bug reports to Jian Zhu (lingjzhu@umich.edu), if needed), nor to modify the tool to your needs.

* That you will acknowledge the authors of the tool if you use, modify, fork, or re-use the code in your future work.  

* That rather than re-distributing this tool to other researchers, you will instead advise them to download the latest version from the website.

... and, most importantly:

* That neither the authors, our collaborators, nor the the University of Michigan or any related universities on the whole, are responsible for the results obtained from the proper or improper usage of the tool, and that the tool is provided as-is, as a service to our fellow linguists.

All that said, thanks for using our tool, and we hope it works wonderfully for you!

### Support or Contact
Please contact Jian Zhu ([lingjzhu@umich.edu](lingjzhu@umich.edu)) for technical support.  
Contact Cong Zhang ([cong.zhang@ru.nl](cong.zhang@ru.nl)) if you would like to receive more instructions on how to use the package.



