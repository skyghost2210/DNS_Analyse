import json

class Configuration():
    
    def __init__(self):
        data = self.get_JSON_config()
        self.host = data['Host']
        self.port = data['Port']
        self.indexName =  data['IndexName']
        self.beginTimestamp = data['BeginTimestamp']
        self.regexIndexName = data['RegexIndexName']
        self.trafficIndexName = data['TrafficIndexName']
        self.timeRange = data['TimeRange']
        
    def get_JSON_config(self):
        with open("configuration.json", "r") as json_data_file:
            data = json.load(json_data_file)
        return data
    
    def parse_JSON_config(self):
        data = {
            "Host" : self.host,
            "Port" : self.port,
            "BeginTimestamp" : self.beginTimestamp,
            "IndexName" : self.indexName,
            "RegexIndexName" : self.regexIndexName,
            "TrafficIndexName" : self.trafficIndexName,
            "TimeRange" : self.timeRange
        }
        with open("configuration.json", "w") as outfile:
            json.dump(data, outfile ,sort_keys=True, indent=2, separators=(',', ': '))
