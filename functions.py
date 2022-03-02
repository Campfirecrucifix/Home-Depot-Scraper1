from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


def initialization(driver,URL):
    driver.get(URL)
    try:
        shipping_cross = WebDriverWait(driver, 10) \
            .until(EC.element_to_be_clickable((By.ID, "deliveryZipDropDownClose")))  # Wait for first X Click
    except:
        driver.quit()
    driver.find_element(By.ID, "deliveryZipDropDownClose").click()  # First X Click


def store_dropdown(driver):
    store_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myStore")))# Wait for Store Dropdown
    store_dropdown.click()  #Fix this ---> #Already fixed! ~Present Me
    time.sleep(2)
    try:
        find_my_store_button = WebDriverWait(driver, 10) \
            .until(EC.element_to_be_clickable((By.XPATH, "//*[@id='myStoreDropdown']/div/div[4]/a/span")))  # Wait for first X Click change this to CSS Selector
    except TimeoutException:
        print("Could not find store dropdown. Retrying...")
        time.sleep(2)
        find_my_store_button = WebDriverWait(driver, 10) \
            .until(EC.element_to_be_clickable((By.XPATH, "//*[@id='myStoreDropdown']/div/div[4]/a/span")))
    find_my_store_button.click()


# Loops through and selects store
def store_selector(driver, store_number):
    no_errors = False
    textbox = driver.find_element(By.ID, "myStore-formInput")
    #time.sleep(1)
    textbox.send_keys(store_number, Keys.RETURN)
    time.sleep(1)
    while not no_errors:
        no_errors = True
        while driver.find_element(By.ID, "myStore-errorMessage").is_displayed() and store_number < 10000:
            store_number += 1
            textbox.clear()
            textbox.send_keys(store_number, Keys.RETURN)
            time.sleep(1)
        else:
            try:
                store_button = driver.find_element(By.CSS_SELECTOR, f'button[data-storeid="{str(store_number).zfill(4)}"]')
            except NoSuchElementException:
                print("Could not find Store Selector Button. Retrying...")
                time.sleep(2)
                try:
                    store_button = driver.find_element(By.CSS_SELECTOR, f'button[data-storeid="{str(store_number).zfill(4)}"]')
                except NoSuchElementException:
                    print("There was a problem with store:"+str(store_number)+". Skipping...")
                    no_errors = False
                    textbox.clear()
                    store_number += 1
                    textbox.send_keys(store_number, Keys.RETURN)
                    time.sleep(1)
    store_button.click()
    return store_number


# Retrieves the prices
def item_inspector(driver):
    try:  # fix this to handle item out of stock
        item_price = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='price-format__large price-format__main-price']/span[2]"))).text
    except StaleElementReferenceException:
        print("Could not find item price. Retrying...")
        time.sleep(2)
        item_price = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='price-format__large price-format__main-price']/span[2]"))).text
    # print("$"+item_price.text)
    time.sleep(3)
    return item_price


# Not used anymore
def item_adder(driver):
    clickable_button_xpath = "//a[@type='button'][contains(., 'Ship to Home') and contains(@class, '-unselected')]"
    selected_button_xpath = "//a[@type='button'][contains(., 'Ship to Home') and contains(@class, '-selected')]"
    unclickable_button_xpath = "//a[@type='button'][contains(., 'Ship to Home') and contains(@class, '-unclickable')]"
    time.sleep(1.5)
    some_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, clickable_button_xpath)))
    some_element.click()
    add_to_cart_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//img[@class='add-to-cart__icon']")))
    add_to_cart_button.click()
    pass


# Write store number and item price to file
def write_to_file(store_number, prices):
    lowest_price(store_number, prices)
    textfile = open("a_file.txt", "a")
    textfile.write("Store:" + str(store_number) + " Price:$" + prices + "\n")
    textfile.close()


def lowest_price(store_number, item_price):
    if item_price == "":
        print("This item in store:"+str(store_number)+" has no price. Skipping.")
    else:
        item_price = int(item_price)
        if item_price < 899:
            print("Store Number:" + store_number + "has the lowest price of" + item_price)
