# crypass

256 bit encrypted password saver (32 character key)

use with header like "service  ||  id_name  ||  password  ||  comments"

example of decrypted file: http://i.imgur.com/7eZ0ZbF.png

key initialiazed during first use (comment out line 91 - decrypt(FILE, key) - for the first usage)

----------

WORKS ONLY WITH WINDOWS (at least until i figure out a universal method to copy to clipboard)

TO DO:
* should implement a changeKey option

USE WITH:
* python 3.4
* pywin from here: http://sourceforge.net/projects/pywin32/files/pywin32/
* pycrypto from here :https://github.com/axper/python3-pycrypto-windows-installer
