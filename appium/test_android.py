import unittest
from selenium import webdriver

class AndroidTest(unittest.TestCase):

    def setUp(self):
        caps = {
            'platformName': 'Android',
            'automationName': 'UIAutomator2',
            'app': '/Users/jeremykao/work/learning/appium/app-debug.apk',
            'deviceName': 'FBAZCY09W684'
        }
        self._driver = webdriver.Remote('http://localhost:4723/wd/hub', caps)

    def test(self):
        self._driver.find_element_by_id('show_recycler').click()
        pass

    def tearDown(self):
        self._driver.quit()

if __name__ == '__main__':
    unittest.main()

