
#Organize data 
class DomainStatistic:
    
    def __init__(self,domain,IPs,beginTimestamp,numberOfRequests):
        self.domain = domain
        #This is a set to prevent duplicate IPs
        self.IPs = IPs
        self.beginTimestamp = beginTimestamp
        self.numberOfRequests = numberOfRequests