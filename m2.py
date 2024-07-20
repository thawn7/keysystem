import subprocess
import os
import time
import colorama
import ctypes
from termcolor import colored
from keyauth import api
import sys
import platform
import hashlib
from datetime import datetime


if platform.system() == 'Windows':
    os.system('cls & title Python Example')  # clear console, change title
elif platform.system() == 'Linux':
    os.system('clear')  # clear console
    sys.stdout.write("\x1b]0;Python Example\x07")  # change title
elif platform.system() == 'Darwin':
    os.system("clear && printf '\e[3J'")  # clear console
    os.system('''echo - n - e "\033]0;Python Example\007"''')  # change title

def getchecksum():
    md5_hash = hashlib.md5()
    file = open(''.join(sys.argv), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest

keyauthapp = api(
    name = "misa", #App name (Manage Applications --> Application name)
    ownerid = "fsn9HqQouF", #Owner ID (Account-Settings --> OwnerID)
    secret = "9333f445d4e3409f41e9191f132b1e308a0e127040401f56aa01e8d85d4b4f01", #App secret(Manage Applications --> App credentials code)
    version = "1.0",
    hash_to_check = getchecksum()
)

subs = keyauthapp.user_data.subscriptions  # Get all Subscription names, expiry, and timeleft
for i in range(len(subs)):
    sub = subs[i]["subscription"]  # Subscription from every Sub
    expiry = datetime.utcfromtimestamp(int(subs[i]["expiry"])).strftime(
        '%Y-%m-%d %H:%M:%S')  # Expiry date from every Sub
    timeleft = subs[i]["timeleft"]  # Timeleft from every Sub

    print(f"[{i + 1} / {len(subs)}] | Subscription: {sub} - Expiry: {expiry} - Timeleft: {timeleft}")

colorama.init()

print(colorama.Fore.CYAN + " Connecting...." + colorama.Fore.RESET)

time.sleep(3.5)
def answer():
    try:
        key = input('Enter your Key: ')
        keyauthapp.license(key)
    except KeyboardInterrupt:
        os._exit(1)

answer()

print(f"\n Key Expires at: " + datetime.utcfromtimestamp(int(keyauthapp.user_data.expires)).strftime('%Y-%m-%d %H:%M:%S'))
time.sleep(4)
print(colored('''                                                                                                                                                                                  
  o          o   __o__     o__ __o           o         
 <|\        /|>    |      /v     v\         <|>        
 / \\o    o// \   / \    />       <\        / \        
 \o/ v\  /v \o/   \o/   _\o____           o/   \o      
  |   <\/>   |     |         \_\__o__    <|__ __|>     
 / \        / \   < >              \     /       \     
 \o/        \o/    |     \         /   o/         \o   
  |          |     o      o       o   /v           v\  
 / \        / \  __|>_    <\__ __/>  />             <\ 
                                                       
''', "light_yellow"))
time.sleep(3)
console_handle = ctypes.windll.kernel32.GetConsoleWindow()

if console_handle != 0:
    ctypes.windll.user32.ShowWindow(console_handle, 0)

subprocess.call(["python", os.path.join(os.getcwd(), "m1.py")])
