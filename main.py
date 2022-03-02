from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from functions import initialization, store_dropdown, store_selector, item_adder, item_inspector,write_to_file

PATH = "chromedriver.exe"
URL = "http://tiny.cc/5h5ouz"
#URL = "https://www.homedepot.com/p/Hampton-Bay-Mena-54-in-White-Color-Changing-Integrated-LED-Indoor-Outdoor-Black-Ceiling-Fan-with-Light-Kit-and-Remote-Control-58929/315182926"
store_number = 1553  # 149
prices = []

ser = Service(PATH)
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)

initialization(driver, URL)

while store_number < 10000:
    store_dropdown(driver)
    store_number = store_selector(driver, store_number) + 1

    # prices.append("Store: "+str(store_number)+":$"+str(item_inspector(driver)))
    write_to_file(store_number, item_inspector(driver))
    # print(prices)
#item_adder(driver)



