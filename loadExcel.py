import pandas as pd
from log import log
import sys

class Data():
    def __init__(self, config) -> None:
        self.config = config
        self.type = config['file']['type']

    def getFileData(self):
        '''Get template excel data'''
        filename = self.config['file']['filename']

        pd.set_option('display.max_colwidth', None) #Remove text size limitation from a cell
        
        if self.type == 'csv':
            df = pd.read_csv(filename)
        elif self.type == 'xlsx':
            df = pd.read_excel(filename)
        else:
            raise TypeError
        
        columns = self.config['file']['columns'].split()
        columnsDf = df[columns]

        assert 'unnamed' not in str(columnsDf.head(1)).lower()
        print("Excel parsed preview")
        print("######################################")
        print(columnsDf.head(3))
        resp = int(input('Do you want to proceed with information above? \
                        \n1 - Yes\
                        \n2 - No\
                        \nAnswer: '))
        if resp != 1:
            sys.exit(1)

        return columnsDf.to_dict('records')
