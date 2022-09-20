from bs4 import BeautifulSoup
import schedule
import time
import requests
import mysql.connector

def scrapping():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bs4"
    )
    mycursor = mydb.cursor()

    source=requests.get('https://www.careerpointkenya.co.ke/jobs/')
    source.raise_for_status()
    html_parser=BeautifulSoup(source.text,'html.parser')
    jobs=html_parser.find('div',class_='fusion-posts-container-pagination').find_all('article')
    for jobs in jobs:
        job=jobs.find('div',class_='fusion-post-content post-content').h2.a.text
        details=jobs.find('div',class_='fusion-post-content-container').p.text
        date=jobs.find('span',class_='updated').text
        link=jobs.find('h2',class_='blog-shortcode-post-title').a.get('href')
    
        sql = "INSERT INTO jobs (job, details,link,date) VALUES (%s, %s,%s,%s)"
        val = (job,details,link,date)
        mycursor.execute(sql,val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

schedule.every(24).hours.do(scrapping)
while 1:
    schedule.run_pending()
    time.sleep(1)