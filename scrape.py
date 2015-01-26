import random
import time
import re
from selenium import webdriver
from searchterms import searchterms
from db import DB

def navigate_to_content_frame(driver):
    # locate iframe & switch to it
    elements = driver.find_elements_by_tag_name("frame")
    element = elements[2]
    driver.switch_to_frame(element)

    # pretend we're human
    time.sleep(1)

def extract_record_info(driver, data):
    # hacky, trying to account for missing photographer but with no easy way
    #   to reference the element that contains the photographer info
    photographer = None
    index = range(2,9)
    try:
        photographer = data[2].find_element_by_tag_name('a').get_attribute('innerText')
        # Begin count at 3, after photographer
        index = range(3,10)
    except Exception as e:
        print "No photographer found: {0}".format(e)

    # try again, just ignore the entry if it breaks something
    try:
        image_url       = data[0].find_element_by_tag_name('a').get_attribute('href')
        title           = data[1].find_element_by_tag_name('a').get_attribute('innerText')

        # these elements are relative, based on whether photographer is present
        order_no        = re.sub("[^0-9]", "",data[index.pop(0)].get_attribute('innerText'))
        filing_info     = data[index.pop(0)].get_attribute('innerText')
        date            = data[index.pop(0)].get_attribute('innerText')
        description     = data[index.pop(0)].get_attribute('innerText')
        notes           = data[index.pop(0)].get_attribute('innerText')
        summary         = data[index.pop(0)].get_attribute('innerText')
        subjects        = data[index.pop(0)].get_attribute('innerText')

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

    except Exception as e:
        print e


if __name__ == "__main__":
    # open DB connection
    db = DB()

    for term in searchterms:
        # Create new session
        driver = webdriver.Chrome(executable_path = '/usr/local/chromedriver/chromedriver')
        driver.implicitly_wait(7)

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

        # Get items until failure
        records = []
        count = 0

        while True:
            count += 1

            # PAGE: Individual Record
            navigate_to_content_frame(driver)
            data = driver.find_elements_by_css_selector('.BIBtagdata')

            # Extract data
            record_hash = extract_record_info(driver, data)
            records.append(record_hash)

            # in batches of 100
            if count % 100 == 0:
                db.create_record_batch(records)
                records = []
            # continue to next try
            try:
                next_link = driver.find_element_by_link_text('Next')
                next_link.click()
            except Exception as e:
                print "End of results. {0}".format(e)
                break

        db.create_record_batch(records)

        # End session
        driver.quit()
