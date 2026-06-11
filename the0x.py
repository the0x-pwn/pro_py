from concurrent.futures import ThreadPoolExecutor
import requests
import sys
import os
import argparse
# color
RED = "\033[0;31m"
GREEN = "\033[0;32m"
DARK_GRAY = "\033[1;30m"
END = "\033[0m"

session = requests.Session()
count = 0
time_out = 0
connection_error = 0
parse = argparse.ArgumentParser()
parse.add_argument('-u','--url',required=True,metavar="This flag takes the target value",type=str)
parse.add_argument('-w','--wordlist',required=True,type=str,metavar="This flag takes on the value of the brute force list")
parse.add_argument('--timeout',required=False,default=5,type=int,metavar="This flag takes a numerical value to determine the delay time")
parse.add_argument('-t','--threads',required=False,type=int,default=30,metavar="This flag takes into account the speed at which orders are sent")
parse.add_argument('-fc',required=False,default=None,type=lambda x : [int(i) for i in x.split(',')],metavar="This flag takes value by taking unwanted responses")
parse.add_argument('-fs',required=False,default=None,type=lambda x: [int(i) for i in x.split(',')],metavar="This flag takes a value that represents the size of the pages that are not desired to be displayed")
parse.add_argument('-H',required=False,type=str,metavar="This flag takes the cost of adding a header upon request")
arg = parse.parse_args()

url = arg.url
wordlist = arg.wordlist
timeout = arg.timeout
threads = arg.threads
filter_code = arg.fc
filter_size = arg.fs
header = arg.H
headers = {}

if header:
    for h in header.split(','):
        if ':' not in h:
            continue
        key,value = h.split(':',1)
        headers[key.strip()] = value.strip()
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


   
def request(url, word):
    global session
    global count
    global connection_error
    global time_out

    count += 1
    full_path = f"{url}/{word.strip()}"

    try:
        response = session.get(
            url=full_path,
            headers=headers,
            timeout=timeout,
            allow_redirects=True
        )


        if filter_size is not None and len(response.content) in filter_size:
            return

        if filter_code is not None and response.status_code in filter_code:
            return

        if response.status_code == 200 and len(response.content) > 0:
            print("\r", end="")
            print(f"{GREEN}[+] {full_path:<50} [Status: {response.status_code}] [Size: {len(response.content)} B]{END}")
        else:
            print(
                f'{DARK_GRAY}\r[*] Requests sent: {count} '
                f'{END}{DARK_GRAY}||{END} '
                f'{RED}ReadTimeout({time_out}){END} '
                f'{DARK_GRAY}||{END} '
                f'{RED}ConnectionError({connection_error}){END}',
                end=''
            )

    except requests.exceptions.ConnectionError:
        connection_error += 1

    except requests.exceptions.ReadTimeout:
        time_out += 1
    

with open(wordlist,'r',encoding='latin-1') as words:
        with ThreadPoolExecutor(max_workers=threads) as ex:
            for word in words:
                ex.submit(request,url,word)
