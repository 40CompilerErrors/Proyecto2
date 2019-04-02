# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 09:35:22 2019

@author: javie
"""

import requests
import re
from bs4 import BeautifulSoup


url = "https://www.metacritic.com/movie/the-lord-of-the-rings-the-return-of-the-king"
movie = False

if re.search("https://www.metacritic.com/game/.*/.*", url):
    print("It's a game")
elif re.search("https://www.metacritic.com/music/.*/.*", url):
    print("It's music")
elif re.search("https://www.metacritic.com/tv/.*", url):
    print("It's a tv show")
elif re.search("https://www.metacritic.com/movie/.*", url):
    movie = True
    print("It's a movie")
else:
    print("Invalid syntax")

page = requests.get(url, headers=      {'User-Agent': 'Mozilla/5.0'})
page = page.content.decode('utf-8')
page = page.replace("<br>","\n")   
page = page.replace("<br/>","\n")                       
soup = BeautifulSoup(page, 'html.parser')
html = list(soup.children)[2]
html = (list(html))
i = 0
j = 0
h = 0
starList = []
contentList = []
    
if movie == True:
    
    userReviews = soup.find("a", string="User Score")
    userReviews = userReviews['href']
    userReviews = str(userReviews)
    
    url = "https://www.metacritic.com"+userReviews
    page = requests.get(url, headers=      {'User-Agent': 'Mozilla/5.0'})
    page = page.content.decode('utf-8')
    page = page.replace("<br>","\n")   
    page = page.replace("<br/>","\n")                   
    soup = BeautifulSoup(page, 'html.parser')
    html = list(soup.children)[2]
    reviewList = soup.findAll("div", {"class": "review"})
    
    pages = soup.find("div", {"class": "page_nav"})
    
    for i in range(len(reviewList)):
        star = reviewList[i].find("div", {"class": "metascore_w"})
        starList.append(float(star.text))
        content = reviewList[i].find("div", {"class": "review_body"})
        content = content.find("span")
        contentList.append(content.text)
        
    if pages:
        
        nextpage = soup.find("a", {"rel": "next"})
        
        while nextpage:
            nextpage = nextpage['href']
            url2 = "https://www.metacritic.com"+nextpage
            page2 = requests.get(url2, headers=      {'User-Agent': 'Mozilla/5.0'})  
            page2 = page2.content.decode('utf-8')
            page2 = page2.replace("<br>","\n")   
            page2 = page2.replace("<br/>","\n")                 
            soup2 = BeautifulSoup(page2, 'html.parser')
            html2 = list(soup2.children)[2]
            reviewList2 = soup2.findAll("div", {"class": "review"})
            
            for i in range(len(reviewList2)):
                star = reviewList2[i].find("div", {"class": "metascore_w"})
                starList.append(float(star.text))
                content = reviewList2[i].find("div", {"class": "review_body"})
                content = content.find("span")
                contentList.append(content.text)
                
            nextpage = soup2.find("a", {"rel": "next"})
else:
    criticReviews = soup.find("a", string="Critic Reviews")
    criticReviews = criticReviews['href']
    criticReviews = str(criticReviews)
    
    url1 = "https://www.metacritic.com"+criticReviews
    page1 = requests.get(url1, headers=      {'User-Agent': 'Mozilla/5.0'}) 
    page1 = page1.content.decode('utf-8')
    page1 = page1.replace("<br>","\n")   
    page1 = page1.replace("<br/>","\n")                  
    soup1 = BeautifulSoup(page1, 'html.parser')
    html1 = list(soup1.children)[2]
    
    reviewList1 = soup1.findAll("li", {"class": "critic_review"})
    
    for i in range(len(reviewList1)):
        star = reviewList1[i].find("div", {"class": "metascore_w"})
        
        if star.text:
            star = float(star.text)/10
            starList.append(star)
            content = reviewList1[i].find("div", {"class": "review_body"})
            contentList.append(content.text)
    
    userReviews = soup.find("a", string="User Reviews")
    userReviews = userReviews['href']
    userReviews = str(userReviews)
    
    url2 = "https://www.metacritic.com"+userReviews
    page2 = requests.get(url2, headers=      {'User-Agent': 'Mozilla/5.0'})
    page2 = page2.content.decode('utf-8')
    page2 = page2.replace("<br>","\n")   
    page2 = page2.replace("<br/>","\n")             
    soup2 = BeautifulSoup(page2, 'html.parser')
    html2 = list(soup2.children)[2]
    
    pages = soup2.find("ul", {"class": "pages"})
    
    reviewList2 = soup2.findAll("li", {"class": "user_review"})
       
    for j in range(len(reviewList2)):
        star = reviewList2[j].find("div", {"class": "metascore_w"})
        starList.append(float(star.text))
        content = reviewList2[j].find("div", {"class": "review_body"})
        contentList.append(content.text)
            
    if pages:
        
        nextpage = soup2.find("a", {"rel": "next"})
        
        while nextpage:
            nextpage = nextpage['href']
            url3 = "https://www.metacritic.com"+nextpage
            page3 = requests.get(url3, headers=      {'User-Agent': 'Mozilla/5.0'})                   
            page3 = page3.content.decode('utf-8')
            page3 = page3.replace("<br>","\n")   
            page3 = page3.replace("<br/>","\n")   
            soup3 = BeautifulSoup(page3, 'html.parser')
            html3 = list(soup3.children)[2]
            
            
            
            reviewList3 = soup3.findAll("li", {"class": "user_review"})
               
            for h in range(len(reviewList3)):
                star = reviewList3[h].find("div", {"class": "metascore_w"})
                starList.append(float(star.text))
                content = reviewList3[h].find("div", {"class": "review_body"})
                contentList.append(content.text)
                
            nextpage = soup3.find("a", {"rel": "next"})

print(starList[-1])
print(contentList[-1])