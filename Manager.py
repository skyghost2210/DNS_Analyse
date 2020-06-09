#Query all data in array format (Object DNS Query Record)
#Regex Analysis
#Convert to JSON
#Move to Elastic
#Traffic Ananlysis
#Cpnvert to JSON
#Move to Elastic

from Ultility import Ultility
from DNSQueryRecord import DNSQueryRecord
from DomainStatistic import DomainStatistic
from Report import RegexReport,TrafficReport
from ConnectElastic import ConnectElastic

class Manager():

    def regex_analysis(self,queryRecords):
        #request per domain = {"domainA":[domainStatistic,toolName]}
        domainsStatistics ={}
        
        #Loop through every Records
        for queryRecord in queryRecords:
            
            analysisResult = Ultility.is_tunelling_get_tool_regex_analysis(queryRecord)
            
            #Check if this domain is tunneling
            if analysisResult[0]:
                
                #Get the root domain from FQDN
                domain = Ultility.get_domain(queryRecord.FQDN)
                
                #Check if this domain already in dictionary
                if domain not in domainsStatistics:
                    domainsStatistics[domain] = [DomainStatistic(domain,{queryRecord.IP},queryRecord.timestamp,1),analysisResult[1]]
                else:
                    #Add IP request to set (UNIQUE)
                    domainsStatistics[domain][0].IPs.add(queryRecord.IP)
                    
        reports = []
        
        for domainStatistic in domainsStatistics.values():
            reports.append(
                RegexReport(domainStatistic[0],"Severe",domainStatistic[1]))
            
        return reports
    
    def traffic_analysis(self,queryRecords):
        #request per domain = {"domainA":{ips:[ip1,ip2,ip3,ip4], begin_timestamp=''}
        domainsStatistics ={}
        
        #Total number of request
        totalNumberOfRequests = 0

        #Loop through every Records
        for queryRecord in queryRecords:
            #Get the root domain from FQDN
            domain = Ultility.get_domain(queryRecord.FQDN)
            
            #Check if this domain already in dictionary
            if domain not in domainsStatistics:
                domainsStatistics[domain] = DomainStatistic(domain,{queryRecord.IP},queryRecord.timestamp,1)
            else:
                #Add IP request to set (UNIQUE)
                domainsStatistics[domain].IPs.add(queryRecord.IP)
                #Plus 1 to total
                domainsStatistics[domain].numberOfRequests += 1
                
            #Update the total
            totalNumberOfRequests += 1
        
        #Calulate the avarage request per domain
        avarageRequestsPerDomains = totalNumberOfRequests / len(domainsStatistics)
        
        reports = []
        
        for domainStatistic in domainsStatistics.values():
            if domainStatistic.numberOfRequests > avarageRequestsPerDomains:
                reports.append(
                    TrafficReport(domainStatistic,Ultility.get_class_serverity(
                        avarageRequestsPerDomains,domainStatistic.numberOfRequests)))
        
        return reports
    
    def convert_to_JSON_send_elasticsearch(self,reports,elsaticConnection,isTrafficAnalysis):
        JSONReports = []
        for report in reports:
            JSONReports.append(report.JSON_report())
        elsaticConnection.send_analysis_result(JSONReports,isTrafficAnalysis)