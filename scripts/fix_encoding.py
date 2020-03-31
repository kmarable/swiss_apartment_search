import os

import set_env_variables  # noqa

from src.utilities.header import Header
from src.utilities.htmlFile import htmlFile
from src.utilities import get_absolute_path

# hopefully the code should now enforce saving and writing html files with a 
# consistent encoding and this is no longer necessary, but just in case...

class fix_html(htmlFile):

    def read(self):
        # returns dict of header data and the body
        try:
            f = open(self.path, 'r', encoding='utf-8')
            print(f)
            file_lines = f.readlines()
            header_text, body = self.splitHeaderFromBody(file_lines)
            header = Header.parseHeader(header_text)
            return {'HEADER': header, 'BODY': body}
        except:
            f = open(self.path, 'r')
            print('not utf-8', f)
            file_lines = f.readlines()
            header_text, body = self.splitHeaderFromBody(file_lines)
            header = Header.parseHeader(header_text)
            return {'HEADER': header, 'BODY': body}


if __name__ == '__main__':
    lf = os.path.normpath(get_absolute_path("data\\old_saved_pages"))
    files = [os.path.join(lf, f) for f in os.listdir(lf)]
    print(lf)
    for f in files:
        print('current file', f)
        fh = fix_html(f)
        contents = fh.read()
        fh.write(contents['BODY'], contents['HEADER'])
