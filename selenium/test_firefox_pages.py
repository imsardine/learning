import unittest, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from pageobject_support import callable_find_by as find_by, visible

class HomePage:

    _search_box = find_by(id_='searchInput')

    def __init__(self, driver):
        self._driver = driver

    def visit(self):
        self._driver.get('http://en.wikipedia.org')
        return self
    
    def search(self, keyword):
        self._search_box().send_keys(keyword + Keys.ENTER)
        return ArticlePage(self._driver)

class ArticlePage:

    _heading = find_by(id_='firstHeading')

    def __init__(self, driver):
        self._driver = driver

    @property
    def title(self):
        heading = WebDriverWait(self._driver, 5).until(visible(self._heading))
        return heading.text

class HelloWorldTest(unittest.TestCase):

    def setUp(self):
        self._driver = webdriver.Firefox()

    def test(self):
        home = HomePage(self._driver).visit()
        article = home.search('hello world')
        self.assertEqual(article.title, '"Hello, World!" program')

    def tearDown(self):
        self._driver.quit()

if __name__ == '__main__':
    unittest.main()

