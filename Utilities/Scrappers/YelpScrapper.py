import requests
from bs4 import BeautifulSoup
import re

# class="review-content"
#?start=X where X = page_number*20
from Utilities.Scrappers import AbstractScrapper as AS


class YelScrapper(AS.AbstractScrapper):

    def scrapURL(self, URL):

        reviews = None
        current_page = 1

        while True:
            print("Currently searching page " + str(current_page))
            page = requests.get(URL + "?start=" + str((current_page-1) * 20))
            soup = BeautifulSoup(page.content, 'html.parser')
            searchResult = soup.find_all('div', class_="review-content")
            current_page += 1
            if searchResult == []:
                print("No reviews on this page. Proceeding to review cleaning")
                break

            if reviews == None:
                reviews = searchResult
            else:
                reviews = reviews + searchResult

        print(len(reviews))
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


