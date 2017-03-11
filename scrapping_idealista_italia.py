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

filename=city+"_idealista_"+time.strftime("%H-%M-%S_%d-%m-%Y")+".csv"
fp = open(filename, 'w+')
fp.write("Email,Phone,Phone 2,Name,Country,City,Link,Notes,Campaign,SBA_id,type,date")
first_page=""
get_page=link_page.split("lista-")
if len(get_page)==1:
    first_page=1
else:
    i=0
    while i<=4:
        if get_page[1][i]== "?" or get_page[1][i]== ".":
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
    for offer_div in soup_page.find_all("div", { "class" : "item-info-container" }):

        html_a=offer_div.find("a", {"class" : "item-link"})
        html_href=html_a.get('href')
        link_offer= "https://www.idealista.it"+html_href
        print(link_offer)
        html_offer=requests.get(link_offer)
        data_offer=html_offer.text
        soup_offer=BeautifulSoup(data_offer,"html.parser")
        if soup_offer.find("div", { "class" : "placeholder-multimedia image horizontal printable " }) or soup_offer.find("div", { "class" : "placeholder-multimedia image vertical printable " }):
            if soup_offer.find ("div", {"class" : "phone first-phone"}):
                html_name = soup_offer.find ("div", {"class" : "advertiser-data txt-soft"})
                name=html_name.find("p")
                var=name.text.split(" - ")
                landlord_type=var[0].replace(" ","")
                if landlord_type == "Privato":
                    name=var[1].replace(" ","")
                    html_contact_1=soup_offer.find("p", {"class" : "txt-bold _browserPhone icon-phone"})
                    contact_1=html_contact_1.text.split(" ")
                    if len(contact_1)==6:
                        phone_1= contact_1[0]+contact_1[2]+contact_1[3]+contact_1[4]+contact_1[5]
                        phone_1=phone_1.replace(" ","")
                    if len(contact_1)==7:
                        phone_1= contact_1[0]+contact_1[3]+contact_1[4]+contact_1[5]+contact_1[6]
                        phone_1=phone_1.replace(" ","")
                        print(phone_1)
                    else:
                        phone_1=html_contact_1.text.replace(" ","")

                    html_date=soup_offer.find("section", {"id" : "stats"})
                    date=html_date.find("p")
                    date=date.text
                    date_aux=" (offer from link: "+link_page+")"
                    date=date+date_aux

                    phone_2=""
                    if soup_offer.find("p", {"class" : "txt-bold _browserPhone"}):
                        html_contact_2=soup_offer.find("p", {"class" : "txt-bold _browserPhone"})
                        contact_2=html_contact_2.text.split(" ")
                        if len(contact_2)==6:
                            phone_2=contact_2[0]+contact_2[2]+contact_2[3]+contact_2[4]+contact_2[5]
                            phone_2=phone_2.replace(" ","")
                        if len(contact_2)==7:
                            phone_2=contact_2[0]+contact_2[3]+contact_2[4]+contact_2[5]+contact_2[6]
                            phone_2=phone_2.replace(" ","")
                            print(phone_2)
                        else:
                            phone_2=html_contact_2.text.replace(" ","")
                    fp.write("\n,"+phone_1+","+phone_2+","+name+","+country+","+city+","+link_offer+","+notes+",,"+promocode+","+accomodation+","+date)
    if page==1:
    ula    var=link_page.split("?")
        if len(var)==1:
            var=link_page.split("lista-1.htm")
            added="lista-2.htm"
        else:
            added="lista-2?"
        link_page=var[0]+added+var[1]
    else:
        added="lista-"+str(page)
        var=link_page.split(added)
        link_page=var[0]+"lista-"+str(page+1)+var[1]
fp.close()
