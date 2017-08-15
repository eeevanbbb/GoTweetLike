class Blacklist(object):
    blacklist_file_name = "blacklist.txt"

    def __init__(self):
        self.blacklist = []

        self.read_blacklist()

    def read_blacklist(self):
        try:
            with open(self.blacklist_file_name) as blacklist_file:
                for line in blacklist_file:
                    self.blacklist.append(line)
        except IOError:
            print('Could not read blacklist from file: ' + self.blacklist_file_name)