#https://api.telegram.org/bot6217962481:AAElrXjC0iR3wg1csX7ex-jaURJk1EbNOdk/getUpdates

import requests
import time

current_struct_time = time.localtime()
formatted_time = time.strftime("%d/%m/%Y %H:%M:%S", current_struct_time)
noidungvipham="Dung Day"

baseUrl='https://api.telegram.org/bot6217962481:AAElrXjC0iR3wg1csX7ex-jaURJk1EbNOdk/sendPhoto'


my_file = open("6613904233cee190b8df.jpg", "rb")
phong='413'
parameters = {
    "chat_id" : "-984762057",
    "caption" : f"Thoi gian: {formatted_time}"+","+f"Noi dung vi pham: {noidungvipham}','Phong:f{phong}"
}

files = {
    "photo" : my_file
}
resp = requests.get(baseUrl, data = parameters, files=files)
print(resp.text)