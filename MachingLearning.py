from sklearn.neighbors import KNeighborsClassifier
kn=KNeighborsClassifier()
kn.fit(WGS84LON, WGS84LAT) #드롭다운 된 경도, 위도를 가져와야 합니다.
user=[경도, 위도] #사용자의 경도, 위도입니다.
kn.predict([new]) 
distances, indexes=kn.neighbors([new])

for i in indexes:
  print(DUTYNAME[i], DUTYADDR[i], distances[i]) #사용자 주변 5개의 약국 이름, 약국 주소, 거리(단위 변환 필요)를 출력합니다.
