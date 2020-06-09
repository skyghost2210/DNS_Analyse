from ConnectElastic import ConnectElastic
from Manager import Manager
from Ultility import Ultility
from Configuration import Configuration


configData = Configuration()
#Get data from config file
elasticBeginTimesstamp = configData.beginTimestamp
currentTimestamp = Ultility.get_current_time()

while not Ultility.is_after_end_date(elasticBeginTimesstamp,currentTimestamp):
    #Create Objects
    manager = Manager()
    #Connect to Elastic Search
    esConnect = ConnectElastic(host=configData.host,port=configData.port,indexName=configData.indexName,beginTimestamp=elasticBeginTimesstamp,endTimesstamp = Ultility.plus_time(configData.timeRange,elasticBeginTimesstamp),
                           regexIndexName=configData.regexIndexName,trafficIndexName=configData.trafficIndexName)

    #Update timestamp
    elasticBeginTimesstamp = Ultility.plus_time(10,elasticBeginTimesstamp)

    #Get query records
    queryRecords = esConnect.get_DNS_Records()
    print(len(queryRecords))
    #Check if there is any records
    if len(queryRecords) > 1:
        #Traffic Analysis
        trafficReports = manager.traffic_analysis(queryRecords=queryRecords)
        #Send back to Elastic
        manager.convert_to_JSON_send_elasticsearch(reports=trafficReports,elsaticConnection=esConnect,isTrafficAnalysis=True)
        #Regex Analysis
        regexReports = manager.regex_analysis(queryRecords=queryRecords)
        #Send back to Elastic
        #manager.convert_to_JSON_send_elasticsearch(reports=regexReports,elsaticConnection=esConnect,isTrafficAnalysis=False)
        
#Update config file
configData.beginTimestamp = currentTimestamp
configData.parse_JSON_config()
