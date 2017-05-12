import requests
import sys
import time

city=sys.argv[1]
n_merge=sys.argv[2]

n=int(n_merge)

filename="Bquarto_contactos_"+city+"_"+time.strftime("%H-%M-%S_%d-%m-%Y")+".csv"
fp = open(filename, 'w+')
fp.write("Nome,Phone,Email,Zona,Date")
for x in range(1,n+1):
    n_merge=str(x)
    fread= open(n_merge+".csv", 'r')
    for line in fread:
        fp.write(line)
    fread.close()
fp.close()
