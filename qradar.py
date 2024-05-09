import requests, json, sys
from log import log

requests.packages.urllib3.disable_warnings()

class Qradar():
    def __init__(self, config) -> None:
        self.logger = log()
        self.config = config

        self.URL = config['qradar']['url']

        self.headers = {
                'Version': '12.0',
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'SEC': self.config['qradar']['apiKey']
            }

    def getLogSourceTypeId(self, name):
        '''Get log source type ID by name'''
        params = {'filter': f'name = \"{name}\"'}
        
        URI = f'/config/event_sources/log_source_management/log_source_types'

        response = requests.get(url=self.URL+URI, headers=self.headers, params=params, verify=False)
        self.logger.debug(response.json())
        return response.json()[0]['id']
        
    def getQidByName(self, name):
        '''Get qid by name'''

        params = {'filter': f'name = \"{name}\"'}
        
        URI = f'/data_classification/qid_records'

        response = requests.get(url=self.URL+URI, headers=self.headers, params=params, verify=False)
        self.logger.debug(response.json())
        if response.status_code == 200:
            return response.json()
        else:
            print(response.text)
            sys.exit(1)

    def createQid(self, line):
        '''Creatig QID '''
        URI = '/data_classification/qid_records'
        data = {
            "log_source_type_id": self.getLogSourceTypeId(self.config['dsm']['logSourceTypeName']),
            "name": line[self.config['qid']['qidName']],
            "description": line[self.config['qid']['qidDesc']],
            "severity": int(self.config['qid']['qidSev']),
            "low_level_category_id": int(self.config['qid']['qidLLC']) #Misc
        }
        response = requests.post(url=self.URL+URI, headers=self.headers, data=json.dumps(data), verify=False)
        self.logger.debug(response.json())
        return response.json()

    def assignToDSM(self, line, qid):
        '''Assign qid to DSM'''
        URI = '/data_classification/dsm_event_mappings'
        data = {
            "log_source_type_id": self.getLogSourceTypeId(self.config['dsm']['logSourceTypeName']), 
            "log_source_event_id": str(line[self.config['dsm']['eventId']]), 
            "log_source_event_category": line[self.config['dsm']['eventCategory']],
            "qid_record_id": qid['id'],
        }
        response = requests.post(url=self.URL+URI, headers=self.headers, data=json.dumps(data), verify=False)
        self.logger.debug(response.json())
        return response.json()