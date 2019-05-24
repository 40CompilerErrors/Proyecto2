import requests
from bs4 import BeautifulSoup
import re
import urllib.request, json
from Model.Scrappers import AbstractScrapper as AS
from urllib.request import urlopen
import urllib.request
# class="review-content"
#?start=X where X = page_number*20

class AmazonScrapper(AS.AbstractScrapper):

    def scrapURL(self, URL):

        current_page = 1
        total_reviews_int = 2
        starList = []
        contentList = []
        
        step = re.search('.*?/ref', URL).group()[:-4]
        step2 = re.sub('dp', 'product-reviews', step)
        page_reviews = step2 + '/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=' + str(1)
        request = urllib.request.Request(page_reviews, headers={"Accept" : "text/html"})


        codigo_html = urllib.request.urlopen(request).read()
        page_content = BeautifulSoup(codigo_html, 'html.parser')
        rgx = 'total-review-count'
        total_reviews = page_content.find('span', attrs={'data-hook': rgx})
        print(total_reviews.getText())
        total_reviews_final = re.sub(',', '', total_reviews.getText())
        total_reviews_int = int(total_reviews_final)


        while len(contentList) < total_reviews_int:

            # ppp = 'https://www.amazon.com/Apple-iPhone-Plus-Unlocked-64GB/product-reviews/B0775FLHPN/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=1'
            # page_link = 'https://www.amazon.com/Apple-iPhone-Plus-Unlocked-64GB/dp/B0775FLHPN/ref=br_asw_pdt-3?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=&pf_rd_r=12JGPX8WVMY0E6H1DE86&pf_rd_t=36701&pf_rd_p=74c2af8b-5acb-4bf8-b252-8b1584c94b14&pf_rd_i=desktop'
            # page_reviews = re.sub('dp', 'product-reviews', page_link)
            step = re.search('.*?/ref', URL).group()[:-4]
            step2 = re.sub('dp', 'product-reviews', step)
            page_reviews = step2 + '/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=' + str(current_page)
            request = urllib.request.Request(page_reviews, headers={"Accept" : "text/html"})

            codigo_html = urllib.request.urlopen(request).read()
            page_content = BeautifulSoup(codigo_html, 'html.parser')

            print(current_page)

            reviews = page_content.findAll('div', class_='a-row a-spacing-small review-data')
            regex = 'review-star-rating'
            puntuacion = page_content.findAll('i', attrs={'data-hook': regex})

            for i in puntuacion:
                starList.append(i.getText()[0])

            for div in reviews:
                contentList.append(div.getText().split('\n')[0])

            current_page += 1

        return starList, contentList



if __name__ == "__main__":
    URL = 'https://www.amazon.com/Clarks-Tilden-Style-black-leather/dp/B078GZB11J/ref=lp_18637582011_1_1?srs=18637582011&ie=UTF8&qid=1554809371&sr=8-1#customerReviews'
    scrappy = AmazonScrapper()
    print(scrappy.scrapURL(URL))