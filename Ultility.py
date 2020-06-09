import tldextract
import dateutil.parser as parseDate
from dateutil.relativedelta import relativedelta
import regex as re
import datetime

class Ultility:
    @staticmethod
    def extract_FQDN(FQDN):
        return tldextract.extract(str(FQDN))
    
    @staticmethod
    def is_after_end_date(beginTimestamp,endTimestamp):
        beginTime = parseDate.isoparse(beginTimestamp)
        endTime = parseDate.isoparse(endTimestamp)
        if (beginTime < endTime):
            return False
        else:
            return True
    
    @staticmethod
    def get_current_time():
        return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    
    @staticmethod
    def plus_time(minutesAdd,stringTimestamp):
        date = parseDate.isoparse(stringTimestamp)
        newDate = date + relativedelta(minutes=minutesAdd)
        return newDate.isoformat()
    
    @staticmethod
    def get_domain(FQDN):
        FQDNExtract = tldextract.extract(str(FQDN))
        return FQDNExtract.domain+"."+FQDNExtract.suffix
    
    @staticmethod
    def is_tunelling_get_tool_regex_analysis(queryRecord):
        subdomain = Ultility.extract_FQDN(queryRecord.FQDN).subdomain
        #List of know regex by tools
        regexs={"DNSCAT_BP":r"[A-Za-z0-9]{25,63}\.[A-Za-z0-9]{25,63}\.[A-Za-z0-9]{25,63}"}
        for attackTool in regexs.keys():
            if re.match(regexs[attackTool],subdomain):
                return True, attackTool
        return False, None
    
    @staticmethod
    def get_class_serverity(avarageRequestPerDomain,numberOfRequests):
        times = numberOfRequests / avarageRequestPerDomain
        if times >= 4.0:
            return "Severe"
        if times >= 3.0:
            return "High"
        if times >= 2.0:
            return "Elevated"
        if times >= 1.5:
            return "Guarded"
        else:
            return "Low"
        