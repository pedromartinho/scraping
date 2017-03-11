from bs4 import BeautifulSoup
from time import sleep
import requests
import sys
import time

link_page=sys.argv[1]
num_pages=sys.argv[2]
country=sys.argv[3]
city=sys.argv[4]
notes=sys.argv[5]
accomodation=sys.argv[6]
promocode=sys.argv[7]

filename=city+"_grandemercado_"+time.strftime("%H-%M-%S_%d-%m-%Y")+".csv"
fp = open(filename, 'w+')
fp.write("Email,Phone,Phone 2,Name,Country,City,Link,Notes,Campaign,SBA_id,type,date")
first_page=""
get_page=link_page.split("/p")

i=0
while i<=4:
    if get_page[1][i]== ".":
        a=i
        break
    i=i+1
while i>0:
    first_page=first_page+get_page[1][a-i]
    i=i-1
first_page=int(first_page)
last_page=int(num_pages)+int(first_page)-1
for page in range(first_page,last_page+1):
    print(link_page)

    html_page=requests.get(link_page)
    data_page=html_page.text
    soup_page=BeautifulSoup(data_page,"html.parser")
    for offer_div in soup_page.find_all("td", { "class" : "titulo " }):
        html_a=offer_div.find("a")
        link_offer=html_a.get('href')

        html_offer=requests.get(link_offer)
        data_offer=html_offer.text
        soup_offer=BeautifulSoup(data_offer,"html.parser")
        if soup_offer.find("img", { "id" : "img_grande_id"}):

            if len(soup_offer.find_all("div", {"class" : "descr_box" })[5].text)>2:
                if len(soup_offer.find_all("div", {"class" : "descr_box" })[6].text)>2:
                    print(link_offer)
                    name=soup_offer.find_all("div", {"class" : "descr_box" })[5].text
                    print(name)
                    phone_1=soup_offer.find_all("div", {"class" : "descr_box" })[6].text
                    phone_1=phone_1.replace(" ", "")
                    print(phone_1)
                    date=soup_offer.find_all("div", {"class" : "descr_box" })[2].text
                    date="update: "+date
                    print(date)
                    fp.write("\n,"+phone_1+",,"+name+","+country+","+city+","+link_offer+","+notes+",,"+promocode+","+accomodation+","+date)
    added="/p"+str(page)
    var=link_page.split(added)
    link_page=var[0]+"/p"+str(page+1)+".htm"
fp.close()
