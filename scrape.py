import random
import time
import re
from selenium import webdriver
from searchterms import searchterms
from db import DB
from common import db_cred

def navigate_to_content_frame(driver):
    # locate iframe & switch to it
    elements = driver.find_elements_by_tag_name("frame")
    element = elements[2]
    driver.switch_to_frame(element)

    # pretend we're human
    time.sleep(2)

def extract_record_info(driver, data):
    image_url       = data[0].find_elements_by_tag_name('a').get_attribute('href')
    title           = data[1].find_elements_by_tag_name('a').get_attribute('innerText')
    photographer    = data[2].find_element_by_tag_name('a').get_attribute('innerText')
    order_no        = re.sub("[^0-9]", "",data[3].get_attribute('innerText'))
    filing_info     = data[4].get_attribute('innerText')
    date            = data[5].get_attribute('innerText')
    description     = data[6].get_attribute('innerText')
    notes           = data[7].get_attribute('innerText')
    summary         = data[8].get_attribute('innerText')
    subjects        = data[9].get_attribute('innerText')

    record = {
        'image_url': image_url,
        'title': title,
        'photographer': photographer,
        'order_no': order_no,
        'filing_info': filing_info,
        'date': date,
        'description': description,
        'notes': notes,
        'summary': summary,
        'subjects': subjects
    }

    return record


if __name__ == "__main__":
    # open DB connection
    db = DB(db_cred)

    for term in searchterms:
        # Create new session
        driver = webdriver.Chrome(executable_path = '/usr/local/chromedriver/chromedriver')
        driver.implicitly_wait(10)

        driver.get('http://photos.lapl.org')

        # PAGE: Photos Home
        navigate_to_content_frame(driver)

        search_input = driver.find_element_by_name('keyword')

        search_input.send_keys(term)
        driver.find_element_by_name("Search").click()

        # PAGE: Search Results List
        navigate_to_content_frame(driver)

        entry_list = driver.find_elements_by_css_selector('.titleListTitle')
        entry = entry_list[0]

        link = entry.find_element_by_tag_name('a')
        link.click()

        records = []
        # Get items until failure
        while True:
            # in batches of 100
            for index in range(0,5):
                # PAGE: Individual Record
                navigate_to_content_frame(driver)

                data = driver.find_elements_by_css_selector('.BIBtagdata')

                # Extract data
                try:
                    record_hash = extract_record_info(driver, data)
                    records.append(record_hash)
                except Exception as e:
                    print "Error finding record info. {0}".format(e)
                    db.create_record_batch(records)

                # Continue to next page, or save if no pages left
                try:
                    next_link = driver.find_element_by_link_text('Next')
                    next_link.click()
                except Exception as e:
                    print "Error finding link. {0}".format(e)
                    db.create_record_batch(records)

            db.create_record_batch(records)

        # End session
        driver.quit()
