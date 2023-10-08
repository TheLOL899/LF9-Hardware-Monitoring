import tkinter as tk
from api_requests import ApiRequests
from tkinter import ttk
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiClientGUI:
    def __init__(self, master, api_requests):
        self.master, self.api_requests = master, api_requests
        self.bg_color, self.text_color = "#E0E0E0", "#333333"
        self.create_widgets()

    def create_widgets(self):

        text_area_label = tk.Label(self.master, text="Geben Sie JSON ein:", bg=self.bg_color, fg=self.text_color)
        text_area_label.pack()
        self.text_area = tk.Text(self.master, height=10, width=50, bg=self.bg_color, fg=self.text_color)
        self.text_area.pack(pady=10)

        scrollbar = tk.Scrollbar(self.master, command=self.text_area.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_area.config(yscrollcommand=scrollbar.set)

        interface_name_label = tk.Label(self.master, text="Interface-Name:", bg=self.bg_color, fg=self.text_color)
        interface_name_label.pack()
        self.interface_name_entry = tk.Entry(self.master, bg=self.bg_color, fg=self.text_color)
        self.interface_name_entry.pack(pady=5)

        button_frame = tk.Frame(self.master, bg=self.bg_color)
        button_frame.pack()

        buttons = [("Get Interface", self.get_interface), ("GET ALL", self.send_get_all_request),
                   ("POST", self.send_post_request), ("PUT", self.send_put_request), ("DELETE", self.send_delete_request)]

        for text, command in buttons:
            button = tk.Button(button_frame, text=text, command=command, bg=self.bg_color, fg=self.text_color)
            button.pack(side="left", padx=5)

        self.result_frame = tk.Frame(self.master, bg=self.bg_color)
        self.result_frame.pack(pady=10)

        columns = ('Name', 'Description', 'Type', 'Enabled', 'IPv4 Address', 'IPv6 Address')
        self.result_tree = ttk.Treeview(self.result_frame, columns=columns)
        for col in columns:
            self.result_tree.heading(col, text=col)
        self.result_tree.pack()

    def send_get_all_request(self):
        self.display_response(self.api_requests.send_get_request())

    def get_interface(self):
        interface_name = self.interface_name_entry.get()
        self.display_response(self.api_requests.send_get_interface_request(interface_name))

    def send_post_request(self):
        data = self.get_input_data()
        self.display_response(self.api_requests.send_post_request(data))

    def send_put_request(self):
        data = self.get_input_data()
        interface_name = self.extract_interface_name(data)
        self.display_response(self.api_requests.send_put_request(data, interface_name))

    def send_delete_request(self):
        interface_name = self.interface_name_entry.get()
        self.display_response(self.api_requests.send_delete_request(interface_name))

    def get_input_data(self):
        try:
            return json.loads(self.text_area.get("1.0", "end-1c"))
        except json.JSONDecodeError as e:
            print(f"Fehler beim Laden von JSON-Daten: {str(e)}")
            return None

    def extract_interface_name(self, data):
        return data.get("ietf-interfaces:interface", {}).get("name", "")

    def display_response(self, response):
        self.clear_result_tree()

        if response is not None:
            if "error" in response:
                self.result_tree.insert("", "end", values=(f"Fehler: {response['error']['message']}", "", "", "", "", ""))
            else:
                if 'ietf-interfaces:interface' in response:
                    self.display_single_interface(response.get('ietf-interfaces:interface', {}))
                elif 'ietf-interfaces:interfaces' in response:
                    for interface in response['ietf-interfaces:interfaces']['interface']:
                        self.display_single_interface(interface)
                else:
                    print("Ungültiges Antwortformat")
        else:
            self.result_tree.insert("", "end", values=("Die Anfrage war erfolgreich!", "", "", "", "", ""))

    def display_single_interface(self, interface):
        name, description, type, enabled = interface.get('name', ''), interface.get('description', ''), \
                                          interface.get('type', ''), interface.get('enabled', '')

        ipv4_addresses = interface.get('ietf-ip:ipv4', {}).get('address', [])
        ipv6_addresses = interface.get('ietf-ip:ipv6', {}).get('address', [])

        ipv4_address = f"{ipv4_addresses[0].get('ip', '')}/{ipv4_addresses[0].get('netmask', '')}" if ipv4_addresses else ""
        ipv6_address = ipv6_addresses[0].get('ip', '') if ipv6_addresses else ""

        self.result_tree.insert("", "end", values=(name, description, type, enabled, ipv4_address, ipv6_address))

    def clear_result_tree(self):
        [self.result_tree.delete(item) for item in self.result_tree.get_children()]


if __name__ == "__main__":
    root, api_requests = tk.Tk(), ApiRequests()
    app = ApiClientGUI(root, api_requests)
    root.mainloop()
