import requests
from threading import Thread


hosts = open('hosts.txt').read().split('\n')
if '' in hosts: hosts.remove('')
len_hosts = len(hosts)
book_cookies = {"_xsrf": "x"}
book_headers = {"Content-Type": "application/x-www-form-urlencoded", "Cookie":"_xsrf=x", "Connection": "close"}
alive = []
THREAD_NUM = int(len_hosts/4)


def checkLogin(notebook, passwd):
  book_url = "http://"+notebook+"/login"
  book_data = {"_xsrf": "x", "password": passwd}
  try:
    code = requests.post(book_url, headers=book_headers, cookies=book_cookies, data=book_data, verify=False, allow_redirects=False, timeout=3).status_code
    if code == 302:
      alive.append("{}/login?pass={}".format(notebook,passwd))
      return True
  except Exception as e:
    pass

def threader(chunk):
  for creds in chunk:
    notebook = creds[0]
    passwd = creds[1]
    checkLogin(notebook, passwd)

#########################################

cred_args = []
for item in hosts:
  host = item.split('/')
  notebook = host[0]
  passwd = host[1].split('=')[-1]
  cred_args.append((notebook, passwd))

chunks = [cred_args[i * THREAD_NUM:(i + 1) * THREAD_NUM] for i in range((len(cred_args) + THREAD_NUM - 1) // THREAD_NUM )]

threads = []
for chunk in chunks:
  t = Thread(target=threader, args=(chunk,))
  threads.append(t)
for t in threads:
  t.start()
for t in threads:
  t.join()

for life in alive:
  print(life)