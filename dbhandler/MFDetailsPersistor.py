from pymongo import MongoClient
import datetime

connection = MongoClient('localhost', 27017)
db = connection.mfhack
collection = db.mflayer1


def transform(_mf_object):
    print "Inserting for ::", _mf_object.name
    _mf_object.timestamp = datetime.datetime.now().utcnow()
    try:
        collection.insert(_mf_object.__dict__)

    except Exception as e:
        print "Exception -->", type(e), e


def transformAndInsert(_mf_object):
    transform(_mf_object)
