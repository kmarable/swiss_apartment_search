import yaml

test_file_path = 'test\\parsing_tests\\immoscout_gets.yaml'
with open(test_file_path, encoding='utf8') as file:
    tests_dict = yaml.load(file, Loader=yaml.FullLoader)

print(len(tests_dict), 'tests to run')

for k,v in tests_dict.items():
    print(k, ":", v['input_text'])
