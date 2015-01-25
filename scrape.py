import random
import time
from selenium import webdriver
from searchterms import searchterms

def navigate_to_content_frame(driver):
    # locate iframe & switch to it
    elements = driver.find_elements_by_tag_name("frame")
    element = elements[2]
    driver.switch_to_frame(element)

    # pretend we're human
    time.sleep(2)



if __name__ == "__main__":

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

        # ten list entries per page
        entry_indexes = range(0,9)

        for index in entry_indexes:
            navigate_to_content_frame(driver)

            entry_list = driver.find_elements_by_css_selector('.titleListTitle')
            entry = entry_list[index]

            link = entry.find_element_by_tag_name('a')
            link.click()

            # PAGE: Individual Record
            navigate_to_content_frame(driver)

            # Data to gather:
                # Date
                # Photographer
                # Record link
                # Image link
                # Notes
                # Summary
                # Filing information
                # Order number

            driver.back()

        # End session
        driver.quit()
