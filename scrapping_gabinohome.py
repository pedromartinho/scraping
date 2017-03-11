from bs4 import BeautifulSoup
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

filename=city+"_gabino_"+time.strftime("%H-%M-%S_%d-%m-%Y")+".csv"
fp = open(filename, 'w+')
fp.write("Email,Phone,Phone 2,Name,Country,City,Link,Notes,Campaign,SBA_id,type,date")
#first_page=""

auxi=city+"/"
get_page=link_page.split(auxi)

#if len(get_page)==1:
#    first_page=1
#else:
#    i=0
#    while i<=4:
#        if get_page[1][i]== "?" or get_page[1][i]== ".":
#            a=i
#            break
#        i=i+1
#    while i>0:
#        first_page=first_page+get_page[1][a-i]
#        i=i-1

first_page=int(get_page[1])
last_page=int(num_pages)+int(first_page)-1
for page in range(first_page,last_page+1):
    print(link_page)
    html_page=requests.get(link_page)
    data_page=html_page.text
    soup_page=BeautifulSoup(data_page,"html.parser")
    for offer_div in soup_page.find_all("div", { "class" : "list_advert " }):
        if offer_div.find("span", {"class" : "tot-photos"}):
            html_a=offer_div.find("a", {"class" : " external"})
            html_href=html_a.get('href')
            link_offer=html_href
            print(link_offer)
            html_offer=requests.get(link_offer)
            data_offer=html_offer.text
            soup_offer=BeautifulSoup(data_offer,"html.parser")

            if soup_offer.find ("div", {"id" : "client_side_name"}):
                html_name = soup_offer.find ("div", {"id" : "client_side_name"})
                name=html_name.find("a").text
                html_date = soup_offer.find ("ul", {"style" : "list-style:none; padding-left:10px;"})
                date = html_date.find_all("span", {"class" : "advert-stats-data"})[1].text

                if date.replace(" ","")=="":
                    date = html_date.find_all("span", {"class" : "advert-stats-data"})[3].text
                date="last update: "+date
                if soup_offer.find ("div", {"style" : "text-align:center;"}):
                    site2 = soup_offer.find ("div", {"style" : "text-align:center;"})
                    site2_a=site2.find("a")
                    site2_href=site2_a.get("href")
                    html_site2=requests.get(site2_href)
                    data_site2=html_site2.text
                    soup_site2=BeautifulSoup(data_site2,"html.parser")
                    botao = soup_site2.find ("div", {"class" : "block_NO"})
                    if botao.find("span"):
                        info_phone = botao.find("span").text
                        phone1 = info_phone.replace(" ","")
                        fp.write("\n,"+phone1+",,"+name+","+country+","+city+","+link_offer+","+notes+",,"+promocode+","+accomodation+","+date)

    added=city+"/"+str(page)
    var=link_page.replace(added,"")
    link_page=var+city+"/"+str(page+1)

fp.close()
