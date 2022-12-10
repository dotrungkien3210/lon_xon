from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import numpy as np
import os

chrome_options = Options()
PATH = "C:\Program Files\Google\Chrome\chromedriver.exe"
driver = webdriver.Chrome(PATH, options=chrome_options)
# implicit wait
driver.implicitly_wait(20)
# maximize browser
driver.maximize_window()
# -----------------------------------open web brower-------------------------------------
driver.get(
    "https://www.standard.no/en/webshop/search/?search=NS&fbclid=IwAR3zbo-k2mV90K-lnKHo-qFTZKtiw-FtiK3Wz_oHNv97cFYpYwtyzcncwY4")
time.sleep(1)
driver.find_element(By.ID, "ctl00_FullRegion_uxSearchResultContainer_SearchIncludingWithdrawnChkBox").click()
time.sleep(1)

count_all = driver.find_element(By.XPATH, '//*[@id="ctl00_FullRegion_uxSearchResultContainer_HitStats"]/b')
count_all = int(count_all.text)
count_all = int(count_all / 10) + 1
current_page = 7

first = pd.DataFrame(
    columns=['Name', 'Name With Year', 'Year', 'Description', 'Language', 'Url', 'Replace', 'Replace By', 'Active'])
PATH1 = 'data.csv'
csv_columns = ['Name', 'Name With Year', 'Year', 'Description', 'Language', 'Url', 'Replace', 'Replace By', 'Active']

if current_page > 1:
    for page in range(1, current_page):
        driver.find_element(By.XPATH, '//*[@id="ctl00_FullRegion_uxSearchResultContainer_PagerNextLink"]').click()
        time.sleep(5)

if os.path.isfile(PATH) and os.access(PATH1, os.R_OK):
    for page in range(current_page, count_all + 1):
        data = np.empty((0, 9), int)
        for i in range(1, 11):
            title = driver.find_element(By.XPATH,
                                        '//*[@id="ctl00_FullRegion_uxSearchResultContainer_SearchResultSection"]/div[' + str(
                                            i) + ']/div[2]/h3')
            count = len(driver.find_elements(By.XPATH,
                                             '//*[@id="ctl00_FullRegion_uxSearchResultContainer_SearchResultSection"]/div[' + str(
                                                 i) + ']/div[5]/p[1]/span'))
            check_Withdrawn = driver.find_element(By.XPATH,
                                                  '//*[@id="ctl00_FullRegion_uxSearchResultContainer_SearchResultSection"]/div[' + str(
                                                      i) + ']/div[5]/p[1]/span[' + str(count) + ']/strong')
            description = driver.find_element(By.XPATH,
                                              '//*[@id="ctl00_FullRegion_uxSearchResultContainer_SearchResultSection"]/div[' + str(
                                                  i) + ']/div[5]/div[1]/p')
            name_with_year = title.text
            name = name_with_year.split()[-1]
            year = ' '.join(name_with_year.split()[0:-1])
            if_active = "no"
            # print(count)
            if (check_Withdrawn.text != "Withdrawn"):
                if_active = "yes"
                # print("is publish : "+if_active)
            else:
                if_active = "no"
                # print("is publish : " + if_active)
            description = description.text
            time.sleep(1)
            title.click()
            time.sleep(1)
            web_url = driver.current_url
            publish_or_drawn = driver.find_element(By.XPATH,
                                                   '//*[@id="ctl00_FullRegion_myProductDetails_trStatus"]/td[2]')
            # print(publish_or_drawn.text)
            country = driver.find_element(By.XPATH, '//*[@id="ctl00_FullRegion_myProductDetails_trLanguage"]//td[2]')
            country = country.text
            Supersedes = "None"
            Superseded_by = "None"
            if (publish_or_drawn.text == "Withdrawn"):
                try:
                    Supersedes = driver.find_element(By.XPATH,
                                                     '//*[@id="body"]/div/section[2]/div/div[1]/div/table/tbody/tr[7]/td[2]/a')
                    Supersedes = Supersedes.text
                    # print(Supersedes.text)
                    Superseded_by = driver.find_element(By.XPATH,
                                                        '//*[@id="body"]/div/section[2]/div/div[1]/div/table/tbody/tr[8]/td[2]/a')
                    Superseded_by = Superseded_by.text
                    # print(Superseded_by.text)
                except:
                    Supersedes = None
                    # print(Supersedes)
                    Superseded_by = None
                    # print(Superseded_by)
            else:
                Supersedes = None
                # print(Supersedes)
                Superseded_by = None
                # print(Superseded_by)
            time.sleep(1)
            driver.back()
            time.sleep(1)
            print(name)  # 1
            print(name_with_year)  # 2
            print(year)  # 3
            print(description)  # 4
            print(country)  # 5
            print(web_url)  # 6
            print(Supersedes)  # 7
            print(Superseded_by)  # 8
            print(if_active)  # 9
            data = np.append(data, np.array(
                [[name, name_with_year, year, description, country, web_url, Supersedes, Superseded_by, if_active]]),
                             axis=0)
            print("-----------------------------------------------------------------------------------")
        csvdata = pd.DataFrame(data, columns=csv_columns)
        csvdata.to_csv('data.csv', index=False, mode='a', header=False)

        # Open a file with access mode 'a'
        file_object = open('save_work.txt', 'a')
        # Append 'hello' at the end of file
        file_object.write("Success save page number " + str(page) + "\n")
        # Close the file
        file_object.close()

        print("Success save page number " + str(page))
        print("-----------------------------go to next page-----------------------------------------------")
        try:
            driver.find_element(By.XPATH, '//*[@id="ctl00_FullRegion_uxSearchResultContainer_PagerNextLink"]').click()
        except:
            print("khong the bam vao nut next de chuyen trang")
            print("chuong trinh gap loi tai page thu : " + str(page))
            print("mo file save_work.txt neu như " + str(count_all) + " page da duoc luu chung to da luu toan bo")
            break
else:
    first.to_csv('data.csv', index=False)
    print("Created CSV save file, Please run Again")
# -----------------------------------close web browser-------------------------------------
driver.close()
