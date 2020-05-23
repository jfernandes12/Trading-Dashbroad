import sched, time
import pandas as pd
import requests
from bs4 import BeautifulSoup

class bcolors :
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def start():
    indices = ["us-30", "nasdaq-composite", "us-spx-500"]


            
    def get_rsi(tick):
        page = requests.get('https://www.investing.com/indices/' + tick + "-technical", headers={"user-agent": "Chrome"})
        soup = BeautifulSoup(page.content, 'html.parser')
        summary = soup.find(id="techStudiesInnerWrap")
        name = soup.find("td", class_="first left symbol", string="RSI(14)")
        value = name.find_next('td')
        action = value.find_next('td')
        return  name.text, value.text, action.span.text

    name_list=[]
    rsi_list=[]
    action_list=[]
    
  
    
    for index in indices:
        name,rsi,action = get_rsi(index)
        name_list.append(name)
        rsi_list.append(rsi)
        action_list.append(action)
       
            
        
            
    rsi_action = {"INDEX": indices,"NAME":name_list,"RSI":rsi_list,"ACTION":action_list}
    my_rsi = zip(name_list, rsi_list, action_list)
    for it in my_rsi:
        n = it[0]
        r = it[1]
        p = it[2]
        if float(r) > 70:
            rsi_txt = f"{bcolors.WARNING}{r}{bcolors.ENDC}"
        else:
            rsi_txt = f"{bcolors.OKGREEN}{r}{bcolors.ENDC}"

        print(f"Name: {n} | RSI: {rsi_txt} | Action: {p}")


    df=pd.DataFrame.from_dict(rsi_action, orient='index')
    print(df.transpose())
    print("----------------------------------------------------\n")
    print("----------------------------------------------------\n")
    
    
while True:
    start()
    time.sleep(2)
    
    
