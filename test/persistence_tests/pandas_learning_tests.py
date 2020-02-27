import unittest
import pandas as pd
import os
import sys
from src.utilities.data_file import DataFile
from datetime import datetime
from shutil import copy
import re


def write_test_file(file_name):
    f = open(file_name, "w")
    f.write("Now the file has more content!")
    f.close()


class TestReadAndBackupFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.join('test', 'persistence_tests')
        cls.backup_dir = os.path.join(cls.test_dir, 'raw_backups')

    def setUp(self):
        self.tfile = DataFile(self.test_dir, 'test_readFile.csv')

        if not os.path.exists(self.tfile.backup_dir):
            os.mkdir(self.tfile.backup_dir)

    def test_constructor_makes_data_file(self):
        self.assertIsInstance(self.tfile, DataFile)

    def test_read_file(self):
        test_df = pd.DataFrame({'Floor': [1, 2, 3], 'Price': [2300, 120, 190]})
        read_df = self.tfile.read_file()
        pd.testing.assert_frame_equal(test_df, read_df)

    def test_make_backup_filename(self):
        time_str = datetime.now().strftime("%d_%m_%Y_%H_%M")
        result = self.tfile.make_backup_filename()
        directory_result, file_result = os.path.split(result)
        self.assertTrue(os.path.samefile(directory_result, self.backup_dir))
        self.assertTrue(re.match(time_str, file_result))

    def test_calling_backup_old_file_creates_files_in_backup_directory(self):
        if os.path.exists(self.backup_dir):
            nfiles_before = len(os.listdir(self.backup_dir))
        else:
            nfiles_before = 0
        for i in range(4):
            self.tfile.backup_old_file()
        n_new_files = len(os.listdir(self.backup_dir))-nfiles_before
        self.assertEqual(n_new_files, 4)

    def test_backup_old_file_creates_identical_file(self):
        new_file_path = self.tfile.backup_old_file()
        result = pd.read_csv(new_file_path)
        expected = self.tfile.read_file()
        pd.testing.assert_frame_equal(result, expected)

    def test_get_unique_filename_increments_filename(self):
        result = self.tfile.get_unique_filename('multi_backup_test.csv')
        expected = os.path.join(self.backup_dir, 'multi_backup_test_1.csv')
        self.assertEqual(result, expected)

    def test_get_latest_backup(self):
        latest_file = self.tfile.get_latest_backup()
        latest_time = os.stat(latest_file).st_mtime
        backup_paths = self.tfile.get_backup_files()
        for f in backup_paths:
            self.assertGreaterEqual(latest_time, os.stat(f).st_mtime)


class TestUpdateFile(unittest.TestCase):
    def setUp(self):

        self.test_dir = os.path.join('test', 'persistence_tests')
        self.backup_dir = os.path.join(self.test_dir, 'raw_backups')
        self.tfile = DataFile(self.test_dir, 'test_updateFile.csv')

        def initialize_file_to_upate():
            base_file = os.path.join(self.test_dir, 'test_readFile.csv')
            file_to_update = self.tfile.file_path
            copy(src=base_file, dst=file_to_update)

        initialize_file_to_upate()

    def test_updating_a_file_creates_backup(self):
        old_data = self.tfile.read_file()
        self.tfile.update_file(pd.DataFrame())
        latest_file = self.tfile.get_latest_backup()
        backed_up_data = pd.read_csv(latest_file)
        pd.testing.assert_frame_equal(old_data, backed_up_data)

    def test_updating_a_file_appends_new_data(self):
        new_data = pd.DataFrame({'Floor': [4, 5, 6], 'Price': [300, 400, 500]})
        expected = pd.DataFrame({'Floor': [1, 2, 3, 4, 5, 6],
                                'Price': [2300, 120, 190, 300, 400, 500]})
        self.tfile.update_file(new_data)
        result = self.tfile.read_file()
        pd.testing.assert_frame_equal(expected, result)

    def test_updating_a_file_with_new_columns_fills_na(self):
        na = float('NaN')
        new_data = pd.DataFrame({'Floor': [4, 5, 6], 'Area': [30, 40, 50]})
        expected = pd.DataFrame({'Floor': [1, 2, 3, 4, 5, 6],
                                 'Price': [2300, 120, 190, na,  na,  na],
                                 'Area': [na,  na,  na, 30.0, 40.0, 50.0]})
        self.tfile.update_file(new_data)
        result = self.tfile.read_file()
        pd.testing.assert_frame_equal(expected, result)


class TestOS(unittest.TestCase):
    def test_get_file_access_time(self):
        file_to_check = os.path.join('test',
                                     'persistence_tests',
                                     'test_readFile.csv')
        file_status = os.stat(file_to_check)
        expected = 1581689307.7330613
        # expected timestamp corresponds to '2020-02-14 15:08:27.733061'
        self.assertEqual(file_status.st_mtime, expected)

    def test_mtime_is_larger_for_files_added_later(self):
        file_times = []
        for i in range(3):
            test_file = 'blah_blah' + str(i) + '.txt'
            write_test_file(test_file)
            file_time = os.stat(test_file).st_mtime
            file_times.append(file_time)
        self.assertTrue(sorted(file_times))


class TestPath(unittest.TestCase):
    def test_add_subdirectory_to_path(self):
        input = 'C:\\Users\\Kathryn\\'
        expected = 'C:\\Users\\Kathryn\\Documents\\2github'
        result = os.path.join(input, 'Documents', '2github')
        self.assertEqual(expected, result)


class TestPandas(unittest.TestCase):

    def test_fillDfColumn(self):
        test_df = pd.DataFrame()
        test_column = [1, 2, 3]
        column_name = 'Floor'
        test_df[column_name] = test_column
        self.assertEqual(test_df[column_name][0], test_column[0], 'first element of column not equal to original')
        self.assertEqual(test_df.shape[1], 1, 'df has less than or equal to 1 column after adding a column to an empty df')

    def test_write_first_object_to_file(self):
        test_df = pd.DataFrame({'Floor':[1,2,3], 'Price': [2300,1200,1900]})
        file_name = 'first_write_test.csv'
        test_df.to_csv(file_name, index=False)
        read_df = pd.read_csv(file_name)

        pd.testing.assert_frame_equal(test_df,read_df)

        if os.path.exists(file_name):
            os.remove(file_name)


if __name__ == '__main__':
    unittest.main()
