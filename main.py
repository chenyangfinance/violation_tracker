#https://www.goodjobsfirst.org/violation-tracker
import urllib.request
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import re
import time
import random
from fake_useragent import UserAgent
ua=UserAgent()
from tenacity import retry
import math

def get_info(name):
    url = r'https://violationtracker.goodjobsfirst.org/prog.php?parent='+ name
    # print(url)
    headers = {"User-Agent": ua.random}
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf8')
    p_name = re.compile(r'Parent Company Name(.*?)<div class="field field-type-', re.S)
    p_ticker = re.compile(r'ticker symbol (.*?)</div>', re.S)
    # p_penalty = re.compile(r'<b>(.*?)</b>', re.S)
    p_num = re.compile(r'Number of records(.*?)<div class="view-content">', re.S)
    try:
        name1 = p_name.findall(content)[0].split("</div>")[1]
        firm_name = name1.strip()
    except:
        firm_name = " "
    try:
        ticker = p_ticker.findall(content)[0].strip()
    except:
        ticker = " "
    # try:
    #     penalty = p_penalty.findall(content)[0]
    # except:
    #     penalty = " "
    try:
        num1 = p_num.findall(content)[0].split("</div>")[1]
        num = num1.strip()
    except:
        num = " "
    response.close()
    return firm_name,ticker,num

def read_page(page_num,firm_name, name, ticker, output):
    url = r'https://violationtracker.goodjobsfirst.org/prog.php?parent=' + name + "&page=" + str(page_num)
    # print(url)
    headers = {"User-Agent": ua.random}
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf8')
    # print(content)
    p_year = re.compile("<span class=\"date-display-single\">(\d\d\d\d)</span></td>")
    year = p_year.findall(content)
    # print(year)
    p_penalty = re.compile("\$(.*)</a></td>")
    penalty = p_penalty.findall(content)
    # print(penalty)
    for i in range(0,len(year)):
        output = output.append({'name' : firm_name , 'ticker' : ticker, 'year' : year[i], 'penalty': penalty[i]} , ignore_index=True)
        # print(output.head(10))
    return output


def loop(k,output):
    try:
        for i in range(k,df.shape[0]): #df.shape[0]
            # second = random.randint(0, 9)
            # time.sleep(second)
            name = df.iloc[i,0]
            firm_name, ticker, num = get_info(name)
            page = math.ceil(int(num.replace(',',''))/100)
            k = i
            print(k)
            for page_num in range(1, page +1):
                output = read_page(page_num,firm_name, name, ticker, output)
    except:
        time.sleep(5)
        print("loop" + str(k))
        loop(k,output)
    return output


df = pd.read_excel(r"C:\Users\cheny\Desktop\Python\vio\company_name.xlsx", header = None)
output = pd.DataFrame(columns=['name', 'ticker', 'year', 'penalty'])

output = loop(0,output)

output.to_csv("output.csv")

