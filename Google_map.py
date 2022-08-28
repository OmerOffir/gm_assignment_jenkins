"""
The script search for locaion in google maps and and save the url,screen-shots and zoom-in zoom-out screen-shot. I've uesed selenium tool for 
this task. 
"""
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fpdf import FPDF
import numpy as np
import time


####################### configuration ####################################################
options = webdriver.ChromeOptions()
PATH = Service("C:\Program Files (x86)\chromedriver.exe")    # driver
options.add_argument('--lang=en-UK')                         # Set the language to English
driver = webdriver.Chrome(service=PATH, options=options)
wait = WebDriverWait(driver, 10)
driver.get("https://www.google.com/maps")
time.sleep(0.5)
##################### PDF ########################################################
pdf = FPDF()                                                  # create pdf
pdf.add_page()                                                # add page
pdf.set_font("Arial", size=8)                                 # font
###################################################################################

class colors:
    red = '\033[31m'
    green = '\033[32m'
    purple = '\033[35m'
    end = '\033[0m'

################# Load the csv file ##########################################
def load_csv():
    df = pd.read_csv("C:/Users/user/PycharmProjects/work_test/example_city_csv.csv")
    cities = df['city'].tolist()
    zoom_num = df['zoom_num'].tolist()
    return (cities, zoom_num)

############### Search location in google maps ###############################
def searchplace(city):
    place = driver.find_element(By.CLASS_NAME, "tactile-searchbox-input")  # search box
    place.send_keys(city)
    driver.find_element(By.XPATH, "/html/body/div[3]/div[9]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/button").click()  # press search button
    wait.until(EC.text_to_be_present_in_element((By.XPATH,'/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1') ,f'{city}'))   #INTERRUPT
    time.sleep(1.5)
    flag = 1
    screenshot(city, flag)
    print_url(city, flag, num=0)
    place.clear()



##################### Take screenshot #######################################
def screenshot(city, flag):
    if (flag == 1):
        driver.save_screenshot(f"C:/Users/user/PycharmProjects/work_test/images/{city}.png")
    elif (flag == 2):
        driver.save_screenshot(f"C:/Users/user/PycharmProjects/work_test/images/zoom_in/{city}.png")
    elif (flag == 3):
        driver.save_screenshot(f"C:/Users/user/PycharmProjects/work_test/images/zoom_out/{city}.png")

############## Save URL ##########################################
def print_url(city, flag, num):

    if (flag == 1):
        get_url = driver.current_url
        log = f"URL of {city}: {get_url}"
        log_pdf(log)
        print(log)
    elif (flag == 2):
        get_url = driver.current_url
        log = f"Zoom_in (X{num}) URL of {city}: {get_url}"
        log_pdf(log)
        print(log)
    elif (flag == 3):
        get_url = driver.current_url
        log = f"Zoom_out (X{num}) URL of {city}: {get_url}"
        log_pdf(log)
        print(log)

###################### Zoom in ###############################################
def zoom_in(num,city):
    for i in range(num):
        driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[23]/div[1]/div[3]/div[6]/div/div[1]/button").click()
        time.sleep(1)
    flag = 2
    screenshot(city, flag)
    print_url(city, flag, num)


###################### Zoom out ###############################################
def zoom_out(num, city):
    num = int(num / 2)                                     # Round down
    # num = int(np.round(num / 2))                         # Round up
    for i in range(num):
        driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[23]/div[1]/div[3]/div[6]/div/button").click()
        time.sleep(1)
    flag = 3
    screenshot(city, flag)
    print_url(city, flag, num)
    # print(num)

################ Create PFD log file ################################################
def log_pdf(log):
    pdf.cell(200, 10, txt=str(log), ln=1, align="L")


############################ Main loop #############################################
if __name__ == '__main__':
    cities, zoom_num = load_csv()
    for ct,zn in zip(cities, zoom_num):
        print(colors.purple,f'----------------------{ct}-------------------------',colors.end)
        log_pdf(f'----------------------{ct}-------------------------')
        searchplace(ct)
        zoom_in(zn, ct)
        zoom_out(zn, ct)
    pdf.output("URL_list.pdf")                                                    # output file
    driver.close()





