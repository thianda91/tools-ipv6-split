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
    VERSION = '0.9'
    # COLOR_GROUPS = {"Switches" : colors.bold & colors.yellow}
    outputs = []
    echo_to_cli = False   # 默认为输入到文件，而不是直接在命令行输入。
    o_type = False  # 默认输出为压缩格式，而不是完整格式。
    # ip = '2019:1234:ABCD::/48'
    # suffix = 56

    def now(self):
        return datetime.strftime(datetime.now(), '%Y-%m-%d.%H%M%S')

    def usage(self):
        '''显示使用样例'''
        print(self.PROGNAME,'v{}\n'.format(self.VERSION))
        fun1_doc = self.split.__doc__ if self.split.__doc__ else ""
        fun2_doc = self.pick_up.__doc__ if self.pick_up.__doc__ else ""
        fun3_doc = self.trans.__doc__ if self.trans.__doc__ else ""
        print('功能1：' + fun1_doc)
        print('功能2：' + fun2_doc)
        print('功能3：' + fun3_doc)
        print('\n使用示例：（使用 -h 查看详细）\n')
        print(self.PROGNAME, '-i 2019:1234:abcd::/48 -s 56 --split')
        print(self.PROGNAME,
              '-i 2019:1234:abcd::/48 -o 2019:1234:abcd::/127 --pick-up')
        print(self.PROGNAME, '-f input.csv --trans')
        print('\n其他参数：（使用 -h 查看详细）\n')
        print('--full、--cli')
        print('\n~~~~ !!!双击直接运行仅可查看此帮助，使用功能请在命令行下运行!!!')
        print('按回车键继续...')

    @cli.switch('-h')
    def help(self):
        '''显示帮助和使用样例'''
        # self.usage()
        super().help()
        print('****仅运行', self.PROGNAME, '可查看使用示例（无 -h 参数）')

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
            if self.o_type:
                self.outputs.append(i.strFullsize())
            else:
                self.outputs.append(i.strCompressed())
        tips = '拆分后个数 {} 。（个数=2的{}次幂）'.format(total, self.index_mark)
        self.__out(tips)

    def __pick_up(self):
        output_ip_mask = self.output_ip.prefixlen()
        ip_mask = self.ip.prefixlen()
        total = int(output_ip_mask) - int(ip_mask) + 1
        result = self.ip - self.output_ip
        if self.o_type:
            self.outputs.append(self.output_ip.strFullsize())
            for i in result:
                self.outputs.append(i.strFullsize())
        else:
            self.outputs.append(self.output_ip.strCompressed())
            for i in result:
                self.outputs.append(i.strCompressed())
        tips = '拆分后个数 {} 。（个数=掩码相减再+1）'.format(total)
        self.__out(tips)

    def __trans(self):
        with open(self.input_file, 'r') as f:
            for line in f:
                _ip = IP(line.strip())
                if self.o_type:
                    # self.outputs.append(_ip.strFullsize(3).replace('-', ','))
                    self.outputs.append("{},{}".format(_ip[0].strFullsize(), _ip[-1].strFullsize()))
                else:
                    self.outputs.append("{},{}".format(_ip[0], _ip[-1]))
        self.__out()

    def __out(self, tips=""):
        '''结果输出'''
        _result = '\n'.join(self.outputs)
        if self.echo_to_cli:
            print(_result)
        else:
            fileName = 'result-{}.csv'.format(self.now())
            with open(fileName, 'w') as f:
                f.write(_result)
            print('\n\n**拆分结果的文件名基于时间生成，不会覆盖旧文件**')
            print('文件保存在小工具运行目录：\n\t{}\n'.format(fileName))
            print(tips)

    @cli.switch(names='-i', argtype=str)
    def input(self, input_ip):
        '''原 IP 地址段'''
        self.ip = IP(input_ip)

    @cli.switch('--split', requires=['-s'], excludes=['-o'])
    def split(self):
        '''功能1.将 IP 地址拆分成掩码相同的 IP 地址段'''
        self.method = self.__split

    @cli.switch('--pick-up', requires=['-o'], excludes=['-s'])
    def pick_up(self):
        '''功能2.将指定的 IP 地址/段提取出来'''
        self.method = self.__pick_up

    @cli.switch('-s', argtype=int, group=split.__doc__ if split.__doc__ else "")
    def new_netmask(self, suffix):
        '''要拆分成的掩码(配合 -i 参数)'''
        self.index_mark = suffix - self.ip.prefixlen()
        if(self.index_mark) < 0:
            print('错误： 拆分后的掩码大于原IP段的掩码！')
            return
        self.suffix = '/' + str(suffix)

    @cli.switch('-o', argtype=str, group=pick_up.__doc__ if pick_up.__doc__ else "")
    def output(self, output_ip):
        '''要提取的 IP 地址/段(配合 -i 参数)'''
        self.output_ip = IP(output_ip)

    @cli.switch('--trans', requires=['-f'])
    def trans(self):
        '''功能3.将若干IP/掩码格式转换成：起始IP,终止IP'''
        self.method = self.__trans

    @cli.switch('-f', argtype=str, group=trans.__doc__ if trans.__doc__ else "")
    def file_in(self, input_file_name):
        '''要转换的文件名(可由功能 1 或功能 2 生成)'''
        self.input_file = input_file_name

    @cli.switch('--full', group='其他参数')
    def output_type(self):
        '''输出完整的 IP 地址'''
        self.o_type = True

    @cli.switch('--cli', group='其他参数')
    def echo_through_cli(self):
        '''直接在命令行打印结果'''
        self.echo_to_cli = True

    def main(self, *args, **kwargs):
        if hasattr(self, 'method'):
            start_time = datetime.now()
            self.method()
            total_time = (datetime.now() - start_time).total_seconds()
            print('\n>>> 拆分用时： {:4.4f} 秒'.format(total_time))
            return 0
        else:
            print('\n*********************************************')
            print('****欢迎使用 Xianda 小工具****')
            print('*********************************************\n')
            self.usage()
            input()
            return 0


if __name__ == '__main__':
    try:
        Ipv6Split.run()
    except Exception as e:
        print('运行出错了。多数情况是IP地址输入有误哦~报错信息如下：')
        print(e)
