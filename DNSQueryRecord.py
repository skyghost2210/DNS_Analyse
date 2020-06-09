import tldextract

#Convert JSON to a readable Object
class DNSQueryRecord:
    def __init__(self,timestamp,IP,FQDN):
        self.timestamp=timestamp
        self.IP=IP
        self.FQDN=FQDN