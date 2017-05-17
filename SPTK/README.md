## Development: How to use the SPTK

### 1.Output raw file using SPTK <br>

````rb
dmp +s data.short | less
````

波形データのダンプ<br>
shor型のraw音声ファイル(一般的なソフトで再生できない)の音声波形の振幅
<br>
![image](https://cloud.githubusercontent.com/assets/17031124/25885680/c37de508-3594-11e7-9768-9b1f3cc13025.png)
<br>
<br>
### 2.Draw raw file with SPTK <br>

````rb
gwave +s data.short | xgr
````

![image](https://cloud.githubusercontent.com/assets/17031124/25886027/b6690fda-3596-11e7-8dfd-ee8563b9d177.png)
<br>
<br>
![image](https://cloud.githubusercontent.com/assets/17031124/25886479/b65911be-3598-11e7-90a7-3e05e5e93e56.png)
<br>
<br>

### 3.Play raw file with SPTK <br>
Pythonライブラリpyaudio使用し、rawファイルを再生するスクリプト<br>
rawファイルのデータを1024byteずつ読み込み音声ストリームに流す<br>
<br>

### 4.Play raw file with SPTK <br>
rawファイルを再生するスクリプトにサンプリング周波数を引数として受け付ける<br>
<br>

### 5.Cut raw file<br>
音声波形の切り出し<br>

````rb
bcut +s -s 1000 -e 11000 < data.short > part.short
````

<br>

![image](https://cloud.githubusercontent.com/assets/17031124/25928438/3e3902d0-3637-11e7-8679-ff7e37b92e51.png)

<br>
1000サンプル目から11000サンプル目を切り出したもの
<br>

![screen shot 2017-05-11 at 10 54 59](https://cloud.githubusercontent.com/assets/17031124/25928451/4c1e5b66-3637-11e7-9183-dcb6ecce2945.png)

<br>

### 5.Cut MP3 file<br>
<br>

### 7.Convert from big endian to little endian 
STPKのswabコマンドでrawファイルをリトルエンディアンに変換する

![image](https://cloud.githubusercontent.com/assets/28590220/25952320/562794ce-369b-11e7-988c-781d18b4ca46.png)

<br>

### 8.Draw pitch file with matplotlib & pitch extraction<br>
pitchの抽出とpitchファイルの描画

````rb
x2x +sf a01.ad | pitch -a 1 -p 80 -s 16 -L 60 -H 240 > a01.pitch
fdrw -y 0 250 -W 1.5 -H 0.4 < a01.pitch | xgr
````

<br>

pitch描画 XWinodws版<br>

![image](https://cloud.githubusercontent.com/assets/28590220/25954039/117e3c56-36a0-11e7-9b0f-8266349de3ce.png)

pitch描画 matplotlib版<br>

![image](https://cloud.githubusercontent.com/assets/28590220/25954455/55a098ba-36a1-11e7-912d-e99abe9a081f.png)

<br>

### 9.FFT<br>
フーリエ変換 256 = FFTのサンプル数 16000Hz = サンプリング周波数

````rb
sin -l 256 -p 10 | fftr -l 256 -A > fft.result
python 9_Plot_FFT.py fft.result 256 16000
````

<br>

![image](https://cloud.githubusercontent.com/assets/17031124/25956712/672f1920-36a7-11e7-806a-fdca6fec0ee1.png)

<br>

### 10.Window -> FFT<br>
窓関数(ハミング窓) -> FFT

````rb
sin -l 256 -p 10 | window -L 256 -w 1 | fftr -l 256 -A > fft.win.result
python 9_Plot_FFT.py fft.win.result 256 16000
````

<br>

![image](https://cloud.githubusercontent.com/assets/17031124/25957484/652cf64a-36a9-11e7-8c71-3eed7ccff733.png)

<br>

### 11.Window -> FFT<br>
sinコマンドではなく、wavデータでFFT生成
あとは10と同じ

````rb
wav2raw combined.wav
x2x +sf combined.raw | bcut +f -s 0 -e 255 | window -l 256 --w 1 | fftr -l 256 -A > result.fft
python 9_Plot_FFT.py result.fft 256 16000
````

<br>

![image](https://cloud.githubusercontent.com/assets/17031124/25975767/4249c300-36eb-11e7-8edf-0e8e8ab9f363.png)

<br>

### 12.Divide frame<br>
音声波形をフレームごとに分割するframeコマンド(SPTK)を使っていくために簡単なデータを作成<br>

simple.shor(0~99のshort型データのバイナリファイル)作成 & dmpして確認<br>

````rb
> dmp +s simple.short
0       0
1       1
2       2
...
97      97
98      98
99      99
````

<br>

````rb
x2x +sf < simple.short | frame -l 10 -p 5 > simple.frame
dmp -l 10+f simple.frame
````

<br>

````rb
6       20
7       21
8       22
9       23
10      24
1       20
2       21
3       22
4       23
5       24
6       25
7       26
8       27
9       28
10      29
````
<br>
波形から任意のフレームを切り出す
-lオプション

````rb
bcut +f -l 10 -s 18 -e 18 < simple.frame | dmp +f
````

<br>

````rb
0       85
1       86
2       87
3       88
4       89
5       90
6       91
7       92
8       93
9       94
````

<br>

### 13.Operate Frame


<br>

 ````rb
 x2x +sf < data.short | fram -l 400 -p 80 | bcut +f -l 400 -s 65 -e 65 | window -l 400 -L 512 | fftr -l 512 -A > data.fft
 ````

<br>

 1. data.shortをshort型 -> float型
 2. フレーム長400サンプル フレーム周期80サンプルで抽出
 3. フレーム長を400サンプル、65フレーム目を抜き出す
 4. 入力のフレーム長を400サンプル、出力フレーム長を512サンプルの窓関数をかける
 5. フレーム長512サンプルでFFTして振幅スペクトル出力

<br>

 ````rb
 python 9_Plot_FFT.py data.fft 512 16000
 ````

 <br>

 ![image](https://cloud.githubusercontent.com/assets/28590220/25985903/0bb4889c-3728-11e7-9791-b190f0d18f89.png)

 <br>

### 13.Convert Spectrum<br>
12.を対数スペクトルに変換

![image](https://cloud.githubusercontent.com/assets/28590220/25986248/f49723fc-3729-11e7-9e2d-8898aa46f019.png)

### 14.Convert Spectrum with SPTK<br>

13.の対数スペクトル変換をspecコマンドで(SPTK)

````rb
x2x +sf < data.short | frame -l 400 -p 80 \
| bcut +f -l 400 -s 65 -e 65 | window -l 400 -L 512 \
| spec -l 512 | glogsp -l 512 -x 8 -p 2 | xgr
````

<br>

![image](https://cloud.githubusercontent.com/assets/17031124/25986607/989fe050-372b-11e7-8d28-cd3070d4e929.png)

<br>

### 15.MFCC<br>
メル周波数ケプストラム係数

````rb
x2x +sf < data.short | frame -l 640 -p 160 | \
mfcc -l 640 -f 16 -m 12 -n 20 -a 0.97 > data.mfc
````

<rb>


````rb
> python 15_mfcc.py data.mfc 12
-11.75	-0.31	-6.73	0.24	4.32	3.89	-1.38	2.27	3.07	8.11	-0.63	-1.65
-12.45	0.51	-5.58	1.54	2.47	1.90	-1.73	2.38	7.31	8.20	-1.47	-2.40
-13.48	1.95	-3.17	4.40	4.20	1.41	-1.68	1.34	5.90	6.95	-0.02	-0.27
-14.92	5.96	-0.64	5.05	3.75	-0.11	-0.73	1.75	2.97	3.35	1.52	-1.77
・・・
````

<br>

## Speech Coding[音声符号化]<br>

### 16.Souce-filter model of speech production<br>
ソース・フィルタモデル

人間の音声 -> 声帯振動 -> 声道 -> 口 -> 言葉<br>
ヴォコーダー -> 音源(声の高さをピッチパラメータ) -> 音声合成フィルタ(メルケプストラム) -> 音声波形<br>

1. Rawデータ準備
- 16000Hz,16bit,monoral,little endhian

2. pitch抽出
- サンプリング周波数 / Hz

![pitch](https://cloud.githubusercontent.com/assets/28590220/26005883/7007daae-3775-11e7-929c-21e29487e687.png)

<br>

3. 音源生成 
- excite: ピッチから音源のブザー音を作成
- sopr: 振幅1000倍
- x2x: float -> signed integer -> Raw file

![image](https://cloud.githubusercontent.com/assets/28590220/26005915/924be6b4-3775-11e7-9f8f-c31e8898d647.png)

<br>

4. メルケプストラムの抽出
- mcep: 音声をframe分割し、windowをかけ、mcepで抽出
- spec: 音声のスペクトルを求める
- mgc2sp: メルケプストラムパラメータをスペクトルに変換する

![image](https://cloud.githubusercontent.com/assets/28590220/26005950/afaa5cd6-3775-11e7-8858-20d0d45e9d6e.png)

<br>

5. 分析・合成
- mlsadf: MLSAフィルタで音声を合成

<br>

### 17.Extraction LPC(Linear Predictive Coding)<br>
16.のメルケプストラムのスペクトルパラメータとは別の前向き線形予測

````rb
x2x +sf < data.raw | frame -l 400 -p 80 | window -l 400 | lpc -l 400 -m 20 > data.lpc
````

<br>

mgc2sp: メルケプストラム係数からスペクトル包絡を求める
spec: LPC係数からスペクトル包絡を求める

````rb
x2x +sf < data.raw | frame -l 400 -p 800 | bcut +f -l 400 -s 65 -e 65 | window -l 400 -L 512 | dmp +f > spec.txt
bcut +f -n 20 -s 65 -e 65 < data.lpc > data.tmp
spec -l 512 -n 20 -p data.tmp | dmp +f > lpc.txt
````

<br>

対数スペクトル

![image](https://cloud.githubusercontent.com/assets/28590220/26024139/bd1aabfa-3806-11e7-9f79-39d4dca13719.png)

<br>

LPCスペクトル包絡

![image](https://cloud.githubusercontent.com/assets/28590220/26024146/f186a394-3806-11e7-809f-c2dcf268e859.png)

<br>

LPC分析合成に振幅調整のためshort型(16bit)にクリッピングしている

````rb
excite -p 80 data.pitch | poledf -m 20 -p 80 data.lpc | clip -y -32000 32000 | x2x +fs > data.lpc.raw
sox -e signed-integer -c 1 -b 16 -r 16000 data.lpc.raw data.lpc.wav
````

<br>

PARCOR分析合成(Partial auto-Correlation:偏自己相関)関数を用いたもの

````r
excite -p 80 data.pitch | ltcdf -m 20 -p 80 data.par | clip -y -32000 32000 | x2x +fs > data.par.raw
sox -e signed-integer -c 1 -b 16 -r 16000 data.par.raw data.par.wav
````

<br>

LSP分析合成(Line Spectrum Pair:線スペクトル対)係数を用い体もの

````rb
lpc2lsp -m 20 -n 256 < data.lpc > data.lsp
````

<br>

````rb
excite -p 80 data.pitch | lspdf -m 20 -p 80 data.lsp | clip -y -32000 32000 | x2x +fs > data.lsp.raw
sox -e signed-integer -c 1 -b 16 -r 16000 data.lsp.raw data.lsp.wav
````

<br>

LPC(フィルタ係数が誤りに弱く転送が不適当)<br>
-> PARCOR係数(低次元のパラメータの感度が良い)<br>
-> LSP(安定し、パラメータの感度も良く、補完特性も優れるため滑らか)<br>

<br>

### 18.Mel-Generalized Cepstrum:MGC<br>

<br>

#### メル一般化ケプストラムの抽出

他のものと異なり2つのパラメータを追加する

````rb
x2x +sf < data.raw | frame -l 400 -p 80 | window -l 400 -L 512 | mgcep -m 20 -a 0.42 -g -0.5 -l 512 > data.mgcep
````

<br>

````rb
x2x +sf < data.raw | frame -l 400 -p 80 | bcut +f -l 400 -s 65 -e 65 | window -l 400 -L 512 | spec -l 512 | dmp +f > spec.txt
bcut +f -n 20 -s 65 -e 65 < data.mgcep | mgc2sp -m 20 -a 0.42 -g -0.5 -l 512 | dmp +f > mgcep.txt
````

![image](https://cloud.githubusercontent.com/assets/28590220/26024473/d244f6c4-380c-11e7-94b0-e236854b59a6.png)

<br>

#### メル一般化ケプストラム分析合成

````rb
excite -p 80 data.pitch| mglsadf -m 20 -a 0.42 -c 2 -p 80 data.mgcep | clip -y -32000 32000 | x2x +fs > data.mgcep.raw
````

<br>

分析の関係性<br>

![image](https://cloud.githubusercontent.com/assets/28590220/26024492/27813ed6-380d-11e7-902b-7937818252fc.png)

<br>

### 19.Vocoder<br>
ヴォコーダー

pitch抽出

<br>

![image](https://cloud.githubusercontent.com/assets/28590220/26026388/e8ae9906-3834-11e7-9e95-fc4e8d438674.png)

<br>

pitch control(高音、低音)<br>

````rb
sopr -m 0.5 a01.pitch | excite -p 80 | mlsadf -m 20 -a 0.42 -p 80 a01.mcep | clip -y -32000 32000 | x2x +fs > a01.high.raw
sopr -m 2 a01.pitch | excite -p 80 | mlsadf -m 20 -a 0.42 -p 80 a01.mcep | clip -y -32000 32000 | x2x +fs > a01.low.raw
````

<br>

![image](https://cloud.githubusercontent.com/assets/28590220/26026417/d22c1dec-3835-11e7-9cde-2a6bf5a3be29.png)

<br>

frame shift(高速、低速)<br>

````rb
excite -p 40 a01.pitch | mlsadf -m 20 -a 0.42 -p 40 a01.mcep | clip -y -32000 32000 | x2x +fs > a01.fast.raw
excite -p 160 a01.pitch | mlsadf -m 20 -a 0.42 -p 160 a01.mcep | clip -y -32000 32000 | x2x +fs > a01.slow.raw
````

Hoarse Voice(無声音)

````rb
sopr -m 0 a01.pitch | excite -p 80 | mlsadf -m 20 -a 0.42 -p 80 a01.mcep | clip -y -32000 32000 | x2x +fs > a01.hoarse.raw
````

<br>

Robot Voice(ロボット声)

````rb
train -p 200 -l -1 | mlsadf -m 20 -a 0.42 -p 80 a01.mcep | clip -y -32000 32000 | x2x +fs > a01.robot.raw
````

<br>

スペクトル包絡のαパラメータ + ピッチ操作

````rb
sopr -m 0.5 a01.pitch | excite -p 80 | mlsadf -m 20 -a 0.1 -p 80 a01.mcep | clip -y -32000 32000 | x2x +fs > a01.child.raw
sopr -m 2 a01.pitch | excite -p 80 | mlsadf -m 20 -a 0.6 -p 80 a01.mcep | clip -y -32000 32000 | x2x +fs > a01.deep.raw
````

