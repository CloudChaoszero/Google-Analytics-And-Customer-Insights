'''
Func: string_cleaning
Input: Raw String

Description: Remove certain string values and parse 
string to an array through delimiter ","
'''
def string_cleaning(rawString):
    convertedString = rawString.replace("\"","")\
                        .replace("\'","")\
                        .replace("{","")\
                        .replace("}","")\
                        .split(',')
    return(convertedString)

'''
Func: geographic_parse
Input: Raw String

Description: Parse Geographic information
'''
def geographic_parse(rawString):
    convertStr = string_cleaning(rawString)
    return(convertStr[0], convertStr[1])

'''
Func: sessionInput
Input: Raw String

Description: Obtain session information
and if none, then impute 0 value.
'''

def sessionInput(string):
    stringFormatted = 0
    try:
        stringFormatted = int(string[5].split(":")[1])
    
    except:
        stringFormatted = 0
    return 0


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
        
def trafficSource_cleaning(trafficString):
    trafficList_cleaned = string_cleaning(trafficString)
    trafficHash = {}
    for keyVal in trafficList_cleaned[:-1]:
        parsedItems= keyVal.split(":")
        if len(parsedItems) > 1:
            trafficHash[parsedItems[0]] = parsedItems[1]
        else:
            trafficHash["N/A"] = "(not set)"

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



def hit_productPrice_agg(raw_hit_string):
    
    #Modify String to remove ', True", and d's items
    modifiedString = raw_hit_string.replace("'", '"').replace(\
                            "True","\"True\"").replace(\
                            "d\"s","ds")
    
    # Partition Modified string into array by ',' delim
    modifiedStringArray = modifiedString.split(",")

#    # Obtain all Product Name occurences from hit record
#     productNames = [i.replace("\"","") for i in modifiedStringArray if i.find("v2ProductName") != -1]
    
    # Obtain all Pricing occurences from hit record, respective 
    # from the above productNames list.
    # Note: Exclude first blank value in string
    productPrices = [i.replace("\"","")[1:] for i in modifiedStringArray if i.find("productPrice") != -1]

    # Obtain the value/100000 from key-pair value in each row
    productSum_estimated = [int(i.split(":")[1])/100000 for i in productPrices]

    # Sum expected total Order Value from Cart.
    estimatedAggTotal = sum(productSum_estimated)
    return(estimatedAggTotal)