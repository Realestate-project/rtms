import pandas as pd
import folium
from folium.plugins import MarkerCluster
from folium.features import CustomIcon

# for key, value in rental_opi.iterrows():
#     folium.Marker([value['위도'], value['경도']], tooltip=value['건물명'],
#                   icon=folium.Icon(color='red', icon='glyphicon glyphicon-home')).add_to(map)

rental_offi=pd.read_csv('data/전월세_오피스텔__중복제거.csv', encoding='cp949')
# rental_offi

m = folium.Map(location=[37.566345, 126.977893], zoom_start=16)
# m.save('cityhall.html')
# m

# icon_image1='static/부엉이_1.png'
# icon1 = folium.features.CustomIcon('static/부엉이_1.png', icon_size=(180, 228))
#
# for key,value in rental_offi.iterrows():
#     icon1 = folium.features.CustomIcon('static/부엉이_1.png', icon_size=(180, 228))    # 휘발성!!!!!!!!!!!!11
#     folium.Marker([value['위도'], value['경도']], tooltip=value['건물명'], icon=icon1).add_to(m)
# # m
# # m.save('offi.html')
#
# m_2=folium.Map(location=[37.566345, 126.977893], zoom_start=12)
# marker_cluster = MarkerCluster().add_to(m_2)
# for key,value in rental_offi.iterrows():
#     icon1 = folium.features.CustomIcon('static/부엉이_1.png', icon_size=(180, 228))    # 휘발성!!!!!!!!!!!!11
#     folium.Marker([value['위도'], value['경도']], tooltip=value['건물명'], icon=icon1).add_to(marker_cluster)
# m_2
# m_2.save('offi2.html')
# idx1_map=
# folium.Map('스타벅스.html').add_to(m)
folium.map.Layer(name='스타벅스', overlay=True, control=True, show=False)
folium.map.Layer(name='따릉이 대여소', overlay=True, control=True, show=False)
# folium.map.Layer(name='스타벅스', overlay=True, control=True, show=False).add_to(m)
folium.LayerControl(position='topright', collapsed=True).add_to(m)
m.save('good.html')







