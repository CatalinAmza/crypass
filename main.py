from random import randrange
import subprocess
from crypt import *
import time
import sys
from Log import Log
import os
import shutil

FILE = 'temp' # password file name

def copyToClipboard(text):
    command = "echo " + text.strip() + "|clip"
    return subprocess.check_call(command, shell=True)

def generate(choice, infos, length, log):
    my_chars = []
    if choice == 1:
        for i in range(26):
            my_chars.append(chr(97 + i))
            my_chars.append(chr(65 + i))
        for i in range(10):
            my_chars.append(chr(48 + i))
    else:
        for i in range(32, 127):
            my_chars.append(chr(i))
    n = len(my_chars)
    password = ''
    for nth_char in range(length):
        password += my_chars[randrange(n)]
    new_data = []
    i = 0
    j = 0
    while i < len(log.header):
        if "password" in log.header[i].lower():  # should've probably made a super-item header
            new_data.append(password)
            j = 1
            i += 1
        else:
            new_data.append(infos[i-j])
            i += 1
    log.add(new_data)
    log.save()
    copyToClipboard(password)


def contains(l1, l2):
    g_res = True
    for a in l2:
        res = False
        for b in l1:
            if a in b:
                res = True
        g_res &= res
    return g_res

def getType():
    print("1. Letters + Numbers")
    print("2. ASCII")
    return int(input("Your choice: "))


def search(data):
    scoop = input("What are you looking for?\n").split()
    res = []
    for i in range(len(data.log)):
        if contains(data.log[i], scoop):
            res.append(i)
    if len(res) == 0:
        print("No such accounts found. Retrying in 1 second.")
        time.sleep(1)
        return search(data)
    elif len(res) == 1:
        return res[0]
    else:
        print("Too many results, restrict your search. Retrying in 1 second.")
        time.sleep(1)
        return search(data)

if len(sys.argv) != 2:
    print("Use this with a key.")
else:
    key = sys.argv[1].encode() # provide it as a parameter at launch
    if len(key) != 32:
        print("Wrong key.")
        time.sleep(3)
    else:
        now = time.time()
        shutil.copyfile(FILE, FILE + '.' + str(now).replace(".", ""))
        decrypt_file(FILE, key)
        try:
            data = Log(file_name=FILE, separator="  ||  ")
        except Exception:
            print("Wrong key.")
            time.sleep(3)
        else:
            choice = int(input("1. Add new account\n2. Get an account\n3. Remove an account\n4. Print a decrypted temp\nYour choice: "))
            if choice == 1:
                infos = []
                for head in data.header:
                    if "password" not in head.lower():
                        infos.append(input(head + ": "))
                length = int(input("Password length: "))
                generate(getType(), infos, length, data)
            elif choice in [2,3]:
                for i in range(len(data.header)):
                    if "password" in data.header[i].lower():
                        pos = i
                index = search(data)
                if choice == 2:
                    print("Here's your account: %s. Copied password to clipboard." % str(data.log[index]))
                if choice == 3:
                    x = data.log.pop(index)
                    data.save()
                    print("Removed the following account: %s. Enjoy." % str(x))
            elif choice == 4:
                open(os.path.expanduser("~/Desktop/" + 'temp'), 'w').write(data.__str__())
            else:
                print("Invalid choice.")
            print("Program terminated. Waiting 3 seconds before deleting the decrypted file.")
            time.sleep(3)
            encrypt_file(FILE, key)
            try:
                os.remove(FILE + '.' + str(now).replace(".", ""))
            except:
                ()
