from datetime import date
import os


class Header():
    def __init__(self, link, id, host, the_date=''):
        self.link = link
        self.id = id
        self.host = host
        if the_date == '':
            self.date = str(date.today())

    def writeToHtmlFile(self, file):
        for k, v in self.__dict__.items():
            line = str(k) + ':' + str(v) + os.linesep
            file.write(line)

    @classmethod
    def parseHeader(self, header_lines):
        header_dict = {}
        for h in header_lines:
            if ':' in h:
                sep = h.index(':')
                key = h[:sep]
                val = h[sep+1:].rstrip()
                if key == 'id':
                    header_dict[key] = int(val)
                else:
                    header_dict[key] = val
            else:
                continue
        return Header.fromDict(header_dict)

    @classmethod
    def fromDict(cls, hdict):
        return cls(hdict['link'], hdict['id'], hdict['host'], hdict['date'])
