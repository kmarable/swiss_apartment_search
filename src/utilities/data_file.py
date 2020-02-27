import pandas as pd
from datetime import datetime
from shutil import copy
import re
import os


class DataFile():
    def __init__(self, directory='data', file_name='raw_data.csv'):
        self.dir = directory
        self.file = file_name
        self.file_path = os.path.join(directory, file_name)
        self.backup_dir = os.path.join(directory, 'raw_backups')

        if not os.path.exists(self.backup_dir):
            os.mkdir(self.backup_dir)

    def read_file(self):
        return (pd.read_csv(self.file_path))

    def backup_old_file(self):
        backup_name = self.make_backup_filename()
        copy(self.file_path, backup_name)
        return(backup_name)

    def make_backup_filename(self):
        time_str = datetime.now().strftime("%d_%m_%Y_%H_%M")
        new_filename = time_str+'.csv'
        new_path = os.path.join(self.backup_dir, new_filename)
        if os.path.exists(new_path):
            new_path = self.get_unique_filename(new_filename)
        return(new_path)

    def get_unique_filename(self, new_filename):
        # new filename is just the name without the directory path
        # and returns a complete path form project directory
        f_pat = new_filename[:-4] + '_([0-9]*)\.csv'
        files = [f for f in os.listdir(self.backup_dir) if re.match(f_pat, f)]
        if len(files) == 0:
            latest_file = 0
        else:
            latest_file = max([int(re.findall(f_pat, f)[0]) for f in files])
        new_filename = new_filename[:-4] + '_' + str(latest_file+1) + '.csv'
        new_path = os.path.join(self.backup_dir, new_filename)
        return (new_path)

    def get_backup_files(self):
        backup_names = os.listdir(self.backup_dir)
        backup_paths = [os.path.join(self.backup_dir, f) for f in backup_names]
        return(backup_paths)

    def get_latest_backup(self):
        backup_paths = self.get_backup_files()
        update_times = [os.stat(f).st_mtime for f in backup_paths]
        latest_file_ix = update_times.index(max(update_times))
        return backup_paths[latest_file_ix]

    def update_file(self, new_data):
        self.backup_old_file()
        old_data = self.read_file()
        data_to_write = old_data.append(new_data, sort=False)
        data_to_write.to_csv(self.file_path, index=False)
