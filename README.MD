Install CRSV100V VM 

Install python 
pip install python 
pip install tk 
pip install requests 

Die VM fügt via DHCP sich selbst eine IP Adresse zu. 
Um diese zu sehen muss man in der VM folgende Befehle ausführen: 
en 
show ip interface brief 

Ändere die IP-Adresse für die Apirequests in der api_requests.py mit der IP Adresse aus der VM. 

Anwendung starten: 
python main.py 
