from pymongo import MongoClient
from pprint import pprint
import pandas as pd
import numpy as np

class myClass():
    db = 0
    def __init__(self):
        print("Object has been initialized.")

    def initializeNewDatabase(self, url):
        client = MongoClient(url)
        self.db = client.domains
        self.loadDataFromCSV(self.db)


    def runExistingDatabase(self, url):
        client = MongoClient(url)
        self.db = client.domains

    def loadDataFromCSV(self, db):
        df_1 = pd.read_csv('politifact_fake.csv')
        df_2 = pd.read_csv('gossipcop_fake.csv')
        self.convertDFtoDocument(df_1, db)
        self.convertDFtoDocument(df_2, db)

    def convertDFtoDocument(self, df, db):
        for x in range(0, len(df)):
            try:
                assert df.loc[x, 'news_url'] != np.nan
                assert isinstance(df.loc[x, 'news_url'], str)
            except:
                #print("Exception - no value found.")
                continue
            fakeDomain = self.findDomain(df.loc[x, 'news_url'])
            domains = {
                'domain': fakeDomain,
                'rating': 2
            }
            #print(fakeDomain)
            result = db.reviews.insert_one(domains)

    def findDomain(self, testString):
        testString = testString.replace("https://www.", "")
        testString = testString.replace("http://www.", "")
        testString = testString.replace("https://", "")
        testString = testString.replace("http://", "")
        domena = testString.split("/")[0]
        return domena

    def findOne(self, domainToSearch):
        result = self.db.reviews.find_one({'domain': domainToSearch})
        if result is None:
            #pprint(result)
            return 0
        else:
            #pprint(result)
            return 1

    def insertMany(self, domainsToInsert):
        domainsToInsert_splitted = domainsToInsert.split(';')
        df = pd.DataFrame(domainsToInsert_splitted)
        self.convertDFtoDocument(df, self.db)


def main():
    flag = 1
    obj = myClass()
    while (flag):
        print(
            "Script has been started. Type 'create' to initialize new database with data from .csv files or 'start' to load existing database.")
        choice = input()
        if choice == "create":
            print("Create new database chosen.")
            print("Paste MongoDB URL: ")
            # ..........................
            url = "mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb"
            flag = 0
            i = 1
            while (i < 20):
                obj.initializeNewDatabase(url)
                i += 1

            break
        if choice == "start":
            print("Start existing database.")
            print("Paste MongoDB URL: ")
            # ..........................
            url = "mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb"
            flag = 0
            obj.runExistingDatabase(url)
            break
        else:
            print("Unknown command.")

    obj.insertMany("wikipedia.org;youtube.com")
    if obj.findOne("dziwne.com"):
         print("Site found in database.")
    else:
        print("Site not found in database.")

if __name__ == '__main__':
    main()
