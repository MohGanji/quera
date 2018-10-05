from os import *
import glob
import shutil

class FileManager:
    def __init__(self):
        self.backups = list()
        pass

    def create_dir(self, name, address):
        if path.exists(address) and name not in listdir(address):
            mkdir("{}/{}".format(address, name))

    def create_file(self, name, address):
        if path.exists(address) and name not in listdir(address):
            open("{}/{}".format(address, name), O_CREAT)

    def delete(self, name, address):
        if path.exists(address) and name in listdir(address):
            filepath = "{}/{}".format(address, name)
            self.backups.append(filepath)
            shutil.copyfile(filepath, '{}.bak'.format(filepath))
            remove("{}".format(filepath))

    def find(self, name, address):
        res = []
        for filename in glob.iglob('{}/**/{}'.format(address, name), recursive=True):
            res.append(filename)
        return res

    def restore(self, name):
        files = [a for a in self.backups if name in a]
        if not len(files):
            return
        last = files[-1]
        if last in self.backups: self.backups.remove(last)
        rename('{}.bak'.format(last), last)
        pass

    

fm = FileManager()
# fm.create_dir('tst', '.')
# fm.create_file('something.txt', 'tst')
# fm.delete('something.txt', 'tst')
# fm.restore('something.txt')
fm.create_dir('tst', '.')
fm.create_file('tst', 'tst')
fm.create_dir('tst1', 'tst')
fm.create_dir('tst2', 'tst/tst1/')

fm.create_file('tst.txt', 'tst')
fm.create_file('tst.txt', 'tst/tst1')
fm.create_file('tst.txt', 'tst/tst1/tst2')
print(fm.find('tst.txt', 'tst'))
fm.delete('tst.txt', 'tst')
fm.delete('tst.txt', 'tst/tst1/')
fm.delete('tst.txt', 'tst/tst1/tst2')
fm.restore('tst.txt')
fm.restore('tst.txt')