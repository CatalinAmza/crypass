from random import randrange
from crypt import *
import time
import sys
from Log import Log
import os
import shutil
import pyperclip

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
        if "password" in log.header[i].lower():
            new_data.append(password)
            j = 1
            i += 1
        else:
            if len(infos[i-j].replace(" ", "")) == 0:
                new_data.append("N/A")
            else:
                new_data.append(infos[i-j])
            i += 1
    log.add(new_data)
    log.save()
    pyperclip.copy(password)

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

def get_file_name(text):
    for i in range(len(text)):
        if text[len(text) - 1 - i] == "/":
            return text[len(text) - i:]
    return text

def get_folder(text):
    for i in range(len(text)):
        if text[len(text) - 1 - i] == "/":
            return text[:len(text) - i]
    return ""

def check_choice(text):
    try:
        x = int(text)
    except:
        print("Invalid choice, try again")
        return check_choice(input("1. Add new account\n2. Get an account\n3. Change a password\n4. Remove an account\n5. Change the master key\n6. Print a decrypted temp\nYour choice: "))
    else:
        if x in range(7):
            return x
        else:
            print("Invalid choice, try again")
            return check_choice(input("1. Add new account\n2. Get an account\n3. Change a password\n4. Remove an account\n5. Change the master key\n6. Print a decrypted temp\nYour choice: "))

if len(sys.argv) != 3:
    print("Use this with the full path of your password file and your key.")
    time.sleep(3)
else:
    key = sys.argv[2].encode()
    if len(key) != 32:
        print("Wrong key.")
        time.sleep(3)
    else:
        file = sys.argv[1]
        now = time.time()
        working_file = get_folder(sys.argv[0]) + get_file_name(file) + '.' + str(now).replace(".", "")
        shutil.copyfile(file, working_file)
        decrypt_file(working_file, key)
        try:
            data = Log(file_name=working_file, separator="  ||  ")
            if len(data.log[0]) == 1:
                raise Exception
        except Exception:
            print("Wrong key.")
            time.sleep(3)
        else:
            choice = check_choice(input("1. Add new account\n2. Get an account\n3. Change a password\n4. Remove an account\n5. Change the master key\n6. Print a decrypted temp\nYour choice: "))
            if choice == 1:
                infos = []
                for head in data.header:
                    if "password" not in head.lower():
                        infos.append(input(head + ": "))
                length = int(input("Password length: "))
                generate(getType(), infos, length, data)
            elif choice in [2,3,4]:
                for i in range(len(data.header)):
                    if "password" in data.header[i].lower():
                        pos = i
                index = search(data)
                if choice == 2:
                    pyperclip.copy(str(data.log[index][pos]))
                    data.log[index].remove(data.log[index][pos])
                    print("Here's your account: %s. \nCopied password to clipboard." % str(data.log[index]))
                elif choice == 3:
                    length = int(input("Password length: "))
                    x = data.log[index]
                    x.remove(x[pos])
                    data.log.remove(data.log[index])
                    generate(getType(), x, length, data)
                    print("Password successfully changed. Copied new password to clipboard.")
                else:
                    x = data.log.pop(index)
                    data.save()
                    print("Removed the following account: %s. Enjoy." % str(x))
            elif choice == 5:
                key = ""
                while len(key) != 32:
                    key = input("Insert your new key (32 characters long): ")
                key = key.encode()
                print("Successfully changed your key.")
            else:
                open(os.path.expanduser("~/Desktop/" + 'temp'), 'w').write(data.__str__())
            print("Program terminated. Waiting 3 seconds before deleting the decrypted file.")
            time.sleep(3)
            shutil.copyfile(working_file, file)
            os.remove(working_file)
            encrypt_file(file, key)
