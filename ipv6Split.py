#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from IPy import IP, IPSet
from plumbum import cli
from datetime import datetime

ipv6_reg = r'^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$'


class Ipv6Split(cli.Application):
    '''用于 IPv6 地址拆分  --Xianda'''

    PROGNAME = 'ipv6Split'
    # PROGNAME = colors.green | 'ipv6Split'
    # PROGNAME = __file__
    VERSION = '0.4'
    # COLOR_GROUPS = {"Switches" : colors.bold & colors.yellow}
    outputs = []
    echo_to_cli = False   # 默认为输入到文件，而不是直接在命令行输入。
    # ip = '2019:1234:ABCD::/48'
    # suffix = 56

    def now(self):
        return datetime.strftime(datetime.now(), '%Y-%m-%d.%H%M%S')

    def usage(self):
        '''显示使用样例'''
        print(self.PROGNAME,)
        print('================= verison: v{}\n'.format(self.VERSION))
        print('功能1：' + self.split.__doc__)
        print('功能2：' + self.pick_up.__doc__)
        print('\n用例：（使用 -h 查看更多帮助）\n')
        print(self.PROGNAME, '-i 2019:1234:abcd::/48 -s 56 --split')
        print(self.PROGNAME,
              '-i 2019:1234:abcd::/48 -o 2019:1234:abcd::/127 --pick-up\n')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    @cli.switch('-h')
    def help(self):
        '''显示帮助和使用样例'''
        # self.usage()
        super().help()

    def split_recursion(self, ip, suffix):
        '''递归法'''
        ip1 = IP(ip.strNormal(0) + suffix)  # 2019:1234:ABCD::/64
        result = [ip1]
        ip -= ip1
        for i in ip:
            if i.strNetmask() != suffix:  # 掩码与预期的不一致
                result.extend(self.split_recursion(i, suffix))
            else:
                result.append(i)
        return result

    def __split(self):
        total = 2**self.index_mark
        result = self.split_recursion(self.ip, self.suffix)
        for i in result:
            self.outputs.append(i.strCompressed())
        self.__out()
        print('拆分后个数 {} 。（个数=2的{}次幂）'.format(total, self.index_mark))

    def __pick_up(self):
        result = self.ip - self.output_ip
        self.outputs.append(self.output_ip.strCompressed())
        for i in result:
            self.outputs.append(i.strCompressed())
        self.__out()
        # print(self.outputs[0].strCompressed())
        print('拆分后个数 {} 。（个数=掩码相减再+1）'.format(len(self.outputs)))

    def __out(self):
        '''结果输出'''
        _result = '\n'.join(self.outputs)
        if self.echo_to_cli:
            print(_result)
        else:
            fileName = 'result-{}.txt'.format(self.now())
            with open(fileName,'w') as f:
                f.write(_result)
            print('\n\n**输出结果的文件名基于时间生成，不会覆盖旧文件**')
            print('文件保存在小工具运行目录：\n\t{}\n'.format(fileName))

    @cli.switch(names='-i', argtype=str)
    def input(self, input_ip):
        '''原 IPv6 地址段'''
        self.ip = IP(input_ip)

    @cli.switch('--split', requires=['-s'], excludes=['-o'])
    def split(self):
        '''将 IPv6 地址拆分成掩码相同的 IPv6 地址段'''
        self.method = self.__split

    @cli.switch('--pick-up', requires=['-o'], excludes=['-s'])
    def pick_up(self):
        '''将指定的 IPv6 地址（段）提取出来'''
        self.method = self.__pick_up

    @cli.switch('-s', int, group=split.__doc__)
    def new_netmask(self, suffix):
        '''要拆分成的掩码'''
        self.index_mark = suffix - self.ip.prefixlen()
        if(self.index_mark) < 0:
            print('错误： 拆分后的掩码大于原IP段的掩码！')
            return
        self.suffix = '/' + str(suffix)

    @cli.switch('-o', str, group=pick_up.__doc__)
    def output(self, output_ip):
        '''要提取的 IPv6 地址（段）'''
        self.output_ip = IP(output_ip)

    @cli.switch('--cli')
    def echo_through_cli(self):
        '''直接在命令行输入结果'''
        self.echo_to_cli = True

    def main(self):
        if hasattr(self, 'method'):
            self.method()
        else:
            print('\n*********************************************')
            print('\t****欢迎使用 Xianda 小工具****')
            print('*********************************************\n')
            self.usage()


if __name__ == '__main__':
    try:
        Ipv6Split.run()
    except Exception as e:
        print('运行出错了。多数情况是IP地址输入有误哦~报错信息如下：')
        print(e)
