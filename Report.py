from DomainStatistic import DomainStatistic

class RegexReport (DomainStatistic):
    
    def __init__(self,DomainStatistic,level,toolName):
        #Inheritance parent Class
        super().__init__(DomainStatistic.domain,DomainStatistic.IPs
                         ,DomainStatistic.beginTimestamp,DomainStatistic.numberOfRequests)
        self.toolName = toolName
        self.level = level
        
        
    def JSON_report(self):
        return {"domain":self.domain,
                "ip_s":list(self.IPs),
                "@timestamp":self.beginTimestamp,
                "tool":self.toolName,
                "level":self.level}
        
class TrafficReport (DomainStatistic):
    
    def __init__(self,DomainStatistic,level):
        #Inheritance parent Class
        super().__init__(DomainStatistic.domain,DomainStatistic.IPs
                         ,DomainStatistic.beginTimestamp,DomainStatistic.numberOfRequests)
        self.level = level
        
    def JSON_report(self):
        return {"domain":self.domain,
                "ip_s":list(self.IPs),
                "@timestamp":self.beginTimestamp,
                "request_numbers":self.numberOfRequests,
                "level":self.level}