import sys
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


class ChromeSetup():
    '''
    This class is just for setting up chrome driver for selenium. 
    It can save your time when you create a class that utilise selenium. 
    Just import this, put it as inherented class, and super.__init__(). 
    '''

    def __init__(
        self,
        headless: bool = True,
    ):
        # setup ChromeOptions
        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument('--disable-extensions')
        # self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        self.chrome_options.add_argument('--ignore-ssl-errors')
        # loading strategy, {'normal', 'eager', 'none'}, see https://www.selenium.dev/documentation/webdriver/page_loading_strategy/
        self.chrome_options.page_load_strategy = 'eager'
        # window size, if not headless
        if not headless:
            self.chrome_options.add_argument('--start-maximized')
        # if headless or sys.platform == 'linux':
        #     self.chrome_options.add_argument('--headless')
        # if sys.platform == 'linux':
        #     self.chrome_options.add_argument('--no-sandbox')
        #     self.chrome_options.add_argument('--disable-dev-shm-usage')
        # install newest chrome driver
        self.chrome_path = ChromeDriverManager().install()
