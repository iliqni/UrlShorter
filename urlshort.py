import tkinter as tk
import requests
import json

class URLShortenerGUI:
    def __init__(self, master):
        self.master = master
        master.title("URL Shortener")

        self.service_label = tk.Label(master, text="Choose a URL shortening service:")
        self.service_label.pack()

        self.service_options = [
            ("Bitly", "https://api-ssl.bitly.com/v4/shorten"),
            ("TinyURL", "https://tinyurl.com/api-create.php"),
            ("Rebrandly", "https://api.rebrandly.com/v1/links")
        ]

        self.service_var = tk.StringVar()
        self.service_var.set(self.service_options[0][1])

        for service, url in self.service_options:
            radio_button = tk.Radiobutton(master, text=service, variable=self.service_var, value=url)
            radio_button.pack(anchor=tk.W)

        self.long_url_label = tk.Label(master, text="Enter a long URL:")
        self.long_url_label.pack()

        self.long_url_entry = tk.Entry(master)
        self.long_url_entry.pack()

        self.shorten_button = tk.Button(master, text="Shorten URL", command=self.shorten_url)
        self.shorten_button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

    def shorten_url(self):
        service_url = self.service_var.get()
        long_url = self.long_url_entry.get()

        if service_url == "https://api-ssl.bitly.com/v4/shorten":
            access_token = "YOUR_BITLY_ACCESS_TOKEN_HERE"
            headers = {
                "Authorization": "Bearer " + access_token,
                "Content-Type": "application/json"
            }
            payload = {
                "long_url": long_url,
                "domain": "bit.ly"
            }
            response = requests.post(service_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            data = json.loads(response.text)
            short_url = data["link"]

        elif service_url == "https://tinyurl.com/api-create.php":
            params = {
                "url": long_url
            }
            response = requests.get(service_url, params=params)
            response.raise_for_status()
            short_url = response.text

        elif service_url == "https://api.rebrandly.com/v1/links":
            api_key = "YOUR_REBRANDLY_API_KEY_HERE"
            headers = {
                "apikey": api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "destination": long_url
            }
            response = requests.post(service_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            data = json.loads(response.text)
            short_url = data["shortUrl"]

        self.result_label.config(text=short_url)

if __name__ == "__main__":
    root = tk.Tk()
    gui = URLShortenerGUI(root)
    root.mainloop()
