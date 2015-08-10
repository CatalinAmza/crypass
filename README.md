# crypass

256 bit encrypted password saver

use with header like "service  ||  id_name  ||  password  ||  comments"

launch it with full_file_path as parameter. example: "python3 crypass.py C:/mypasses.txt"

example of decrypted file: http://i.imgur.com/7eZ0ZbF.png

key initialiazed during first use (comment out line 123 for the first usage and when asked for the password, just enter the one you desire)

USE WITH:
* python 3.4
* pyperclip from here: https://pypi.python.org/pypi/pyperclip
* pycrypto from here: https://github.com/axper/python3-pycrypto-windows-installer
* pysha from here: https://pypi.python.org/pypi/pysha3/
* (on Linux) eventually do a sudo apt-get install python3-setuptools
