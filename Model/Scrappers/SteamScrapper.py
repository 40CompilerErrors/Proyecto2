import requests
from bs4 import BeautifulSoup
import re
import urllib.request, json
from Model.Scrappers import AbstractScrapper as AS

class SteamScrapper(AS.AbstractScrapper):


    def scrapReviews(self, games=[], language="english", batch_size=100):
        if not games:
            games.append(input("Type the title of a game to download the comments of: "))

        allReviews = []
        for name in games:
            gameID = self.__getGameID(name)
            rawReviews = self.__getReviews(gameID,language,batch_size)
            gameReviews = self.__filterReviews(rawReviews)
            allReviews = allReviews + gameReviews

        return allReviews

    def scrapURL(self, url, language="english",batch_size=100):
        #get the url https://store.steampowered.com/app/814380/Sekiro_Shadows_Die_Twice/
        gameID = re.search(r'app/.*?/' , url).group()[4:-1]
        rawReviews = self.__getReviews(gameID, language, batch_size)
        gameReviews = self.__filterReviews(rawReviews)


        return self.__splitLists(gameReviews)

    def __splitLists(self,gameReviews):
        starList, reviewList = [],[]
        for item in gameReviews:
            if item['positive'] == True:
                starList.append("4")
            else:
                starList.append("2")
            reviewList.append(item['review'])

        return starList, reviewList


    def __getGameID(self,game):
        page = requests.get('https://store.steampowered.com/search/?term=' + game)
        soup = BeautifulSoup(page.content, 'html.parser')

        searchResult = soup.find('a', class_="search_result_row")

        gameURL = re.search('href=".*?"', str(searchResult)).group()[6:-1]
        gameID = re.search('app/\d*?/', str(gameURL)).group()[4:-1]

        return gameID

    def __getReviews(self,gameID,language,batch_size):
        with urllib.request.urlopen(" https://store.steampowered.com/appreviews/" + gameID
                                    + "?json=1&filter=recent&language=" + language
                                    +"&num_per_page=" + str(batch_size)) as url:
            opinionDict = json.loads(url.read().decode())

        rawReviews = opinionDict["reviews"]

        return rawReviews

    def __filterReviews(self,rawReviews):
        filteredReviews = []

        for raw in rawReviews:
            filtered = {}
            filtered["review"] = raw["review"]
            filtered["positive"] = raw["voted_up"]
            filteredReviews.append(filtered)

        return filteredReviews


if __name__ == "__main__":
    URL ="https://store.steampowered.com/app/814380/Sekiro_Shadows_Die_Twice/"
    scrapper = SteamScrapper()
    print(scrapper.scrapURL(URL))



    # print("Eexecuted SteamScrapper as script: Testing purposes only")
    # scrapper = SteamScrapper()
    # tests = []
    #
    # print("Testing without a given name")
    # noNameTest = 100 == len(scrapper.scrapReviews())
    # print(noNameTest)
    # tests.append(noNameTest)
    #
    # print("Testing with a given name")
    # singleNameTest = 100 == len(scrapper.scrapReviews(games =["Sekiro"]))
    # print(singleNameTest)   #If you give it a string only seems to do it a LOT???
    # tests.append(singleNameTest)
    #
    # print("Testing with a list of names")
    # nameListTest = 300 == len(scrapper.scrapReviews(games=["Sekiro","Team Fortress","Dota 2"]))
    # print(nameListTest)
    #
    # print("Testing with different batch sizes")
    # batchSizeTest = 60 == len(scrapper.scrapReviews(games=["Sekiro", "Team Fortress", "Dota 2"],batch_size=20))
    # print(batchSizeTest)
    #
    # if not False in tests:
    #     print("All tests successful.")
    # else:
    #     print("Some tests failed. Make sure to fix it.")


