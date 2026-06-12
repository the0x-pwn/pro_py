from concurrent.futures import ThreadPoolExecutor
import requests
import sys
import os
import argparse
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from threading import Lock

start = time.perf_counter()
# color
RED = "\033[0;31m"
GREEN = "\033[0;32m"
DARK_GRAY = "\033[1;30m"
CYAN = "\033[1;36m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
END = "\033[0m"

session = requests.Session()
count = 0
time_out = 0
connection_error = 0
delay = 0
found = 0
lock_loop = Lock()

parse = argparse.ArgumentParser(
    prog='GhostDir',
    description='Directory & File Discovery Tool',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parse.add_argument('-u','--url',metavar="URL",required=True,help="This flag takes the target value",type=str)
parse.add_argument('-w','--wordlist',metavar="WORDLIST",required=True,type=str,help="This flag takes on the value of the brute force list")
parse.add_argument('-X', metavar="METHOD", required=False, default='GET', type=str, help="HTTP method to use (GET, POST, HEAD, OPTIONS, PUT, DELETE, PATCH)")
parse.add_argument('-T',metavar="TIMEOUT",required=False,default=10,type=int,help="This flag takes a numerical value to determine the delay time")
parse.add_argument('-t','--threads',metavar='THREADS',required=False,type=int,default=30,help="This flag takes into account the speed at which orders are sent")
parse.add_argument('-fc',metavar="FILTER CODE",required=False,default=None,type=lambda x : [int(i) for i in x.split(',')],help="This flag takes value by taking unwanted responses")
parse.add_argument('-fs',metavar="FILTER SIZE",required=False,default=None,type=lambda x: [int(i) for i in x.split(',')],help="This flag takes a value that represents the size of the pages that are not desired to be displayed")
parse.add_argument('-H',metavar="HEADERS",required=False,type=str,help="This flag takes the cost of adding a header upon request")
parse.add_argument('--proxy',metavar="PROXY", default=None,required=False,type=str,help='Route requests through a proxy (e.g. Burp Suite)')
parse.add_argument('--mode', metavar="MODE",default=None,required=False,type=str,choices=['burp'],help='Run mode: burp (slow)')
arg = parse.parse_args()

url = arg.url
wordlist = arg.wordlist
timeout = arg.T
threads = arg.threads
filter_code = arg.fc
filter_size = arg.fs
proxy = arg.proxy
mode = arg.mode
method = arg.X.upper()
header = arg.H
headers = {}




if mode == 'burp':
    threads = 3
    timeout = max(timeout, 10)
    delay = 0.1

# check url
def check_url():
    global url
    global session
    if not url.startswith(('http://','https://')):
        print(f"{RED}[-] Invalid URL: '{url}'\n[!] URL must start with http:// or https:// {END}")
        sys.exit()
    if url.endswith('/'):
        url = url[:-1]

    return url
check_url()

# check file
def check_word_list():
    global wordlist
    if not os.path.isfile(wordlist):
        print(f"{RED}[-] Wordlist file not found: {wordlist}{END}")
        sys.exit()
check_word_list()

def check_method(x):
    ALLOWED_METHODS = ['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'DELETE', 'PATCH']
    if method not in ALLOWED_METHODS:
        print(f"{RED}[-] Invalid method: '{method}'\n[!] Allowed: {', '.join(ALLOWED_METHODS)}{END}")
        sys.exit()
check_method(method)


def check_header(header_user,stor_header):
    if header_user:
        for h in header_user.split(','):
            if ':' not in h:
                continue
            key,value = h.split(':',1)
            stor_header[key.strip()] = value.strip()
check_header(header,headers)


proxies = None
def check_proxy(proxy):
    global proxies
    if proxy is not None:
        proxies = {
            "http" : proxy,
            "https" : proxy
        }
check_proxy(proxy)


def format_size(size):
    if size < 1024:
        return f"{DARK_GRAY}{size} B{END}"
    elif size < 1024 ** 2:
        return f"{GREEN}{size / 1024:.2f} KB{END}"
    elif size < 1024 ** 3:
        return f"{YELLOW}{size / (1024 ** 2):.2f} MB{END}"
    else:
        return f"{RED}{size / (1024 ** 3):.2f} GB{END}"
    

def request(url, word):
    global session
    global count
    global connection_error
    global time_out
    global found
    status_code = [200, 201, 204, 301, 302, 307, 403, 405, 500]
    with lock_loop:
        count += 1
    full_path = f"{url}/{word.strip()}"

    if delay:
        time.sleep(delay)
    
    try:
        response = session.request(
            method=method,
            url=full_path,
            headers=headers,
            timeout=timeout,
            allow_redirects=True,
            proxies=proxies,
            verify=False
        )

        if filter_size is not None and len(response.content) in filter_size:
            return

        if filter_code is not None and response.status_code in filter_code:
            return

        if response.status_code in status_code and len(response.content) > 0:
            found += 1
            with lock_loop:
                print(f"\r{' ' * 100}\r{GREEN}[+] {word.strip()} [Status: {BLUE}{response.status_code}{END}] [Size: {BLUE}{format_size(len(response.content))}{END}]{END}")
        else:
            with lock_loop:
                print(
                    f'{YELLOW}\r[*] Requests sent: {count} '
                    f'|| '
                    f'Method({method}) '
                    f'|| '
                    f'ReadTimeout({time_out}) '
                    f'|| '
                    f'ConnectionError({connection_error}){END}',
                    end='',
                    flush=True
                )

    except requests.exceptions.ConnectionError:
        with lock_loop:
            connection_error += 1

    except requests.exceptions.ReadTimeout:
        with lock_loop:
            time_out += 1
    


def banner():
    print(rf"""{CYAN}

 ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗██████╗ ██╗██████╗
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██╔══██╗██║██╔══██╗
██║  ███╗███████║██║   ██║███████╗   ██║   ██║  ██║██║██████╔╝
██║   ██║██╔══██║██║   ██║╚════██║   ██║   ██║  ██║██║██╔══██╗
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ██████╔╝██║██║  ██║
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═════╝ ╚═╝╚═╝  ╚═╝

{CYAN}            By: Ali Waled{END}
{GREEN}            GhostDir v1.0{END}
{YELLOW}      Directory & File Discovery Tool{END}

{CYAN}══════════════════════════════════════════════════════════════{END}

{GREEN}[TARGET]{END}     {url}
{GREEN}[WORDLIST]{END}   {wordlist}
{GREEN}[METHOD]{END}   {method}
{GREEN}[THREADS]{END}    {threads}
{GREEN}[TIMEOUT]{END}    {timeout}s
{GREEN}[HEADERS]{END}    {headers}
{GREEN}[FILTER CODE]{END} {filter_code}
{GREEN}[FILTER SIZE]{END} {filter_size}
{GREEN}[MODE]{END} {mode}
{GREEN}[PROXY]{END} {proxy}

{CYAN}══════════════════════════════════════════════════════════════{END}

""")
    
banner()

print('\n')
with open(wordlist,'r',encoding='latin-1') as words:
        with ThreadPoolExecutor(max_workers=threads) as ex:
            for word in words:
                ex.submit(request,url,word)

end = time.perf_counter()
elapsed = end - start
print(f"\n{CYAN}[*] Scan completed in {elapsed:.2f}s{END}")
print(f"{CYAN}[*] Total requests: {count} | Found: {found}{END}")







