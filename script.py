# nohup python3 final.py >/dev/null 2>&1 & disown
#scp azureuser@20.125.141.166:occupancy_data.csv /Users/omidgholizadeh/Documents
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import random
import pandas as pd
import csv
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

#import chromedriver_autoinstaller
#chromedriver_autoinstaller.install()


counter = 0
time_start = time.time()

while True:

    try:

            counter += 1
            print("Scan: ", counter)
            print("Time Elapsed: ", (time.time() - time_start)/60)


            try:
                with open("occupancy_data_new.csv", "r") as file:
                    print("Ledger Loaded")
            except FileNotFoundError:
                with open("occupancy_data_new.csv", "w") as file:
                    print("Ledger Created")

            url = "https://connect2concepts.com/connect2/?type=circle&key=59ac279f-1fd6-4e55-925c-f7e02764ab00"



            options = Options()
            options.headless = True
            driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)
            #driver = webdriver.Chrome("/Users/omidgholizadeh/Downloads/chromedriver", options=options)

            driver.implicitly_wait(20)
            driver.get(url)

            time.sleep(random.random() * 5)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            driver.quit()

            venue_data = soup.find_all('div', {'style': 'text-align:center;'})

            df = pd.DataFrame()

            dictionary = {"ARC Floor 1": [], "Climbing": [], "ARC Olympic Lifting Zones": [], "ARC Floor 2": [], "South Court": [],
                          "4 Court Gym": [], "North Court": [], "Recreation Pool": [], "Competition Pool": [], "ARC Express": [],
                          "Spa": [], "Aquaplex Pool Deck": [], "Tennis Courts": []}

            for venue in venue_data:
                data = venue.text

                venue_name = data.split("(")[0]

                open_status = data.split("(")[1]
                open_status = open_status.split(")")[0]

                person_count = data.split("Last Count: ")[1]
                person_count = person_count.split("Updated: ")[0]

                last_updated = data.split("Updated: ")[1]
                last_updated = last_updated[0:10]

                last_time = data[-8:]

                dictionary[venue_name] = (last_updated, last_time, open_status, person_count)




            pd.DataFrame(dictionary).T.to_csv('occupancy_data_new.csv', header=False, mode='a')

            for i in range(10):
                print("Sleeping" + i * ".")
                time.sleep(60)


    except:
        print("Error")
        time.sleep(5)
        pass
