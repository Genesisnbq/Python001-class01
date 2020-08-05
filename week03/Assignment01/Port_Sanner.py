import os
import json
import socket
import threading
from time import time
from queue import Queue, Empty
from sys import argv, exit

print_lock = threading.Lock()


class PortScanner(object):
    """
    Parameters:
    (1) -url the_web_link
    (2) -method ping/tcp
    (3) -start start_port_num
    (4) -end end_port_num
    (5) -w result.json
    (6) -v True (printing how much time the program has spent)
    (7) -n thread_num
    """

    def __init__(self):
        self.argv_dict = {}
        self.res_dict = {}  # for tcp
        self.result_dict = {}  # for ping
        self.arguments_list = ['-url', '-method', '-start', '-end', '-w', '-v', '-n']
        self.write_file = False
        self.record_time = None

        for argument in self.arguments_list:
            self.check_input(argument)
            self.allocate_arguments(argument)

        # Translate a host name to IPv4 address
        self.target_ip = socket.gethostbyname(self.argv_dict['-url'])
        self.method = self.argv_dict['-method']
        self.tcp = False
        self.ping = False
        self.thread_number = int(self.argv_dict['-n'])

        for method in self.method:
            if method == 'tcp':
                self.tcp = True
            if method == 'ping':
                self.ping = True

        if self.tcp is True:
            self.check_arguments_format()
            self.start_port = int(self.argv_dict['-start'])
            self.end_port = int(self.argv_dict['-end'])

        if self.write_file is True:
            self.result_file_name = self.argv_dict['-w']

        if '-v' in argv:
            self.record_time = self.argv_dict['-v']

        print('-' * 50)
        print('The arguments defined by the user:', self.argv_dict)
        print('Scanning host: {}'.format(self.target_ip))
        print('-' * 50)

    def check_input(self, argument):
        if argument in argv:
            next_element = argv[argv.index(argument) + 1]
            if '-' in next_element:
                print('\n Error: no user-defined argument for {}. \n'.format(argument))
                exit()

    def allocate_arguments(self, argument):
        if argument in argv:
            if argument == '-w':
                self.write_file = True
            if argument == '-method':
                self.argv_dict[argument] = []
                next_element = argv[argv.index(argument) + 1]
                # To avoid the error when users input -method ping/tcp as the last argu
                if argv.index(next_element) != (len(argv) - 1):
                    next_next_element = argv[argv.index(argument) + 2]
                    if '-' not in next_next_element:
                        self.argv_dict[argument].append(next_element)
                        self.argv_dict[argument].append(next_next_element)

                self.argv_dict[argument].append(next_element)
            if argument != '-method':
                self.argv_dict[argument] = argv[argv.index(argument) + 1]

    def check_arguments_format(self):
        if (self.argv_dict['-start'].isdigit() is False) or \
                (self.argv_dict['-end'].isdigit() is False):
            print('\nError: The provided arguments of -start or -end is/are not valid.\n')
            exit()
        else:
            print('Successfully passed the argument format checks.')

    def threader(self):
        while True:
            try:
                # the worker will get one port number from the queue
                port = self.q.get(block=True, timeout=1)
                self.scan(port)
                self.q.task_done()
            except Empty:
                break

    def scan(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        # Ends connection if a port does not respond in 1 second
        result = s.connect_ex((self.target_ip, port))
        # returns an error indicator; open port==0, closed port==1
        try:
            print_lock.acquire()
            if result == 0:
                print('Port {} is open!'.format(port))
                self.open_port_list.append(port)
                self.res_dict[port] = 'open'
            else:
                print('Port {} is closed.'.format(port))
                self.close_port_list.append(port)
                self.res_dict[port] = 'closed'
        finally:
            print_lock.release()
            s.close()

    def tcp_scan(self):

        print('\nStarting to scan ports of the IP'
              ' address {} via TCP... \n'.format(self.target_ip))

        self.open_port_list = []
        self.close_port_list = []

        port_num_range = range(self.start_port, self.end_port)

        self.q = Queue()
        thread_list = []

        for port in port_num_range:
            self.q.put(port)

        for _ in range(self.thread_number):
            t = threading.Thread(target=self.threader)
            thread_list.append(t)
            t.start()

        for t in thread_list:
            t.join()

        if len(self.open_port_list) != 1:
            print('\nSuccessfully scanned {} ports via TCP. \n{} ports are open,'
                  ' {} ports are closed. \n'.format(len(port_num_range),
                                                    len(self.open_port_list),
                                                    len(self.close_port_list))
                  )
        else:
            print('\nSuccessfully scanned {} ports via TCP. \n{} port is open,'
                  ' {} ports are closed. \n'.format(len(port_num_range),
                                                    len(self.open_port_list),
                                                    len(self.close_port_list))
                  )

    def ping_scan(self):
        print('\n Starting to scan ports of the IP'
              ' address {} via Ping... \n'.format(self.target_ip))
        result = os.system('ping -c 1 -W 500 {}'.format(self.target_ip))  # 500 毫秒

        if result == 0:
            print('\n The connection is active! \n')
            self.result_dict[self.target_ip] = 'open'
        else:
            print('\n The connection is closed. \n')
            self.result_dict[self.target_ip] = 'closed'

    def save_json(self):
        """
        Format: port_num: open/closed
        """
        if self.tcp is True:
            with open(self.result_file_name, 'a+') as f:
                content = json.dumps(self.res_dict, ensure_ascii=False) + '\n'
                f.write(content)
            print('\n Successfully saved the tcp connection'
                  ' result into a json file {} \n'.format(self.result_file_name))

        if self.ping is True:
            ping_file_name = 'ping_' + str(self.result_file_name)
            with open(ping_file_name, 'a+') as f:
                content = json.dumps(self.result_dict, ensure_ascii=False) + '\n'
                f.write(content)
            print('\n Successfully saved the ping connection'
                  ' result into a json file {} \n'.format(ping_file_name))


def main():
    start_time = time()
    port_scanner = PortScanner()

    if port_scanner.tcp is True:
        port_scanner.tcp_scan()
    if port_scanner.ping is True:
        port_scanner.ping_scan()
    if port_scanner.write_file is True:
        port_scanner.save_json()

    end_time = time()
    if port_scanner.record_time == 'True':
        print('\n The scanning took {} seconds. \n'.format(end_time - start_time))
    print('-' * 25 + ' end ' + '-' * 25)


if __name__ == '__main__':
    main()
