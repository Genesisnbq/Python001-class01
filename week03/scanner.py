import argparse
import os
import socket
import time
import threading

# scanner.py - n 4 - f ping - ip 192.168.0.1-192.168.0.100
# scanner.py - n 10 - f tcp - ip 192.168.0.1 - w result.json


def usage():
    print(
        """
请输入正确的命令行格式：
    example: python scanner.py -n 4 -f ping -ip 192.168.0.1-192.168.0.3 -w result.json
    example: python scanner.py -n 10 -f tcp -ip 127.0.0.1 -w result.json
    n: 并发数量
    f: -f ping 进行 ping 测试， -f tcp 进行 tcp 端口开放、关闭测试
    ip: 连续 ip, 地址支持 192.168.0.1-192.168.0.100 写法
    w: 扫描结果进行保存
"""
    )


semaphore = threading.BoundedSemaphore(5)  # 最多允许5个线程同时运行


def main():
    _number = 1
    _function = ''
    _ip = ''
    _sip = ''
    _eip = ''
    _write = ''

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', dest='Number', type=int, required=True,
                        default='1', help='target Number')
    parser.add_argument('-f', '--function', dest='Function', type=str, required=True,
                        default='', help='target Function')
    parser.add_argument('-ip', '--ip', dest='ip', type=str, required=True,
                        default='', help='target ip')
    parser.add_argument('-w', '--write', dest='Write',
                        default='', type=str, help='target Write to File')
    # print(parser.parse_args())

    args = parser.parse_args()
    _number = args.Number
    _function = args.Function
    _ip = args.ip
    _write = args.Write

    global semaphore
    semaphore = threading.BoundedSemaphore(_number)  # 最多允许5个线程同时运行

    if _ip.find('-') != -1:
        _ips = _ip.split('-')
        # print(_ips)
        _sip = _ips[0]
        _eip = _ips[1]

    if _function == 'ping':
        _sips = splitIP(_sip)
        if len(_sips) < 4:
            print('开始ip错误')
            raise

        _eips = splitIP(_eip)
        if len(_eips) < 4:
            print('结束ip错误')
            raise

        if _sips[0] != _eips[0] or _sips[1] != _eips[1] or _sips[2] != _eips[2]:
            print('不能跨网段扫码')
            raise

        print('测试开始...')
        # print('进行 tcp 端口开放、关闭测试...')
        print('开始ip: ' + _sip + ' ~ 结束ip: ' + _eip)
        for i in range(int(_sips[3]), int(_eips[3])+1):
            ip = '%s.%s.%s.%s' % (_sips[0], _sips[1], _sips[2], str(i))

            t = threading.Thread(target=scanIP, args=(ip, _write))
            t.start()

        print('测试结束！')

    elif _function == 'tcp':
        print('测试开始...')
        for port in range(20, 100):
            t = threading.Thread(target=get_ip_status,
                                 args=(_ip, port, _write))
            t.start()
        print('测试结束！')
    else:
        print('不能识别的命令')


def splitIP(str):
    if str == '':
        return
    else:
        ips = str.split('.')
        return ips


def scanIP(host, logFilename=''):
    semaphore.acquire()
    result = os.popen('ping -c 1 -t 1 %s' % (host)).read()
    if 'ttl' in result:
        print(f'{host} 在线')
        if logFilename != '':
            logFile(logFilename, f'{host} 在线')
    else:
        print(f'{host} 不在线')
        if logFilename != '':
            logFile(logFilename, f'{host} 不在线')

    semaphore.release()


def get_ip_status(ip, port, logFilename=''):
    semaphore.acquire()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((ip, port))
        result = '{0} port {1} is open'.format(ip, port)
        print(result)
        if logFilename != '':
            logFile(logFilename, result)
    except Exception as err:
        result = '{0} port {1} is not open'.format(ip, port)
        print(result)
        if logFilename != '':
            logFile(logFilename, result)
    finally:
        server.close()
        semaphore.release()


def logFile(filename, text):
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(str(localtime) + ': ' + text + '\r\n')


if __name__ == "__main__":
    main()
