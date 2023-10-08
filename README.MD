# Software zur Konfiguration eines virtuellen Routers von Team09
Eine Software zum Konfigurieren eines virtuellen Routers über SSH und einer APi mit GUI. 

## Vorbereitung VM CRSV1000V

Install CRSV1000V VM <br>

Die VM fügt via DHCP sich selbst eine IP Adresse zu. <br>
Um diese zu sehen muss man in der VM folgende Befehle ausführen: <br>
```
en 
show ip interface brief 
```

Schaue in der VM, ob alle Sachen laufen mit den Befehlen:  

config -t <br>
restconf <br>

## Vorbereitung Script 

Install python <br>

pip install python tk requests
<br>

Ändere die IP-Adresse für die Apirequests in der api_requests.py mit der IP Adresse aus der VM. <br>

Anwendung starten: <br>
python main.py 
