import requests
from bs4 import BeautifulSoup



from pymongo import MongoClient
try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:  
    print("Could not connect to MongoDB")

db= conn.dbdemo

collection = db.news

url = 'https://news.ycombinator.com/'

r=requests.get(url)
htmlContent=r.content

#STEP 2 : PARSE THE HTML
soup=BeautifulSoup(htmlContent,'html.parser')
#open("video.html", "w", encoding='utf8').write(str(soup))

script=soup.find_all('a',class_="storylink")
t = [x.text for x in script]

s1=soup.find_all('td',class_="subtext")
p=[x.text for x in s1]

dict={}

for (a,b) in zip(t,p):
	title=a
	b1=b.split()
	try:
		point=b1[0]+" "+b1[1]+" "+b1[2]+" "+b1[3]
		date=b1[4]+" "+b1[5]+" "+b1[6]
		comment=b1[10]+" "+b1[11]
		dict={"title":title,"point":point,"date":date,"comment":comment}
		rec_id1 = collection.insert_one(dict)
		continue
	except IndexError:
		pass


for page in range(2,24):

	r=requests.get(url+"news?p="+str(page))
	htmlContent=r.content

	#STEP 2 : PARSE THE HTML
	soup=BeautifulSoup(htmlContent,'html.parser')
	#open("video.html", "w", encoding='utf8').write(str(soup))

	script=soup.find_all('a',class_="storylink")
	t = [x.text for x in script]

	s1=soup.find_all('td',class_="subtext")
	p=[x.text for x in s1]

	dict={}

	for (a,b) in zip(t,p):
		title=a
		b1=b.split()
		try:
			point=b1[0]+" "+b1[1]+" "+b1[2]+" "+b1[3]
			date=b1[4]+" "+b1[5]+" "+b1[6]
			comment=b1[10]+" "+b1[11]
			dict={"title":title,"point":point,"date":date,"comment":comment}
			rec_id1 = collection.insert_one(dict)
			continue
		except IndexError:
			pass






