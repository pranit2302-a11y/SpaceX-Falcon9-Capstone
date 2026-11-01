import folium
from folium.plugins import MarkerCluster
from pathlib import Path

Path("outputs/maps").mkdir(parents=True, exist_ok=True)
sites = [
 ("Cape Canaveral SLC-40",28.5618571,-80.577366,"99 launches; 72 successful (72.7%)"),
 ("Kennedy LC-39A",28.6080585,-80.6039558,"52 launches; 47 successful (90.4%)"),
 ("Vandenberg SLC-4E",34.632093,-120.610829,"28 launches; 23 successful (82.1%)")
]
m=folium.Map(location=[30.5,-95],zoom_start=3,tiles="OpenStreetMap")
cluster=MarkerCluster().add_to(m)
for name,lat,lon,detail in sites:
    folium.Marker([lat,lon],popup=f"<b>{name}</b><br>{detail}",tooltip=name).add_to(cluster)
m.save("outputs/maps/launch_sites_map.html")
