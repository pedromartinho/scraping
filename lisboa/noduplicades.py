import requests
import sys
import time

new=sys.argv[1]
old=sys.argv[2]


filename="Bquarto_contactos_new"+time.strftime("%d-%m")+".csv"
fp = open(filename, 'w+')
fp.write("Nome,Phone,Email,Zona,Date")
fread_new= open(new, 'r')
x=0
y=0
for line in fread_new:
    fread_old= open(old, 'r')
    segmentation2=line.split(",")
    date=segmentation2[4]
    for lineOld in fread_old:
        segmentation=lineOld.split(",")
        if segmentation[2] not in line:
            print("no duplicate here")
        else:
            x_str=str(x)
            print("Duplicade - "+x_str)
            x=x+1
            y=1
    if y==0 :
        if "2017" in date:
            if "January" in date:
                print("too late!!")
            elif"February" in date:
                print("too late!!")
            elif"March" in date:
                print("too late!!")
            elif"April" in date:
                print("too late!!")
            else:
                fp.write(line)
        elif "2018" in date:
            fp.write(line)
        else:
            print("too late!!")
    else:
        y=0
    fread_old.close()
fread_new.close()
fp.close()
