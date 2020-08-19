#creat  a database of car : price ,year,milage
from bs4 import BeautifulSoup
import requests
import mysql.connector
import re
import json
import csv
from sklearn import tree
addres='https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117?LH_ItemCondition=3000%7C1000%7C2500&rt=nc&_dmd=1&_stpos=H7G0A1'
asdre='https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117?LH_ItemCondition=3000%7C1000%7C2500&rt=nc&_dmd=1&_pgn='
prices=[]
vechicles=[]
mileages=[]
years=[]
dup=[]
for i in range(1,20): #page
    if i==1:
        ad=addres
    else:
        ad=asdre+str(i)+'&_stpos=H7G0A1'
    r = requests.get(ad)
    soup = BeautifulSoup(r.text, 'html.parser')
    v_link = soup.find_all('a', attrs={'class':'s-item__link'})
    for j in range(len(v_link)):  # len(v_link)): #get each car go tolink and get info
        r2 = requests.get(v_link[j]['href'])
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        t = soup2.find_all('h1', attrs={'itemprop': "name"})

        # year
        z = soup2.find_all('td', attrs={'width': "50.0%"})
        res = re.search(r'>(\d+)', str(z[1]).strip())
        if res == None:
            continue

        x, y = res.span()
        year = ''
        for qq in str(z[1])[13:].strip():
            if qq.isnumeric():
                year = year + qq
        years.append(int(year))
    # milage
        res = re.search(r'>(\d+)', str(z[3]).strip())
        if res == None:
            years.pop()
            continue
        x, y = res.span()

        mileage = ''
        for qq in str(z[3])[13:].strip():
            if qq.isnumeric():
                mileage = mileage + qq

        mileages.append(int(mileage))
#avoid duplicate save 
        if mileage+year in dup :
            years.pop()
            mileages.pop()
            continue
        dup.append(mileage+year)


    #price
        p=soup2.find('span',attrs={'itemprop':'price'})
        res=re.search(r'\$.*\d',str(p))
        x, y = res.span()
        prices.append(float(str(p)[x+1:y].replace(',','',3)))



        print(str(len(years))+'  car')
cnx=mysql.connector.connect(user='root', password='',
                            host='127.0.0.1',
                            database='siavash')
cursor=cnx.cursor()
cursor.execute('SET CHARACTER SET utf8')
cnx.commit()
for j in range(len(years)):
    cursor.execute('INSERT INTO car VALUES(%f,%i,%i)'  %(prices[j],years[j],mileages[j]))
    cnx.commit()
cnx.close()


cnx=mysql.connector.connect(user='root', password='',
                            host='127.0.0.1',
                            database='siavash')
mycursor=cnx.cursor()
mycursor.execute('SET CHARACTER SET utf8')
cnx.commit()
mycursor.execute("SELECT * FROM car")
myresult = mycursor.fetchall()
cnx.close()

y=[]
x=[]
for i in range(len(myresult)):
    x.append(myresult[i][1:3])
    y.append(myresult[i][0])
clf=tree.DecisionTreeRegressor()
clf=clf.fit(x,y)

newdata=[[0,0]]
#newdata=[[year,mileage]]
newdata[0][0]=int(input('enter year: '))
newdata[0][1]=int(input('enter mileage: '))
ans=(clf.predict(newdata))
print('ML think that price is:',str(ans[0]))

