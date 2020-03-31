from src.utilities import response_from_text
from src.utilities.header import Header

ENDHEADER = 'END HEADER'


class htmlFile():

    def __init__(self, path):
        self.path = path

    def read(self):
        # returns dict of header data and the body
        with open(self.path, 'r', encoding='utf-8') as f:
            file_lines = f.readlines()
            header_text, body = self.splitHeaderFromBody(file_lines)
            header = Header.parseHeader(header_text)
            return {'HEADER': header, 'BODY': body}

    def splitHeaderFromBody(self, file_lines):
        isEnd = [ENDHEADER in l for l in file_lines]
        header_end = isEnd.index(True)
        header_text = file_lines[:header_end]
        body = ''.join(file_lines[header_end+1:])
        return header_text, body

    def getResponse(self):
        body = self.read()['BODY']
        return(response_from_text(body))

    def write(self, text, header):
        with open(self.path, 'w', encoding='utf-8') as f:
            print('opening for writing', self.path)
            header.writeToHtmlFile(f)
            f.write(ENDHEADER)
            f.write(text)
        f.close()
