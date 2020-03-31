import sys
import os

project_folder = os.path.dirname(os.path.dirname(__file__))
os.environ['PROJECT_FOLDER'] = project_folder
print('project folder', os.environ['PROJECT_FOLDER'])
if project_folder not in sys.path:
    sys.path.insert(0, project_folder)
