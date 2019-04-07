from abc import ABC, abstractmethod


class AbstractScrapper(ABC):

    @abstractmethod
    def scrapURL(self, url):
        score_list = []
        review_list = []
        print('UNIMPLEMENTED')
        return score_list, review_list