from datetime import datetime
from elasticsearch7 import Elasticsearch,helpers,exceptions
from DNSQueryRecord import DNSQueryRecord
from Ultility import Ultility

class ConnectElastic:
    def __init__(self,host,port,indexName,beginTimestamp,endTimesstamp,regexIndexName,trafficIndexName):
        self.host = host
        self.port = port
        self.indexName = indexName
        self.beginTimestamp = beginTimestamp
        self.endTimestamp = endTimesstamp
        self.regexIndexName = regexIndexName
        self.trafficIndexName = trafficIndexName
        
    def estabilshed_connection(self):
        return Elasticsearch([{'host': self.host, 'port': self.port}])
    
    def get_DNS_Records(self):
        esConnection = self.estabilshed_connection()
        DNSRecords = helpers.scan(esConnection,index=self.indexName,preserve_order=False,    
                   query={"query": {
                       "range": {
                           "@timestamp":{
                               #Example: 2020-06-05T06:55:54.061Z
                               "gte":self.beginTimestamp,
                               "lt":self.endTimestamp
                               }}}})
        DNSQueryRecords = []
        for record in enumerate(DNSRecords):
            DNSQueryData = record[1]['_source']
            try:
                #Prevent '_jsonparsefailure'
                DNSQueryData['_tags']
                print(record)
                continue
            except Exception:
                #Process Here (TO Object QueryRecord)
                timestamp = DNSQueryData['@timestamp']
                IP = DNSQueryData['client_ip']
                FQDN = DNSQueryData['qname']
                DNSQueryRecords.append(DNSQueryRecord(timestamp = timestamp,IP = IP,FQDN = FQDN))
            
        return DNSQueryRecords
    
    def send_analysis_result(self,JSONReports,isTrafficAnalysis):
        esConnection = self.estabilshed_connection()
        indexName = self.regexIndexName
        if isTrafficAnalysis == True:
            indexName = self.trafficIndexName
        for JSONReport in JSONReports:
            esConnection.index(index=indexName,body=JSONReport)