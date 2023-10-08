from tkinter import Tk
from gui import ApiClientGUI
from api_requests import ApiRequests

if __name__ == "__main__":
    root = Tk()
    api_requests = ApiRequests()
    app = ApiClientGUI(root, api_requests)
    root.mainloop()