import sys
sys.path.append('.')
from AastockScraper import AAstock
import unittest
import chromedriver_autoinstaller
from selenium import webdriver 
import json

class Test(unittest.TestCase):
    def setUp(self):
        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome()
        

    def tearDown(self):
        pass
