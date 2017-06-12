import unittest, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HelloWorldTest(unittest.TestCase):

    def setUp(self):
        self._driver = webdriver.Firefox()

    def test(self):
        browser = self._driver

        browser.get('http://en.wikipedia.org')
        browser.find_element_by_id('searchInput').send_keys('hello world' + Keys.ENTER)

        heading = WebDriverWait(browser, 5).until(
                EC.visibility_of_element_located((By.ID, 'firstHeading'))
            ).text
        self.assertEqual(heading, '"Hello, World!" program')

    def tearDown(self):
        self._driver.quit()

if __name__ == '__main__':
    unittest.main()

