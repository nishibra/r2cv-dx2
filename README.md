# r2cv_dynamxel2_2wheel
Dynamxelによる2Wheelステアリング方式で、まずは操縦型のロボットを紹介します。ロボットの名前はDX2WSとします。
### ロボット : DX2WS
![robo](/pics-r/2w-dx.png)

---
### 目次
[1. サーボモータDYNAMIXELについて](#1)

[2. DYNAMIXELのコントロール](#2)

[3. サーボの設定ツール](#3)

[4. サーボの設定](#4)

[5. キーボードによるロボットコントローラー](#5)

[6. ロボットの操縦プログラム](#6)

[7. ロボットの操縦方法](#7)

[8. DX2WS 3Dプリンターデータ](#8)

[<R2CVに戻る>](https://github.com/nishibra/r2cv-1) 

---
<a id="1"></a>
## 1. サーボモータDYNAMIXELについて
ここではXL330とM288を使用します。
XL330はスピード型で足回りに使用します。
M288はトルク型でカメラのパン、チルトに使用します。
詳細スペックは以下のサイトをご覧ください。

> [DYNAMIXEL XL330-M288-T](https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/)

<a id="2"></a>
## 2. Dynamxel設定ツール
またDynamxelサーボの設定ツールは以下にあります。

> [DYNAMIXEL Wizard 2.0](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/)

Windows版は以下よりダウンロードしてインストールしてください。

[ダウンロードwindows版](https://www.robotis.com/service/download.php?no=1670)

以下の画面になればインストール成功です。

![dxwi](/pics-r/dxlwi.png)

Linux版もあります。(RasPi4では使えないようです。)

[ダウンロードLinux版](https://www.robotis.com/service/download.php?no=1671)

インストール手順
```
$ sudo chmod 775 DynamixelWizard2Setup_x64
$ ./DynamixelWizard2Setup_x64
$ sudo usermod -aG dialout <your_account_id>
$ reboot
```

<a id="3"></a>
## 3. ロボットのサーボの設定
写真のロボットのサーボのIDと通信速度を設定します。
ここでは通信速度は1Mbpsで使用します。

ロボットの足回りに使用するサーボはXL330でIDは
> 右モータ ID:1
> 
> 左モータ ID:2
> 
とします。回転モードとして動作させます。

カメラのパン、チルト用サーボにはM288を使用します。
IDは3,4で位置決めモードの動作とします。

> パン ID:3
> 
> チルト ID:4
> 

### DYNAMIXEL Wizard
DYNAMIXEL Wizardをインストール、起動したPCにシリアルインターフェイスU2D2を接続します。
U2D2に電源と1つのサーボモータを接続します。
上記画面でScanを実行します。この時Scan条件をOptionで設定できます。
サーボが見つかると以下の画面となり、必要な項目の設定ができます。

![dxwi](/pics-r/dxls.png)

ここでは

> 通信速度:　1Mbps
> 
> ID: 1/2/3/4
> 
> モード: velosity control/extended position control

などを設定します。


<a id="4"></a>
## 4. DYNAMIXEL2のコントロール
### -DX2ライブラリー
Dynamixelには Protocol V1と Protocol V2があり、それぞれのProtocolに対応したライブラリが株式会社ベストテクノロジーより提供されています。ここで使用するのはProtocol V2の
ライブラリーすなわちDX2ライブラリーです。

以下のサイトで詳細情報が得られます。

[Dynamixel Library](https://www.besttechnology.co.jp/modules/knowledge/?BTE100%20DXHAT)

以下のようにダウンロード、解凍して、コンパイルします。
```
$ cd ~
$ wget https://www.besttechnology.co.jp/download/DX2LIB_V2.8.zip
$ unzip DX2LIB_V2.8.zip
```
unzipが必要なら以下を実行します。
```
$ sudo apt install build-essential unzip
```
ビルトします。
```
$ cd ~/DX2LIB_v2.8/DX2LIB/
$ bash ./build_dx2lib.sh
```
サンプルを実行します。
```
$ cd ~/DX2LIB_v2.8/SampleCode/Python/
$ gedit smpl1.py
```
で以下を変更し実行します。

> COMPort = b'/dev/ttyAMA2'
> Baudrate = 1000000
> TargetID = 1

```
$ python3 smpl1.py
```
pamission deneyとなったら以下を実行してください。
```
$ sudo adduser $USER dialout
```
dx2libはダイナミックリンクライブラリーdx2lib.so.2.6を参照します。

### -DX2WSコントロールプログラム
ここてはdx2libを利用してロボットの動作を実現するプログラムdx2_con.pyを作成しました。
dx2con.pyプログラムをros2で実行します。
まずパッケージを作成します。
```
$ ros2 pkg create --build-type ament_python r2dx2w
```
作成されたフォルダーに以下をコピーします。
```
dx2lib.py
dx2lib.so.2.6
dx2_con.py
```

ubuntu@ubuntu:~/ros2ws/src/r2dx2w$にあるsetup.pyに以下を追記します。
```
entry_points={
        'console_scripts': [
         'dx2c = ' + package_name + '.dx2_con:main',   <------追記
        ],
```        
コルコンビルトします。
```
$ cb
```
プログラムを実行します。
```
$ ros2 run r2dx2w dx2c
```

下記のようにサーボの型式などが表示され、ロボットカメラが左右に動き、ロボットが前後左右に動けばOKです。
 
![dyna](/pics-r/control.png)

![dyna](/pics-r/dx2wc.gif)
 
動作の詳細はdx2_con.pyのmain()をご参照ください。

<a id="5"></a>
## 5. キーボードによるロボットコントローラー
続いてキーボードをコントローラーとして使用してカメラ画像を見ながらロボットを遠隔操縦します。
キーボードよりコマンドを配信するプログラムを作ります。

-1).キーボードによるコマンド配信

●大文字
 
 ![key](/pics-r/keymap.png)
 
 > Camere E:up C:down S:left F:right D:zero
 >
 > Speed  U:up M:doun H:left K:right J:zero
 
●小文字

走行モード設定

> d: drive with speed control
> 
> s:stop f:fw100 b:bk100 r:rt90 l:lt90 u:ut180
> 
> g:get_angle q:quit v:voltage
> 
> a: middle position with arm control　n/N: torque off/on

### -2).プログラム
キー入力により以下のmsgを配信します。

```
/car_command 
/cmd_vel 
```

/car_command ではString型でコマンドを、/cmd_velwでは Twistで移動速度と角度を配信します。
ここでもパッケージを作成します。
packageの作成

```
$ cs
$ ros2 pkg create --build-type ament_python commander
```

gitより以下をdx2w_key_commander.pyをコピーします。
setup.pyを変更します。

```
entry_points={
        'console_scripts': [
        'dx2key = ' + package_name + '.dx2w_key_commander:main',
        ],
    },
```
ビルドします。
```
$ cb
```
実行します。
```
$ ros2 run commander dx2key
```
new terminal

```
$ ros2 topic list
```

でtopicがリストされます。
```
$ ros2 topic echo /car_command
$ ros2 topic echo / cmd_vel
```

で配信内容が表示されます。上記のキーに対応してtopicが配信されているのが確認できればOKです。

<a id="6"></a>
## 6. ロボットの操縦ブログラム
KEYコマンダーの命令に従いロボットを動作させるプログラムです。

ubuntu@ubuntu:~/ros2ws/src/r2dx2w/r2dx2w$にdx2w_op.pyをコピーします。

setup.pyに以下を追記します。
```
'dx2o = ' + package_name + '.dx2_op:main',   <------追記
```
コルコンビルトします。
```
$ cb
```
プログラムを実行します。
```
$ ros2 run r2dx2w dx2o
```

<a id="7"></a>
## 7. ロボットの操縦方法
ロボットを遠隔操縦するには以下の手順で端末を立ち上げます。

1)ロボットのRaspi4を起動します。
WiFiにつないでipアドレスを確認しておきます。

2)Windows PCからリモートデスクトップにてRasPi4のipアドレスにログインします。

3)カメラのプログラムを起動します。
```
$ ros2 run camera cam1
```

4)rqtを起動しカメラ画像を見えるようにします。
```
$ rqt
```
Plugins->Visualization->Image Viewからtopicを選定する。

![rqt](/pics-r/rqt.png)

5)キーコマンダーを起動
```
$ ros2 run commander dx2key
```

6)ロボットのプログラムを起動
```
$ ros2 run r2dx2w dx2o
```
7)ロボットの操縦方法

カメラ画像を見ながらキーコマンダーを起動した画面でキー操作をしてロボットを操縦します。

![dyna](/pics-r/control2.png)

<a id="8"></a>
## 8.DX2WS 3Dプリンターデータ
DX2WSを3D printerで製作するにはdx2w_stlフォルダーのstlファイルを使ってください。 フラットな面を下にして出力すると良いでしょう。

組み立ては図や動画を参照してください。

下図はロボットの裏面です。ここでキャスターとホイールを使用しますが、㈱ベストテクノロジーから入手できます。サーボやHatと一緒に購入すると良いでしょう。

![裏面](/pics-r/ura.jpg)

