from bs4 import BeautifulSoup
import requests
import sys
import time

link_page=sys.argv[1]
pages_decimal=sys.argv[2]

get_separation=link_page.split("==&anut=")
get_page=get_separation[1].split("&mut=")

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

first_page=int(get_page[0])
n_pages= int(pages_decimal)
aux=first_page

filename="Bquarto_contactos"+time.strftime("%H-%M-%S_%d-%m-%Y")+"__"+get_page[0]+".csv"
fp = open(filename, 'w+')
fp.write("Nome,Phone,Email,Zona,Date")

for page in range(first_page,first_page+n_pages):
    print(link_page)
    html_page=requests.get(link_page)
    data_page=html_page.text
    soup_page=BeautifulSoup(data_page,"html.parser")
    for offer_div in soup_page.find_all("div", { "id" : "centro_anu" }):
        html_a=offer_div.find("a")
        html_href=html_a.get('href')
        link_offer= "https://www.bquarto.pt/"+html_href
        html_offer=requests.get(link_offer)
        data_offer=html_offer.text
        soup_offer=BeautifulSoup(data_offer,"html.parser")

        for html_info in soup_offer.find_all("div", {"id" : "dados_des"}):
            if html_info.find("li", {"class" : "esc_b"}):
                html_name = html_info.find("li", {"class" : "esc_b"})
                if html_info.find("li", {"class" : "esc_a"}):
                    html_header = html_info.find("li", {"class" : "esc_a"})
                    if html_header.text == "Email:":
                        email=html_name.text
                        email=email.replace("\n","")
                    if html_header.text == "Nome:":
                        name=html_name.text
                        print(name)
            if html_info.find("li", {"class" : "esc_i"}):
                html_name1 = html_info.find("li", {"class" : "esc_i"})
                if html_info.find("li", {"class" : "esc_h"}):
                    html_header1 = html_info.find("li", {"class" : "esc_h"})
                    if html_header1.text == "Telefone(s):":
                        telefone=html_name1.text
                        telefone=telefone.replace(" ","")

                    if html_header1.text == "A partir de: ":
                        data=html_name1.text
                        data=data.replace("\n","")
                        data=data.replace(" ","")

            if html_info.find("li", {"class" : "esc_h"}):
                html_zona = html_info.find("li", {"class" : "esc_h"})
                if html_zona.text == " 1ª Zona: ":
                    html_zona_info = html_info.find("li", {"class" : "esc_b"})
                    zona=html_zona_info.text
                    zona=zona.replace("\n","")
                    zona=zona.replace(","," ")
                    print(zona)

        fp.write("\n"+name+","+telefone+","+email+","+zona+","+data)
    aux=aux+10
    added="==&anut="+str(aux)+"&mut=10"

    link_page=get_separation[0]+added
fp.close()
