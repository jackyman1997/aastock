from .SeleniumWebDriverSetup import ChromeSetup
import datetime
from selenium import webdriver  # main
from selenium.webdriver import ActionChains  # for click on page
import json
import pathlib
from pyvirtualdisplay import Display


class AAstock(ChromeSetup):
    ''' only minute data for now '''

    def __init__(
        self,
        url: str,
        headless: bool = False,
        filename: str = '',
        filetype: str = 'json',
        foldername: str = 'output',
    ):
        self.xpaths = {
            'chart': '//*[@id="stockChart_chart_container"]',
            'button_nighttime': '//*[@id="AHFTControl"]/div[2]',
            'button_1min': '//*[@id="jsPeriodPanel"]/div[1]',
            'button_zoomout': '//*[@id="dcDrawingTools2"]/div[2]',
            'button_zoomin': '//*[@id="dcDrawingTools2"]/div[1]/div',
            'Name': '//*[@id="divLabelS"]',
            'Datetime': '//*[@id="divLabelD"]',
            'O': '//*[@id="divLabelO"]',
            'H': '//*[@id="divLabelH"]',
            'L': '//*[@id="divLabelL"]',
            'C': '//*[@id="divLabelC"]',
            'Turn': '//*[@id="divLabelTurn"]',
            'Vol': '//*[@id="divLabelVol"]'
        }
        super().__init__(headless=headless)  # chrome driver setup

        with Display(visible=False, size=(800, 600)) as disp:  # virture display setup

            with webdriver.Chrome(
                executable_path=self.chrome_path,
                options=self.chrome_options) as self.driver:  # start chrome driver
                self.driver.get(url)  # start webpage
                self.chart = self.driver.find_element_by_xpath(
                    self.xpaths['chart'])  # locate dynamic chart, and get size
                print(self.chart.location, self.chart.size)
                self.name_of_this = self.driver.find_element_by_xpath( 
                    self.xpaths['Name']).text  # get the name of this future/stock

                try:  # clicks for ignore night data
                    self._click(self.xpaths['button_nighttime'])
                except:
                    pass

                # clicks for getting 1 min period
                self._click(self.xpaths['button_1min'])
                self._click(self.xpaths['button_zoomout'], n_times=10)
                self._click(self.xpaths['button_zoomin'])
                self.driver.execute_script(
                    f'window.scrollTo(0, {self.chart.location["y"]})') # move and capture

                # traverse through the width of the dynamic chart
                raw = []
                for offset in range(self.chart.size['width']):
                    self._moveCursor(offset)
                    row = self._captureData()
                    if offset == 0:  # inital capture, XXX: should be better code here
                        raw.append(row)
                    if raw[-1]['Time'] != row['Time']:  # only store when datetime is different
                        raw.append(row)

        # data preprocessing, XXX: temporarily codes
        # 1. clean date
        newestDate = raw[-1]['Date']  # last item must be the newere date
        new = [row for row in raw if row['Date'] == newestDate]
        # 2. remove duplicate, after some tests, sometimes the last item repeated at the first location of the last
        if new[0]['Time'] == '16:30' or new[0]['Time'] == '16:00':
            new.pop(0)
        # 3. check sum, for future -> 377 elements in list, for stocks -> 330
        if len(new) != 377 and len(new) != 330:
            print(f'some data is missing, {len(new)}')

        # export
        self._setFilenameAndType(name=filename, filetype=filetype)
        self._export(item=new, folder=foldername)

    def _setFilenameAndType(self, name: str, filetype: str):
        now = datetime.datetime.now()  # name by time now
        filename = str(now.year) + str(now.month) + str(now.day) + \
            '-' + str(now.hour) + str(now.minute) + str(now.second)
        if name == '':
            name = self.name_of_this
        self.filename = name + '-' + filename
        if filetype != "json":
            raise NotImplementedError(
                "Please use json, other filetypes are not implemented.")
        else:
            self.filetype = filetype

    def _click(self, xpath: str, n_times: int = 1):
        for _ in range(n_times):
            ActionChains(self.driver).click(
                self.driver.find_element_by_xpath(xpath)).perform()

    def _moveCursor(self, offset):
        ActionChains(self.driver).move_to_element_with_offset(
            self.chart,
            xoffset=offset,
            yoffset=5
        ).click().perform()

    def _captureData(self) -> dict:
        row = {}
        for key in ['Datetime', 'O', 'H', 'L', 'C', 'Turn', 'Vol']:
            if key != 'Datetime':
                row[key] = self.driver.find_element_by_xpath(
                    self.xpaths[key]).text
                if 'K' in row[key]:
                    row[key] = round(
                        float(row[key].replace('K', ''))*1000, ndigits=2)
                elif 'M' in row[key]:
                    row[key] = round(
                        float(row[key].replace('M', ''))*1000000, ndigits=2)
                else:
                    row[key] = float(row[key])
            else:
                datetime = self.driver.find_element_by_xpath(
                    self.xpaths[key]).text.split()
                row['Date'] = datetime[0]
                row['Time'] = datetime[1]
        return row

    def _export(self, item, folder: str):
        pathlib.Path(f'./{folder}').mkdir(exist_ok=True)  # create new folder
        self.filepath = f'./{folder}/{self.filename}.{self.filetype}'
        with open(self.filepath, 'w') as f:
            if self.filetype == 'json':
                f.write(json.dumps(item, indent=1))
            else: 
                raise NotImplementedError(
                    "Please use json, other filetypes are not implemented.")
