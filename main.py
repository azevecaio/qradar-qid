import qradar
import loadExcel
import configparser
import sys
from log import log
import os

#Load and parsing config.ini
dirname = os.path.dirname(__file__)
configFile = os.path.join(dirname, 'config.ini')
config = configparser.ConfigParser()
config.read(configFile)

#Start logging
logger = log()

#Get qradar.py class
q = qradar.Qradar(config)

#Reading and parsing excel data
logger.info('Reading excel fields')
data = loadExcel.Data(config)
lines = data.getFileData()

#For each eventid/eventcategory create qid and assign to dsm
for line in lines:
    qidName = line[config['qid']['qidName']].strip()
    logger.info({'message': f'getting qid - {qidName}'})

    qid = q.getQidByName(qidName)
    logger.debug({'message': {f'{qid}'}})

    #Creating QID if doesn't exist
    if not qid: #if qid does not exist
        logger.info({'message': f'creating qid - {qidName}'})

        qid = q.createQid(line)
        qid = qid
    #Skip QID creation
    else:
        logger.info({'message': f'qid - {qidName} - already exist'})
        qid = qid[0]

    #Assign QID to eventId and eventCategory
    logger.info({'message': f'assign qid - {qidName} - to dsm'})

    response = q.assignToDSM(line, qid)
    logger.info(f'{response}')