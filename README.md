# IPv6 地址拆分工具

## 功能介绍

本工具实现以下三个功能。对 IPv4、IPv6 地址均可操作。

### 功能 1

**1. 给出 IP 段和想要拆分成的 IP 段长度，自动拆分为指定的掩码长度的 IP 段**

例子：

```
已知 2019:1234:ABCD::/48，想要拆分成 /64。
即可生成：
2019:1234:ABCD::/64
2019:1234:ABCD:1::/64
2019:1234:ABCD:2::/64
...
2019:1234:ABCD:FFFF::/64
```

不建议拆分后的条目过多，会导致分割时间过长甚至卡死。

### 功能 2

**2. 给出 IP 段 和想要拆分出来的单个 IP，自动将单个 IP 取出，余下 IP 尽可能合并**

例子 1：

```
已知 2019:1234:ABCD::/48，想要将其中的 2019:1234:ABCD::1/128 拆分出来
即可生成：
2019:1234:ABCD::/128
2019:1234:ABCD::1/128
2019:1234:ABCD::2/127
2019:1234:ABCD::4/126
2019:1234:ABCD::8/125
2019:1234:ABCD::10/124
2019:1234:ABCD::20/123
...
2019:1234:ABCD:4000::/50
2019:1234:ABCD:8000::/49

共 81 行
```

例子 2：

```sh
已知 2019:1234:ABCD::/48，想要将其中的 2019:1234:ABCD:0:10:E00::1/128 拆分出来
即可生成：
2019:1234:ABCD::/76
2019:1234:ABCD:0:10::/85
2019:1234:ABCD:0:10:800::/86
2019:1234:ABCD:0:10:C00::/87
2019:1234:ABCD:0:10:E00::/128
2019:1234:ABCD:0:10:E00::1/128
2019:1234:ABCD:0:10:E00::2/127
2019:1234:ABCD:0:10:E00::4/126
...
2019:1234:ABCD:0:10:E80::/89
2019:1234:ABCD:0:10:F00::/88 #
2019:1234:ABCD:0:10:1000::/84 #
2019:1234:ABCD:0:10:2000::/83
2019:1234:ABCD:0:10:4000::/82
2019:1234:ABCD:0:10:8000::/81
2019:1234:ABCD:0:11::/80
2019:1234:ABCD:0:12::/79
2019:1234:ABCD:0:14::/78
2019:1234:ABCD:0:18::/77 #
2019:1234:ABCD:0:20::/75 #
2019:1234:ABCD:0:40::/74
2019:1234:ABCD:0:80::/73
2019:1234:ABCD:0:100::/72
2019:1234:ABCD:0:200::/71
...
2019:1234:ABCD:4000::/50
2019:1234:ABCD:8000::/49

共 81 行
```

拆分后，生成的 IP 段 所包含的范围，与拆分前所包含的范围一致。

### 功能 3

**3. 给出若干 IP/掩码 格式(可由功能1/功能2生成)， 输出同数量的 起始IP，终止IP 格式。**

例子：

```sh
已知文本`input.csv`，内容如下：
2019:1234:ABCD::/128
2019:1234:ABCD::1/128
2019:1234:ABCD::2/127
2019:1234:ABCD::4/126
2019:1234:ABCD::8/125
需要生成：
2019:1234:ABCD::	2019:1234:ABCD::
2019:1234:ABCD::1	2019:1234:ABCD::1
2019:1234:ABCD::2	2019:1234:ABCD::3
2019:1234:ABCD::4	2019:1234:ABCD::7
2019:1234:ABCD::8	2019:1234:ABCD::15
```

## 使用方法

以下假设小工具的文件名为`ipv6Split.exe`。小工具需要在命令行模式运行。

1. 在小工具的文件夹空白处，按住`shift`键，右键选择“**在此处打开命令窗口**”。
2. 输入`ipv6Split`，**直接按回车**可查看简要使用帮助。
3. 执行`ipv6Split -h`，查看**详细帮助**。

可根据使用帮助输入对应的参数，拆分后的结果默认保存在同目录下（基于时间命名的 `txt` 文件）。

### 优雅使用

在`cmd`中，若参数过长，换行显示很不友好，可设置增加`cmd`的显示宽度：

1. `cmd`窗口标题处右键，选择”**属性**“。
2. 在”布局“选项卡设置**宽度**（默认`80`，推荐改为 `120`）。
3. 屏幕缓冲区和窗口的宽度都需要修改。
4. 修改仅本次生效，若想今后打开`cmd`均生效，则在第一步右键后选择“**默认值**”。

### 功能1-split

```sh
ipv6Split -i 2019:1234:abcd::/48 -s 56 --split

# --split ：将 IPv6 地址拆分成掩码相同的 IPv6 地址段
# -i ：要拆分的 ipv6 是 2019:1234:abcd::/48
# -s ：拆分后的掩码是 56

最终会生成若干个掩码为 /56 的 ipv6 地址段，其包含的范围与原 /48 的地址段相同。
```

### 功能2--pick-up

```sh
ipv6Split -i 2019:1234:abcd::/48 -o 2019:1234:abcd::/127 --pick-up

# --pick-up ：将指定的 IPv6 地址/段提取出来
# -i ：要拆分的 ipv6 是 2019:1234:abcd::/48
# -o ：要拆分出来的是 2019:1234:abcd::/127

最终结果会包含 2019:1234:abcd::/127，且包含的范围与原 /48 的地址段相同。不会造成遗漏。
```

### 功能3--trans

```sh
ipv6Split -f input.csv --trans

# --trans ：将若干IP/掩码格式转换成:起始IP,终止IP
# -f ：要转换的文件名(可由功能 1 或功能 2 生成)

最终结果会是若干 起始IP,终止IP 格式。
```

### 其他参数1--full

 运行命令中添加`--t`，输出的 IPv6 地址为完整格式，而不是默认的压缩格式。

```sh
# 比如：
ipv6Split -i 2019:1234:abcd::/48 -o 2019:1234:abcd::/127 --pick-up --full 
```

### 其他参数2--cli

运行命令中添加`--cli`，结果会直接在命令行输出，而不是默认的输出到文件。


```sh
# 比如：
ipv6Split -i 2019:1234:abcd::/48 -s 56 --split --cli
ipv6Split -i 2019:1234:abcd::/48 -o 2019:1234:abcd::/127 --pick-up --full --cli
```

