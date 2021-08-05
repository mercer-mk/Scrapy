import time
import random

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

proxies = [{
    'proxy': '116.202.228.162',
    'port': 3128
}, {
    'proxy': '116.202.232.246',
    'port': 80
}, {
    'proxy': '103.14.198.169',
    'port': 82
}, {
    'proxy': '122.15.211.125',
    'port': 80
}, {
    'proxy': '182.72.150.242',
    'port': 8080
}]
# random_index = random.randint(0, len(proxies)-1)
# profile = webdriver.FirefoxProfile()
# profile.set_preference("network.proxy.type", 1)
# print(proxies[random_index]['proxy'])
# profile.set_preference("network.proxy.http", proxies[random_index]['proxy'])
# profile.set_preference("network.proxy.http_port", proxies[random_index]['port'])
# profile.set_preference("network.proxy.ssl", proxies[random_index]['proxy'])
# profile.set_preference("network.proxy.ssl_port", proxies[random_index]['port'])


options = Options()
options.headless = True

org_name = []
address = []
mobile = []
email = []

for n in range(50):
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1440, 990)
    p = str(n + 1)
    driver.get("https://ngodarpan.gov.in/index.php/home/statewise_ngo/16050/27/" + p + "?")
    WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "blockOverlay")))

    for i in range(10):
        link_path = "//table/tbody/tr[" + str(i + 1) + "]/td[2]/a"
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//table/tbody/tr/td[2]/a")))
        l = driver.find_element_by_xpath(link_path)
        l.click()

        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "ngo_info_modal")))
            org_name.append(driver.find_element(By.XPATH, link_path).text)
            address.append(driver.find_element(By.ID, 'address').text)
            mobile.append(driver.find_element(By.ID, 'mobile_n').text)
            email.append(driver.find_element(By.ID, 'email_n').text)

            close_path = '//*[@id="ngo_info_modal"]/div[2]/div/div[1]/button'
            close = driver.find_element_by_xpath(close_path)

            WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "blockOverlay")))

            close.click()

        except TimeoutException:
            driver.quit()


        finally:
            data = pd.DataFrame({'Name': org_name,
                                 'Address': address,
                                 'Email': email,
                                 'mobile': mobile
                                 })

            data.to_csv('registration_details2.csv')
    driver.close()
