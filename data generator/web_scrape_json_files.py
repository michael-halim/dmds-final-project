from math import prod
import os
from numpy import product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException,WebDriverException

import re


def remove_text_in_between(text,start,end):
    idx_start = text.index(start) if start in text else None
    idx_end = text.index(end) + len(end) if end in text else None
    
    if idx_start == None or idx_end == None:
        return text
    return str(text[0:idx_start]) + str(text[idx_end:])



os.environ['PATH'] += r'C:/SeleniumDrivers'
driver = webdriver.Chrome()
driver.implicitly_wait(15)

def get_desc_detail():
    from all_data import all_data as AD

    # Get links, product_name from All Data (AD)
    product_links_names = [[attr[5],attr[0]] for attr in AD]
    collections_desc = []
    collections_detail = []

    for links_names in product_links_names:
        try:
            driver.get(links_names[0])

            product_descs = driver.find_elements(By.CSS_SELECTOR, 'p[property="description"]')
            product_details = driver.find_elements(By.CSS_SELECTOR, 'td.pvs')

            for descs in product_descs:
                desc = descs.get_attribute('innerHTML')
                desc = desc.replace('"','')
                desc = desc.encode('ascii', 'ignore').decode()
                collections_desc.append([links_names[1],desc])
                print(desc)

            tmp_detail = {}
            current_key = None
            for count,details in enumerate(product_details):
                product_detail = details.get_attribute('innerHTML')
                product_detail = remove_text_in_between(product_detail,'<a','>')
                product_detail = product_detail.replace('</a>','')
                product_detail = product_detail.encode('ascii', 'ignore').decode()

                if count % 2 == 0:
                    tmp_detail[product_detail] = ''
                    current_key = product_detail
                else:
                    tmp_detail[current_key] = product_detail

            collections_detail.append([links_names[1],tmp_detail])
            print(tmp_detail)

        except WebDriverException as e:
            print(e)


    # Open desc.txt and make it to list as txt
    with open('desc.txt','w') as file:
        file.write('desc = [')
        for count,product in enumerate(collections_desc):
            file.write(str(product))

            if count == len(collections_desc):
                file.write('\n')
            else:
                file.write(',\n')

        file.write(']')
    file.close()

    # Open detail.txt and make it to list as txt
    with open('detail.txt','w') as file:
        file.write('detail = [')
        for count,product in enumerate(collections_detail):
            file.write(str(product))

            if count == len(collections_detail):
                file.write('\n')
            else:
                file.write(',\n')

        file.write(']')
    file.close()

    FILE_NAME = 'desc'
    try:
        os.rename(FILE_NAME + '.txt', FILE_NAME + '.py')

    except FileExistsError:
        
        chc = input('{0}.py Already Exist. Do You Want to Overwrite ? (0/1)'.format(FILE_NAME))
        
        if chc == '1':
            os.remove(FILE_NAME + '.py')
            os.rename(FILE_NAME + '.txt',FILE_NAME + '.py')

    finally:
        input(FILE_NAME + 'Finished\n\n')

    FILE_NAME = 'detail'
    try:
        os.rename(FILE_NAME + '.txt', FILE_NAME + '.py')

    except FileExistsError:
        
        chc = input('{0}.py Already Exist. Do You Want to Overwrite ? (0/1)'.format(FILE_NAME))
        
        if chc == '1':
            os.remove(FILE_NAME + '.py')
            os.rename(FILE_NAME + '.txt',FILE_NAME + '.py')

    finally:
        input('Program Finished\n\n')

if __name__ == '__main__':
    get_desc_detail()