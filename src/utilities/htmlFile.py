from src.utilities import response_from_text
import os
ENDHEADER = 'END HEADER'


class htmlFile():

    def __init__(self, path):
        self.path = path

    def read(self):
        # returns dict of header data and the body
        with open(self.path, 'r') as f:
            file_lines = f.readlines()
            header_end = file_lines.index(ENDHEADER+'\n')
            header = file_lines[:header_end]
            header_dict = self.parseHeader(header)
            body = ''.join(file_lines[header_end+1:])

        return (header_dict, body)

    def getResponse(self):
        body = self.read()[1]
        return(response_from_text(body))

    def parseHeader(self, header_lines):
        header_dict = {}
        for h in header_lines:
            if ':' in h:
                sep = h.index(':')
                key = h[:sep]
                val = h[sep+1:]
                if key == 'id':
                    header_dict[key] = int(val)
                else:
                    header_dict[key] = val
            else:
                continue
        return header_dict

    def write(self, text, header_dict):
        with open(self.path, 'w', encoding= 'utf-8') as f:
            for k, v in header_dict.items():
                line = str(k) + ':' + str(v) +os.linesep
                f.write(line)
            f.write(ENDHEADER)
            f.write(text)
        f.close()
