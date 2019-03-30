import os
import warnings
warnings.filterwarnings("ignore")

import pandas as pd

from misc_functions import string_cleaning, geographic_parse, sessionInput
from misc_functions import marketing_metrics_parser,trafficSource_cleaning,\
                           hit_productPrice_agg


#Import First 100,000 datapoints from .zip file
parse_dates = ['date']
ga_trainDf = pd.read_csv('../Resources/Data/ZipFiles/train_v2.csv.zip',
                        compression='zip',nrows=100000, 
                        parse_dates=parse_dates,
                        skiprows=lambda i: i % 10 != 0)


#Create transformed Geo and Continent Columns

ga_trainDf['geoNetwork_new'] = ga_trainDf['geoNetwork'].transform(geographic_parse)

ga_trainDf['Continent'] = ga_trainDf['geoNetwork_new'].transform(\
                                  lambda x: x[0].split(":")[1])
ga_trainDf['Sub-Continent'] = ga_trainDf['geoNetwork_new'].transform(\
                                  lambda x: x[1].split(":")[1])


# Create transformed Totals Column
ga_trainDf['totals_new'] = ga_trainDf['totals'].apply(string_cleaning)

# Obtain Estimated Cart Total from "hits" nested column.
ga_trainDf['estimatedCartTotal'] = ga_trainDf["hits"].apply(hit_productPrice_agg)

# Segment: visits,hits, pageviews, bounces, newVisits, sessionQualityDim
ga_trainDf['visits'] = ga_trainDf['totals_new'].apply(marketing_metrics_parser,index=(0))

ga_trainDf['hits'] = ga_trainDf['totals_new'].transform(marketing_metrics_parser,index=(1)) 
ga_trainDf['pageviews'] = ga_trainDf['totals_new'].transform(marketing_metrics_parser,index=(2))
ga_trainDf['bounces'] = ga_trainDf['totals_new'].transform(marketing_metrics_parser,index=(3)) 
ga_trainDf['newVisits'] = ga_trainDf['totals_new'].transform(marketing_metrics_parser,index=(4))
ga_trainDf['sessionQualityDim'] = ga_trainDf['totals_new'].transform(sessionInput)


# Extract Device Type information
ga_trainDf['deviceType'] = ga_trainDf['device'].apply(\
                    lambda x: x.split(',')[0][13:-1])


# Extract Region Type information
ga_trainDf['Region'] = ga_trainDf.customDimensions.apply(\
                                        lambda x: x[x.find('\'value\':')+10:-3])


# Parse Traffice Source information    
ga_trainDf['trafficSource'] = ga_trainDf['trafficSource'].transform(\
                                      lambda x: trafficSource_cleaning(x)["source"])

#Drop misc. columns for targeted data export
dropColumnsList = ['customDimensions','device','geoNetwork',
                   'geoNetwork_new','totals','trafficSource',
                   'totals_new']


ga_trainDf.drop(dropColumnsList, 
                axis = 1, 
                inplace=True)

# Export transformed information to CSV
toCsvPath = os.path.join('..', 'Resources','Data',
                         'PreparedData','ga_analytics_filtered_dataset.csv')
ga_trainDf.to_csv(path_or_buf=toCsvPath, index=False)


