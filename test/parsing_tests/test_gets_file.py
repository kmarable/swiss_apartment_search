import yaml
import inspect
import pathlib
import sys
import os
#

current_path = pathlib.Path(__file__).parent.absolute()
sys.path.append(current_path.parents[1].as_posix())
print(sys.path)

from src.parser import Listing

test_file_path = 'test\\parsing_tests\\immoscout_gets.yaml'
with open(test_file_path, encoding='utf8') as file:
    tests_dict = yaml.load(file, Loader=yaml.FullLoader)

print(len(tests_dict), 'tests to run')


methods = inspect.getmembers(Listing)


method_names = [m[0] for m in methods if m[0][0] != '_']
print('All Methods', method_names)
for k,v in tests_dict.items():
    print(k, ":", v['input_text'])
    method_index=(method_names.index(v['method_to_test']))
    method_names.pop(method_index)

print('Methods not tested',method_names)
