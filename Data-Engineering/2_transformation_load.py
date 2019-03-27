import warnings
warnings.filterwarnings("ignore")

import pandas as pd


parse_dates = ['date']
ga_trainDf = pd.read_csv('../Resources/Data/ZipFiles/train_v2.csv.zip',\
                            compression='zip',nrows=100000, parse_dates=parse_dates,
                        skiprows=lambda i: i % 10 != 0)



def string_cleaning(rawString):
    convertedString = rawString.replace("\"","")\
                        .replace("\'","")\
                        .replace("{","")\
                        .replace("}","")\
                        .split(',')
    return(convertedString)

def geographic_parse(rawString):
    convertStr = string_cleaning(rawString)
    return(convertStr[0], convertStr[1])
# ga_trainDf['geoNetwork'][0].replace("\"","").replace("\'","").replace("{","").replace("}","").split(',')
ga_trainDf['geoNetwork_new'] = ga_trainDf['geoNetwork'].transform(geographic_parse)
ga_trainDf['Continent'] = ga_trainDf['geoNetwork_new'].transform(lambda x: x[0].split(":")[1])
ga_trainDf['Sub-Continent'] = ga_trainDf['geoNetwork_new'].transform(lambda x: x[1].split(":")[1])


def sessionInput(string):
    stringFormatted = 0
    try:
        stringFormatted = int(string[5].split(":")[1])
    
    except:
        stringFormatted = 0
    return 0


ga_trainDf['totals_new'] = ga_trainDf['totals'].apply(string_cleaning)


'''
marketing_metrics_parser
Param 1: metricsArray
Param 2; index

Impute 0 value for missing marketing metrics from
original dictionary or list (e.g. A returned row 
would have visits and hits, but no pageviews data
--thus hitting and error)
'''
def marketing_metrics_parser(metricsArray, index):
    try:
        return(metricsArray[index].split(":")[1])
    except:
        return(0)
        

##Segment: visits,hits, pageviews, bounces, newVisits, sessionQualityDim
ga_trainDf['visits'] = ga_trainDf['totals_new'].apply(marketing_metrics_parser,index=(0))
ga_trainDf['hits'] = ga_trainDf['totals_new'].transform(marketing_metrics_parser,index=(1)) 
ga_trainDf['pageviews'] = ga_trainDf['totals_new'].transform(marketing_metrics_parser,index=(2))
ga_trainDf['bounces'] = ga_trainDf['totals_new'].transform(marketing_metrics_parser,index=(3)) 
ga_trainDf['newVisits'] = ga_trainDf['totals_new'].transform(marketing_metrics_parser,index=(4))
ga_trainDf['sessionQualityDim'] = ga_trainDf['totals_new'].transform(sessionInput)


ga_trainDf['deviceType'] = ga_trainDf['device'].apply(\
                    lambda x: x.split(',')[0][13:-1])


ga_trainDf['Region'] = ga_trainDf.customDimensions.apply(\
                                        lambda x: x[x.find('\'value\':')+10:-3])


def trafficSource_cleaning(trafficString):
    trafficList_cleaned = string_cleaning(trafficString)
    trafficHash = {}
    for keyVal in trafficList_cleaned[:-1]:
        parsedItems= keyVal.split(":")
        trafficHash[parsedItems[0]] = parsedItems[1]
    hasKeyList = list(trafficHash.keys())
    if "campaign" not in hasKeyList:
        trafficHash["campaign"] = "(not set)"
    if "referralPath" not in hasKeyList:
        trafficHash["referralPath"] = "(not set)"
    if "source" not in hasKeyList:
        trafficHash["source"] = "(not set)"
    if "medium" not in hasKeyList:
        trafficHash["medium"] = "(not set)"
    if "keyword" not in hasKeyList:
        trafficHash["keyword"] = "(not set)"
    if "adwordsClickInfo" not in hasKeyList:
        trafficHash["adwordsClickInfo"] = "(not set)"
    return(trafficHash)
        
    '''for all key pairs being mapped in hash, if one a key is not in a list, then input values'''
    '''from that hash, we then create columns our of each key-value pair'''
    
ga_trainDf['trafficSource'][:10].transform(lambda x: trafficSource_cleaning(x)["source"])


ga_trainDf.drop(['customDimensions','device','geoNetwork','geoNetwork_new','totals','trafficSource','totals_new'], axis = 1, inplace=True)

toCsvPath = os.path.join()
ga_trainDf.to_csv(path_or_buf='', index=False)
'''

['channelGrouping',
 'customDimensions',
 'date',
 'device',
 'fullVisitorId',
 'geoNetwork',
 'hits',
 'socialEngagementType',
 'totals',
 'trafficSource',
 'visitId',
 'visitNumber',
 'visitStartTime',
 'geoNetwork_new',
 'Continent',
 'Sub-Continent',
 'totals_new',
 'visits',
 'pageviews',
 'bounces',
 'newVisits',
 'sessionQualityDim',
 'deviceType',
 'Region']
'''