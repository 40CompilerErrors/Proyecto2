import requests
from bs4 import BeautifulSoup
import re

# class="review-content"
#?start=X where X = page_number*20
from Utilities.Scrappers import AbstractScrapper as AS


class YelScrapper(AS.AbstractScrapper):

    def scrapURL(self, URL):

        reviews = []
        current_page = 1

        page = requests.get(URL + "?start=0")
        soup = BeautifulSoup(page.content, 'html.parser')

        max_pages = soup.find('div', class_="page-of-pages")
        max_pages = re.search(' [0-9]*</div>', max_pages).group()[1:-6]
        max_pages = int(max_pages)

        print("NUMERO DE PAGINAS MAXIMO: " + str(max_pages))
        print("DENERIA SER INT: " + type(max_pages))

        while current_page <= max_pages:
            print("Currently searching page " + str(current_page))
            page = requests.get(URL + "?start=" + str((current_page-1) * 20))
            soup = BeautifulSoup(page.content, 'html.parser')

            searchResult = soup.find_all('div', class_="review-content")
            last_search = []

            current_page += 1
            if searchResult == [] or searchResult == last_search:
                print("No reviews on this page. Proceeding to review cleaning")
                break
            else:
                reviews = reviews + searchResult
                last_search = searchResult
                searchResult.clear()

        return self.__cleanupReviews(reviews)

    def __cleanupReviews(self,reviews):
        scores = []
        bodies = []

        for review in reviews:
            score = re.search('i-stars--regular-.', str(review)).group()[-1]
            scores.append(score)

            bodyHTML = review.find('p')
            cleanBody = re.sub(r'<.+?>', '', str(bodyHTML))
            bodies.append(cleanBody)

        return scores, bodies

if __name__ == "__main__":
    URL = "https://www.yelp.com/biz/el-sur-madrid"
    scrappy = YelScrapper()
    print(scrappy.scrapURL(URL))


