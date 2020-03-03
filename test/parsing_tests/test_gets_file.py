import yaml
import pathlib
import sys
import os

current_path = pathlib.Path(__file__).parent.absolute()
sys.path.append(current_path.parents[1].as_posix())

from src.parser import Listing
from src.utilities import get_public_members

test_file_path = sys.argv[1]
with open(test_file_path, encoding='utf8') as file:
    tests_dict = yaml.load(file, Loader=yaml.FullLoader)

print(len(tests_dict), 'tests to run in', test_file_path)

method_names = get_public_members(Listing)

print(type(method_names[0]))

print('All Methods', method_names)
print('fields:', [m.replace('get', '') for m in method_names])
methods_tested = set()
for k, v in tests_dict.items():
    print(k, ":", v['input_text'])
    methods_tested.add(v['method_to_test'])

print('Methods not tested', set(method_names) - methods_tested)
