from google.cloud import bigquery
import pandas_gbq
import pandas as pd
import seaborn as sns


import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="my_project.json"
client = bigquery.Client()
project_id = "winged-woods-214006"

query = (
    """
    SELECT visitId, fullVisitorId, visitNumber, date, visitStartTime, trafficSource, totals, channelGrouping, device,geoNetwork 
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
    WHERE _TABLE_SUFFIX BETWEEN '20160801' AND '20170801'
     """
)

df_original = pandas_gbq.read_gbq(query, project_id=project_id)

print("Unnesting Traffic Source")
df_ts = df_original.trafficSource.apply(pd.Series)
print("Unnesting adwordsClickInfo")
df_aci = df_ts.adwordsClickInfo.apply(pd.Series)
print("Unnesting totals")
df_totals = df_original.totals.apply(pd.Series)
print("Unnesting device")
df_device = df_original.device.apply(pd.Series)
print("Unnesting geoNetwork")
df_geo = df_original.geoNetwork.apply(pd.Series)


df = pd.concat([df_original, df_totals, df_ts, df_aci, df_device, df_geo], axis = 1)

df = df.drop(["adwordsClickInfo", "trafficSource", "totals", "device", "geoNetwork"], axis = 1)

coltodrop = []
for column in df:
    if len(df[column].value_counts())<=1:
        coltodrop.append(df[column].name)
    
df = df.drop(coltodrop, axis = 1)

df.to_csv("trafficSource_fullyear.csv")