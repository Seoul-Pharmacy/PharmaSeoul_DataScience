#열 단위 데이터 형성의 전체 과정입니다.
#1. OpenAPI로 약국 위치 정보 데이터를 가져와 데이터 프레임으로 만들기
#2. 외국어 가능 약국 데이터를 다운 받아 데이터 프레임으로 만들기
#3. 약국 위치 정보와 외국어 가능 약국의 데이터프레임을 합치고 중복 행 제거하기
#4. 데이터프레임을 열 단위로 나누기(생략 가능)
#5. 주소를 시, 구, 도로명 단위로 만들어 데이터프레임에 추가



#1
#OpenAPI 데이터 가져오기
import requests
import pprint
import json
import pandas as pd
import numpy as np
url1="http://openapi.seoul.go.kr:8088/보안키/json/TbPharmacyOperateInfo/1/1000/"
url2="http://openapi.seoul.go.kr:8088/보안키/json/TbPharmacyOperateInfo/1001/2000/"
url3="http://openapi.seoul.go.kr:8088/보안키/json/TbPharmacyOperateInfo/2001/3000/"
url4="http://openapi.seoul.go.kr:8088/보안키/json/TbPharmacyOperateInfo/3001/4000/"
url5="http://openapi.seoul.go.kr:8088/보안키/json/TbPharmacyOperateInfo/4001/5000/"
url6="http://openapi.seoul.go.kr:8088/보안키/json/TbPharmacyOperateInfo/5001/5894/"

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

#OpenAPI 데이터를 데이터 프레임으로 변경
ph_df1=pd.json_normalize(body1)
ph_df2=pd.json_normalize(body2)
ph_df3=pd.json_normalize(body3)
ph_df4=pd.json_normalize(body4)
ph_df5=pd.json_normalize(body5)
ph_df6=pd.json_normalize(body6)

ph_df=pd.concat([ph_df1,ph_df2,ph_df3,ph_df4,ph_df5,ph_df6], ignore_index=True)
print(ph_df.columns)


#2
#외국어 가능 약국 데이터 가져와 데이터 프레임으로 변형
Fph_df=pd.read_excel("/content/외국어 가능 약국 현황.xlsx", header=2) #저장소 위치가 같아야 합니다.
Fph_df.drop([0], axis=0, inplace=True)
Fph_df=Fph_df.rename(columns={'약국이름':'DUTYNAME','주소 (도로명)': 'DUTYADDR', '전화번호':'DUTYTEL1','가능 외국어':'외국어가능','Unnamed: 6': 'English','Unnamed: 7': 'Chinese', 'Unnamed: 8':'Japanese'})


#3
#데이터 프레임 합치기
Pharmacy_df=pd.concat([ph_df,Fph_df],ignore_index=True)

#데이터 프레임 중복 제거
Pharmacy_df=Pharmacy_df.drop_duplicates(subset=['DUTYTEL1'],keep=False)

#자치구 열 삭제
Pharmacy_df=Pharmacy_df.drop('자치구', axis=1)

#위도, 경도 외 Nan을 False로 변경
Pharmacy_df.fillna(False, inplace=True)
Pharmacy_df['WGS84LON'].replace(False, np.NaN, inplace=True)
Pharmacy_df['WGS84LAT'].replace(False, np.NaN, inplace=True)

print(Pharmacy_df)


#4(생략 가능)
#데이터 프레임을 열 단위로 나누기
name=['HPID', 'DUTYADDR', 'DUTYNAME', 'DUTYTEL1', 'DUTYTIME1C', 'DUTYTIME2C',
       'DUTYTIME3C', 'DUTYTIME4C', 'DUTYTIME5C', 'DUTYTIME6C', 'DUTYTIME7C',
       'DUTYTIME8C', 'DUTYTIME1S', 'DUTYTIME2S', 'DUTYTIME3S', 'DUTYTIME4S',
       'DUTYTIME5S', 'DUTYTIME6S', 'DUTYTIME7S', 'DUTYTIME8S', 'POSTCDN1',
       'POSTCDN2', 'WGS84LON', 'WGS84LAT', 'WORK_DTTM', '연번', '자치구', '외국어가능',
       'English', 'Chinese', 'Japanese', '비고']

for i in name:
    globals()["{}".format(i)]=Pharmacy_df[i].to_numpy()


#5
#DUTYADDR -> 시, 구 ,도로명으로 파싱
DUTYADDR_tokened=[]
시=[]
구=[]
도로명=[]
for i in range(0,5214):
    DUTYADDR_tokened+=DUTYADDR[i].split(' ',maxsplit=2)
    시.append(DUTYADDR_tokened[0+(i-1)*3])
    구.append(DUTYADDR_tokened[1+(i-1)*3])
    도로명.append(DUTYADDR_tokened[2+(i-1)*3])

#시, 구, 도로명 정보를 dataframe에 추가
Pharmacy_df['시']=시
Pharmacy_df['구']=구
Pharmacy_df['도로명']=도로명

print(Pharmacy_df.columns)
