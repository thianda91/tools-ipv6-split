## IPv6 地址拆分工具

[更新历史](CHANGELOG.md)  [![HitCount](http://hits.dwyl.io/thianda/xda-tools/ipv6-split.svg)](http://hits.dwyl.io/thianda/xda-tools/ipv6-split) 

本工具拟实现以下两个功能：

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

**实现思路**

```python
from IPy import IP, IPSet

ip = IP('2019:1234:ABCD::/48')
suffix = '/56'

def ip_split(ip, suffix):
    ip1 = IP(ip.strNormal(0) + suffix) # 2019:1234:ABCD::/64
    result = [ip1]
    ip -= ip1
    for i in ip:
        if i.strNetmask() != suffix: # 掩码与预期的不一致
            result.extend(ip_split(i, suffix))
        else:
            result.append(i)
    return result

result = ip_split(ip, suffix)
for i in result:
    print(i)
index_mark = int(suffix[1:]) - int(ip.strNetmask()[1:])
total = 2**index_mark
print('共输出 {} 行。（2^{}）'.format(total, index_mark))
```

不建议拆分后的条目过多，会导致分割时间过长甚至卡死。



**2.给出 IP 段 和想要拆分出来的单个 IP，自动将单个 IP 取出，余下 IP 尽可能合并**

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

**实现思路**

```python
from IPy import IP, IPSet

ip = IP('2019:1234:ABCD::/48')
ip_one = IP('2019:1234:ABCD:0:10:E00::1/128')
ips = ip - ip_one

print(ip_one)
count = 1
for i in ips:
    count += 1
    print(i)
print('共输出 {} 行。'.format(count))
```

拆分后，生成的 IP 段 所包含的范围，与拆分前所包含的范围一致。

本工具用于解决 IPv6 地址段从未备案时合并为单条`/48`的状态，到启用后使用某一个`/128`或某一小段`/127`时，拆分地址段较麻烦的痛点。



