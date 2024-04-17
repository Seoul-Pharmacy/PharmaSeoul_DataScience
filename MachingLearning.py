!pip install haversine

from sklearn.neighbors import KNeighborsRegressor
from haversine import haversine

#사용자의 위도, 경도를 통해 datas에서 사용자와 가장 가까운 약국의 정보를 가진 딕셔너리 5개와 해당 딕셔너리에 거리를 추가하여 return.
def get_pharmacy(datas, user_latitude, user_longitude):
    
    filtered_longitude=[]
    filtered_latitude=[]
    datas_results=[]

    for i in range(len(datas)):
        filtered_longitude.append(float(datas[i]['longitude']))
        filtered_latitude.append(float(datas[i]['latitude']))
    filtered_longitude_array=np.array(filtered_longitude)
    filtered_latitude_array=np.array(filtered_latitude)

    kn=KNeighborsRegressor()

    kn.fit(filtered_latitude_array.reshape(-1,1), filtered_longitude_array.reshape(-1,1))
    distances, indexes=kn.kneighbors([user_latitude])
  
    for i in indexes[0]:
        datas_results.append(datas[i])
    
    for i in indexes[0]:
        datas[i]["distance"]=(str(haversine((float(user_latitude[0]), float(user_longitude[0])),(float(datas[i]['latitude']),float(datas[i]['longitude']))))+"km")

    return datas_results
