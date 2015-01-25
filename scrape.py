from selenium import webdriver

path_to_chromedriver = '/usr/local/chromedriver/chromedriver'
driver = webdriver.Chrome(executable_path = path_to_chromedriver)

url = 'http://photos.lapl.org'

driver.implicitly_wait(5)
driver.get(url)

elements = driver.find_elements_by_tag_name("frame")

# for element in elements:
    driver.switch_to_default_content()
    driver.switch_to_frame(element)

    try:
        search_input = driver.find_element_by_name('keyword')

        print("Element found!")
        search_input.send_keys("some text")
        driver.find_element_by_name("Search").click()
    except selenium.common.exceptions.NoSuchElementException as e:
        print(e)

# driver.quit()

# element = driver.find_element_by_xpath("//frameset")
# driver.switch_to_frame(element)
# element = driver.find_element_by_xpath("//frame")
# driver.switch_to_frame(element)
# search_input = driver.find_element_by_name('keyword')
