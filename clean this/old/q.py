import quandl 
import datetime
import requests


quandl.ApiConfig.api_key = 'Er6qAesj6gapbujojxLJ'
today = datetime.datetime.today()

def getter(code): 
    api_link = f"https://www.quandl.com/data/{code}"
    r = requests.get(api_link)
    print(api_link)
    print(r.text)
    pass

if __name__ == "__main__": 
    code = "HKEX/HSIZ2020"
    getter(code)