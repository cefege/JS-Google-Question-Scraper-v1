"""Importing playwright_scrapper from gscraper folder."""
from gscraper import playwright_scrapper
# pylint: disable=R0902,R0903

class GoogleScrapper:
    """GoogleScrapper class."""
    def __init__(self, query, main_query):
        # query string question to scrap paa for
        self.query = query
        self.main_query = main_query
        # number of questions to scrape
        self.max_questions = 4
        # creating lists to put results in later
        self.paa_titles, self.texts, self.urls, \
        self.url_titles,self.results_count,\
        self.related_srch = [], [], [], [], [], []

    def google_scrape(self):
        """Method for running the program
         and sorting gotten results."""
        # we get our results in result variable as dictionary
        result = playwright_scrapper.scrapper_g(
            query=self.query,
            num_questions_to_scraper=self.max_questions,
            headless_mode=False,
            proxy='139.180.229.84:4444:cefege:kZxSgVUN')
        # we extract related questions from our dictionary
        # and put them to the related questions list
        related_questions = result['related_questions']
        # we extract related searches from our dictionary
        self.related_srch = result['related_searches']
        # we extract results count from dictionary
        self.results_count = result['results_count']
        # we extract paa titles,answers,urls,url titles
        # from related questions list
        # and add them to their own lists
        # created in the __init__ main function
        for i in related_questions:
            self.paa_titles.append(i['question'])
            self.texts.append(i['answer'])
            if 'link' in i.keys():
                self.urls.append(i['link'])
            else:
                self.urls.append('https://www.wikipedia.org/')
            if 'title' in i.keys():
                self.url_titles.append(i['title'])
            else:
                self.url_titles.append('Wikipedia')
        # we return all lists with results
        return self.related_srch,self.paa_titles,\
               self.texts,self.urls,\
               self.url_titles,self.results_count

# Example of running the program
GoogleScrapper(
    query='how to squat properly',
    main_query='blabla').google_scrape()
