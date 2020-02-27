import unittest
import pandas as pd
import os
import * from Listing

#OK, tried with series and it does not work because it overwrites files and also can't be read back by pd.read_csv.

class TestRawDataFile(unittest.TestCase):


    def test_set_filename(self):
        file_name = 'first_object_test.csv'
        RawFile.set_filename(file_name)
        RawFile.g

    def test_write_first_object_to_file(self):
        file_name = 'first_object_test.csv'
        test1 = {'Floor': 2, 'Price': 1700}
        try :
            RawFile.set_filename(file_name)
        except:
            pass
        else:
            RawFile
            test_df = pd.read_csv(file_name)
            print('TYPE', type(test_df.iloc[0]))
            print('VALUE', test_df.iloc[0,0])
            print('COMPARE', test_series1)
            #self.assertEqual(test_df.iloc[0], test_series, 'Not getting first series back correctly')
        finally:
            if os.path.exists(file_name):
                pass
            #os.remove(file_name)

if __name__ == '__main__':
    unittest.main()
