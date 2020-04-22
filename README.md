# laptop_display_rest

## 用途

实现Windows系统下的快捷键关闭屏幕功能

执行程序后，屏幕亮度降为0，且不影响其它程序的运行；监听到鼠标或者键盘有输入时，恢复亮度，程序关闭。

## 使用方法

直接运行rest.exe

## 文件功能

| 文件名                      | 功能                                            |
| --------------------------- | ----------------------------------------------- |
| rest_code_in_Powershell.txt | 记录在Powershell下运行的指令                    |
| rest_v1_keyboard.py         | 使用Powershell方法调整亮度的键盘监听程序        |
| rest_v2_keyboard.py         | 使用wmi包方法调整亮度的键盘监听程序             |
| rest_v2_mouse.py            | 使用wmi包方法调整亮度的鼠标监听程序             |
| rest_v3_2ways(threading).py | 通过threading包实现多线程的鼠标和键盘双监听程序 |
| rest_v3_2ways(direct).py    | 直接在pynput监听实现多线程鼠标和键盘双监听程序  |
| rest.exe                    | 由rest_v3_2ways(direct).py打包而来的exe文件     |
| rest.lnk                    | 为实现快捷键运行而创建的快捷方式                |
| README.md                   | 程序文档                                        |
| icon.ico                    | 图标                                            |

打包指令：`pyinstaller -F -w -n rest.exe rest_v3_2ways(direct).py -i rest.ico`

## 开发中遇到的问题

### 问题一：如何降低亮度？

#### 方法一：模拟键盘按键输入

<center>
   <img src="https://i.loli.net/2020/04/20/m8sIqiZP2zMTcFV.png" alt="image-20200420210840043" style="zoom:80%;" />
</center>



   一般的笔记本可以使用Fn+F1-F12实现一些快捷功能，如调整音量等。在我的电脑上，可以使用Fn+F11调低亮度、Fn+F12提高亮度。因此我就想通过软件，多次按Fn+F11调低亮度从而达到熄屏的效果。

   理想很丰满，现实很骨感；我发现这个Fn+F11在键码表中没有，即没有任何一个按键对应这两个键同时按下去时体现的效果（而其它按键，如：调整音量，却在键码表上有）。因此通过模拟键盘的方法无法实现输入Fn+F11。

   难道键码表上没有，pynput包就没有吗？我不信邪，使用了pynput监听键盘，发现当输入Fn+F11时监听系统是没有任何反馈的，即实质上Fn+F11这个键可能使用的不是常规的键盘输入。

   因此最后证实了通过模拟键盘输入来熄屏，这条路是走不通的。



#### 方法二：直接调整屏幕亮度

   既然无法通过模拟键盘输入来降低亮度，那么可以直接调节Windows系统的亮度吗？没想到还真可以使用WMI这个工具来实现。

   刚开始我使用了Powershell中的命令来实现相关功能，并用python来调用Powershell执行；后面经过战略合作伙伴（百度）的提醒，可以在Python中直接调用WMI库执行相关功能。

powershell:

``` powershell
$brightness = 0
$delay = 5
$myMonitor = Get-WmiObject -Namespace root\wmi -Class WmiMonitorBrightnessMethods
$myMonitor.wmisetbrightness($delay, $brightness)
```

python:

``` python
w = WMI(namespace=r'root\wmi')
m = w.WmiMonitorBrightnessMethods()[0]
m.WmiSetBrightness(Brightness=0, Timeout=5)
```

经过测试，真的可以调节亮度。

### 问题二：如何同时监听键盘和鼠标？

监听的函数是以线程的形式实现的，即当检测到相关输入时自动结束线程。因此当要同时监听键盘和鼠标时，就有两个线程同时运行，而当其中一个线程监听到输入时，只会退出其本身，而不影响另一个线程；换言之，若想退出监听，需要有两个输入即键盘和鼠标都进行输入，而不是一个输入即键盘或鼠标输入即可。这就导致了需要先按键盘后按鼠标，或是，先按鼠标再按键盘，才能恢复屏幕的亮度，而这是不合常理的。

刚开始尝试使用信号量，但是发现并不好使，没有像操作系统课里面所讲的信号量那样工作，因此此路不通。

最后采取了一个折衷的办法，当检测到鼠标输入时，模拟键盘进行输入；当检测到键盘输入时，模拟鼠标进行输入。这样就保证了当监听到一个设备输入时，程序可以正常向下运行。

下面展示一下鼠标中的实现，键盘中也是相似的原理。

``` python
def on_click(x, y, button, pressed):
    if not pressed:
        keyboard.Controller().release(keyboard.Key.space)
        # Stop listener
        return False
```

### 问题三：打包发布

编程完成后得到的是python文件，那么使用起来是不够方便的，于是考虑将其打包成可执行文件(exe)。在本项目中使用pyinstaller完成打包工作。遇到的问题是在python 3.7中执行`pip install pyinstaller`时会报错；解决方法是通过conda来安装(`conda install pyinstaller`)，即可避免因为配置环境问题而报错。

### 问题四：快捷键调用

在Windows中想用快捷键直接调用程序，可以使用系统内置的方法。首先为文件创建一个快捷方式，其次在快捷方式的属性中就可以对快捷键进行设置。使用这个方法的最大问题是调用程序的速度较慢，存在一个数秒的延迟，经研究应为Windows系统本身的原因，与其它因素无关。

<center>
    <img alt = "image-20200421212450724" src = "https://i.loli.net/2020/04/21/tlBIGdJDWYh6Ofx.png" style="zoom:50%"/>
</center>


另外在Windows中还可以使用快捷键来调用任务栏中的程序，调用方法为：`Win+数字`。比如在图示中，若想调用第一个程序，只需要输入`Win+1`即可。

<center>
    <img src="https://i.loli.net/2020/04/21/IgosOtn2eQi1Py4.png" alt="image-20200421214016576" style="zoom:100%;" />
</center>



## 参考文章地址

https://docs.microsoft.com/en-us/windows/win32/wmicoreprov/wmisetbrightness-method-in-class-wmimonitorbrightnessmethods

https://pynput.readthedocs.io/en/latest/index.html