# -*- coding: utf-8 -*-

import os
from IPy import IP
import re


class ipv6Split(IP):
    """
    ipv6 分割
    """

    def __init__(self, ipv6, mask=48):
        """
        初始化 + 校验
        """
        array = ipv6.split('/')
        if len(array) == 1:
            self.mask = mask
        elif array[1].isdigit():
            self.mask = int(array[1])
            if 20 <= self.mask <= 128:
                if self.isValidateIpv6(array[0]):
                    self.ipv6 = array[0]
                else:
                    print('The ipv6 is illegal! Now will quit...')
                    os.system('pause')
                    exit()
            else:
                print('The mask is illegal! Now will quit...')
                os.system('pause')
                exit()
        IP.__init__(self, ipv6, make_net=True)

    def isValidateIpv6(self, ipv6):
        """
        判断 ipv6 格式是否正确
        """
        ipv6
        matchobj = re.match(r'^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$', ipv6)
        if matchobj:
            return True
        else:
            return False

    def splitIn2(self):
        """
        将 ipv6 地址段平均拆分成 2 个地址段
        """
        newPerfixlen = self.prefixlen()+1
        return [IP(x).make_net(newPerfixlen).strCompressed() for x in self.strNormal(3).split('-')]


if __name__ == '__main__':
    ipv6str = '2019:1234:ABCD:4:5::7/48'
    print('input: '+ipv6str)
    ip = ipv6Split(ipv6str)
    print(ip.splitIn2())
