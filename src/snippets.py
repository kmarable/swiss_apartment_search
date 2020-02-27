##############
    @classmethod
    def get_project_path(self):
        current_location = os.path.dirname(os.path.realpath(__file__))
        project_pattern = re.compile(r'(.*)\\src\\utilities')
        current_project = re.findall(project_pattern, current_location)[0]
        return(current_project)

    def test_get_project_path(self):
        project_path = r'C:\Users\Kathryn\Documents\2github\swiss_apartment_search'
        result = DataFile.get_project_path()
        self.assertEqual(project_path, result)

##################
