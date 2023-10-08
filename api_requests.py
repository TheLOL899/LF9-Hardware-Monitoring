import json
import requests

class ApiRequests:
    def __init__(self):
        self.api_url = "https://192.168.193.128/restconf/data/ietf-interfaces:interfaces"
        self.headers = {"Accept": "application/yang-data+json", "Content-type": "application/yang-data+json"}
        self.basicauth = ("cisco", "cisco123!")

    def send_request(self, method, url, data=None):
        try:
            resp = requests.request(method, url, auth=self.basicauth, headers=self.headers, json=data, verify=False)
            resp.raise_for_status()

            if 200 <= resp.status_code < 300:
                return resp.json()
            else:
                print(f"Ungültige Serverantwort. Statuscode: {resp.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Fehler bei der {method}-Anfrage: {str(e)}")
            return None

    def send_get_request(self):
        return self.send_request("GET", self.api_url)

    def send_get_interface_request(self, interface_name):
        url = f"{self.api_url}/interface={interface_name}"
        return self.send_request("GET", url)

    def send_post_request(self, data):
        return self.send_request("POST", self.api_url, data)

    def send_put_request(self, data, interface_name):
        url = f"{self.api_url}/interface={interface_name}"
        return self.send_request("PUT", url, data)

    def send_delete_request(self, interface_name):
        url = f"{self.api_url}/interface={interface_name}"
        return self.send_request("DELETE", url)
