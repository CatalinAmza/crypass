class Log(): # no error detection, use carefully
    def __init__(self, file_name='temp', separator=-1): # separator = -1 for one-item lines
        self.file_name = file_name
        self.separator = separator
        self.header = []
        self.log = []
        self.open()
        self.text = []

    def __str__(self):
        self.create_printable()
        self.text.sort()
        res = ""
        for line in self.text:
            res += line + "\n"
        return res[:-1]

    def open(self):
        try:
            backup = open(self.file_name, "r")
            if self.separator != -1:
                self.header = [x.strip() for x in backup.readline().split(self.separator)]
                backup.readline()
                for line in backup:
                    self.log.append([x.strip() for x in line.split(self.separator)])
            else:
                self.header = backup.readline().strip()
                backup.readline()
                for line in backup:
                    self.log.append(line.strip())
            backup.close()
        except:
            ()

    def create_printable(self):
        self.text = []
        if self.separator != -1:
            if self.log != []:
                log_unit_size = len(self.log[0])
                lengths = [max([len(str(self.log[i][j])) for i in range(len(self.log))]) for j in range(log_unit_size)]
                header = ""
                for i in range(len(self.header)):
                    padding = lengths[i] - len(self.header[i])
                    header += int(padding / 2) * " " + self.header[i] + int((padding + 1) / 2) * " "
                    if i < len(self.header) - 1:
                        header += self.separator
                self.text.append(header)
                self.text.append(len(header) * "-")
                for log_bit in self.log:
                    line = ""
                    for i in range(log_unit_size):
                        line += str(log_bit[i]) + " " * (lengths[i] - len(str(log_bit[i])))
                        if i < log_unit_size - 1:
                            line += self.separator
                    self.text.append(line)
        else:
            self.text = [str(log_bit) for log_bit in self.log]

    def save(self):
        backup = open(self.file_name, "w")
        backup.write(self.__str__())
        backup.close()

    def add(self, log_bit):
        if len(log_bit) == len(self.log[0]):
            self.log.append(log_bit)
        else:
            print("Could not add %s to your log. Sizes not matching" % str(log_bit))

    def replace_log(self, new_log):
        self.log = new_log
