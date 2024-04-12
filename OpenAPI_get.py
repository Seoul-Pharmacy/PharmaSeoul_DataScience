# Data
DataProcessing&amp;MachineLearning

import requests
import pprint
import json
url1="http://openapi.seoul.go.kr:8088/697865454c70687234314278716f6f/json/TbPharmacyOperateInfo/1/1000/"
url2="http://openapi.seoul.go.kr:8088/697865454c70687234314278716f6f/json/TbPharmacyOperateInfo/1001/2000/"
url3="http://openapi.seoul.go.kr:8088/697865454c70687234314278716f6f/json/TbPharmacyOperateInfo/2001/3000/"
url4="http://openapi.seoul.go.kr:8088/697865454c70687234314278716f6f/json/TbPharmacyOperateInfo/3001/4000/"
url5="http://openapi.seoul.go.kr:8088/697865454c70687234314278716f6f/json/TbPharmacyOperateInfo/4001/5000/"
url6="http://openapi.seoul.go.kr:8088/697865454c70687234314278716f6f/json/TbPharmacyOperateInfo/5001/5894/"

response1=requests.get(url1)
contents1=response1.text
json_ob1=json.loads(contents1)

response2=requests.get(url2)
contents2=response2.text
json_ob2=json.loads(contents2)

response3=requests.get(url3)
contents3=response3.text
json_ob3=json.loads(contents3)

response4=requests.get(url4)
contents4=response4.text
json_ob4=json.loads(contents4)

response5=requests.get(url5)
contents5=response5.text
json_ob5=json.loads(contents5)

response6=requests.get(url6)
contents6=response6.text
json_ob6=json.loads(contents6)

body1=json_ob1['TbPharmacyOperateInfo']['row']
body2=json_ob2['TbPharmacyOperateInfo']['row']
body3=json_ob3['TbPharmacyOperateInfo']['row']
body4=json_ob4['TbPharmacyOperateInfo']['row']
body5=json_ob5['TbPharmacyOperateInfo']['row']
body6=json_ob6['TbPharmacyOperateInfo']['row']

import pandas as pd
import numpy as np
ph_df1=pd.json_normalize(body1)
ph_df2=pd.json_normalize(body2)
ph_df3=pd.json_normalize(body3)
ph_df4=pd.json_normalize(body4)
ph_df5=pd.json_normalize(body5)
ph_df6=pd.json_normalize(body6)

ph_df=pd.concat([ph_df1,ph_df2,ph_df3,ph_df4,ph_df5,ph_df6], ignore_index=True)
#print(ph_df.columns)
#print(ph_df)

name=['HPID', 'DUTYADDR', 'DUTYNAME', 'DUTYTEL1', 'DUTYTIME1C', 'DUTYTIME2C',
       'DUTYTIME3C', 'DUTYTIME4C', 'DUTYTIME5C', 'DUTYTIME6C', 'DUTYTIME7C',
       'DUTYTIME8C', 'DUTYTIME1S', 'DUTYTIME2S', 'DUTYTIME3S', 'DUTYTIME4S',
       'DUTYTIME5S', 'DUTYTIME6S', 'DUTYTIME7S', 'DUTYTIME8S', 'POSTCDN1',
       'POSTCDN2', 'WGS84LON', 'WGS84LAT', 'WORK_DTTM']

for i in name:
    globals()["{}".format(i)]=ph_df[i].to_numpy()
