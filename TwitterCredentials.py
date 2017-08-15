class Credentials(object):
    key_file_name = "keys.txt"

    def __init__(self):
        self.keys = {}

        self.read_keys()

    def read_keys(self):
        try:
            with open(self.key_file_name) as key_file:
                for line in key_file:
                    key, value = line.split("=")
                    self.keys[key.strip()] = value.strip()
        except IOError:
            print('Could not read twitter keys from file: ' + self.key_file_name)

    def consumer_key(self):
        return self.keys.get('consumer_key')

    def consumer_secret(self):
        return self.keys.get('consumer_secret')

    def access_key(self):
        return self.keys.get('access_key')

    def access_secret(self):
        return self.keys.get('access_secret')