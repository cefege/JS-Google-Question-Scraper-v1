"""DUMMY STRING"""
import sys
# import json
import re
from bs4 import BeautifulSoup
# pylint: disable=W1401,W0702,W0703,R1702,R0903,R0915,R0912,W0201,W0107,R0902,R0914,R1705,R1710
class Scrapper():
    """Scrapper main class"""
    def __init__(self,query,num_questions_to_scraper,page_content):
        try:
            # number of question to scrape
            self.num_questions_to_scraper = num_questions_to_scraper
            # string question to scrape paa for
            self.questionn = query
            self.query = query
            # we replace empty space with + in url
            self.query = self.query.replace(' ','+').replace('  ','+')
            # setting beautifulsoup variable , loading our html
            self.soup = BeautifulSoup(page_content, "html.parser")
            # creating lists
            self.answer_box, self.data2, self.questions, self.related_search,\
            self.snippet, self.displayed_text1, self.link1,\
            self.titles,\
            self.unscraped_questions = [], [], [], [], [], [], [], [], []
            self.answer_box.clear()
            self.data2.clear()
            self.related_search.clear()
            self.questions.clear()
            self.snippet.clear()
            self.displayed_text1.clear()
            self.link1.clear()
            self.titles.clear()
            self.unscraped_questions.clear()
        except Exception as exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exception,exc_type,exc_obj,exc_tb.tb_lineno)


    def scrapping(self):
        """Scrapping method"""
        # function table that adds <table> where needed
        def table(elem):
            return '<table>' + str(elem) + '</table>'
        # function paragraph that adds <p> where needed
        def paragraph(elem):
            return '<p>' + str(elem) + '</p>'
        # function list tags that adds <ol>/<ul> where needed
        def list_tags(elem, tag):
            if tag == 'ol':
                return '<ol>' + str(elem) + '</ol>'
            elif tag == 'ul':
                return '<ul>' + str(elem) + '</ul>'
        try:
            # we try to locate answerbox element (loc_elem)
            # if it is located we proceed
            loc_elem = self.soup.find('h2',
                                      attrs={'class': 'Uo8X3b OhScic zsYMMe'})
            if loc_elem:
                # if it has text featured snippet from the web
                # we set the variable yt_video_cond
                # locating class
                if loc_elem.text == 'Featured snippet from the web':
                    yt_video_cond = self.soup.find('div',
                                                   {'class':'ifM9O'}).find(
                        'div',{'class':'V3FYCf'}).contents[0]['class']
                    yt_video_cond = ','.join(yt_video_cond).replace(',',' ')
                    # locating our link in top search
                    link = self.soup.find_all('div', attrs={'class': 'yuRUbf'})
                    title = self.soup.find('div',
                                           attrs={'class': 'g'}).find(
                        'div', attrs={'class', 'yuRUbf'}).find('h3').text
                    # if condition variable is met
                    # we get youtube string and start time
                    # we put it to the snippet variable
                    if yt_video_cond=='wDYxhc NFQFxe viOShc':
                        base = self.soup.find('div', {'class': 'ifM9O'}).find(
                            'div', {'class': 'V3FYCf'}).find(
                            'div',{'class':'wDYxhc NFQFxe viOShc'})
                        yt_string = base.find('span',{'class':'XdBtEc'}).text
                        yt_string = paragraph(yt_string)
                        snippet = str(yt_string)
                        # locating our display link in top search
                        displayed_link = self.soup.find('cite',
                                                        attrs={'class': 'iUh30 tjvcx'})
                        # youtube videos do not contain date
                        # date = None
                        date = None
                    # else if youtube condition variable isn't met
                    # we get normal anserbox contents
                    else:
                        # locating our topsearch answer
                        snippet = self.soup.find_all(
                            'span', attrs={'class': 'hgKElc'})
                        snippet = ''.join([str(i) for i in snippet[0].contents])
                        snippet = paragraph(snippet)
                        # locating our display link in top search
                        displayed_link = self.soup.find(
                            'cite', attrs={'class': 'iUh30 qLRx3b tjvcx'})
                        # locating our date at top search
                        date = self.soup.find_all(
                            'span', attrs={'class': 'kX21rb ZYHQ7e'})
                    # if content in answerbox exists
                    # we will add it to its suitable list
                    # else we will add None string value
                    if link:
                        # appending link to list answerbox
                        self.answer_box.append(link[0].contents[0]['href'])
                    else:
                        self.answer_box.append('None')
                    if displayed_link:
                        # appending displayed link
                        self.answer_box.append(displayed_link.text)
                    else:
                        self.answer_box.append('None')
                    if date:
                        # appending date
                        self.answer_box.append(date[0].text)
                    else:
                        self.answer_box.append('None')
                    if snippet:
                        # appending answer
                        self.answer_box.append(snippet)
                    else:
                        self.answer_box.append('None')
                    if title:
                        # appending title
                        self.answer_box.append(title)
                    else:
                        self.answer_box.append('None')
                    # we create data1 dictionary
                    # that will contain all contents from answerbox
                    # putting data from lists into dict
                    self.data1 = {'question':self.questionn,
                                  'link': self.answer_box[0],
                                  'displayed_link': self.answer_box[1],
                                  'date': self.answer_box[2],
                                  'answer': self.answer_box[3],
                                  'title':self.answer_box[4]}
                    # for every dict content
                    # if it equals to None string value
                    # we will delete that value from data1 dict
                    if (self.data1['answer']=='None')or(
                            not self.data1['answer']):
                        del self.data1['answer']
                    if (self.data1['date']=='None')or(
                            not self.data1['date']):
                        del self.data1['date']
                    if (self.data1['displayed_link']=='None')or(
                            not self.data1['displayed_link']):
                        del self.data1['displayed_link']
                    if (self.data1['link']=='None')or(
                            not self.data1['link']):
                        del self.data1['link']
                    if (self.data1['question']=='None')or(
                            not self.data1['question']):
                        del self.data1['question']
                    if (self.data1['title']=='None')or(
                            not self.data1['title']):
                        del self.data1['title']
                else:
                    # if there is no topsearch it will return none in dict
                    self.data1 = {'None':'None'}
            else:
                # if there is no topsearch it will return none in dict
                self.data1 = {'None': 'None'}

            # we enumerate all paa and its values
            # in for loop
            for number,i in enumerate(self.soup.find_all(
                    'div', attrs={'jsname': 'F79BRe'})):
                # if number of current paa question
                # is lesser than our set number
                # of questions to scrape
                # we will proceed and try
                if number < self.num_questions_to_scraper:
                    try:
                        # finding list element with ul tag
                        list_ul = i.find('ul',attrs={'class':'i8Z77e'})
                        # finding list element with ol tag
                        list_ol = i.find('ol',attrs={'class':'X5LH0c'})

                        var_t = i.find('div',{'jsname':'rozPHf'}).find(
                            'div',
                            attrs={
                                'class':'webanswers-webanswers_table__webanswers-table'})
                        # finding table element
                        tab = i.find('table')
                        # finding question element
                        var_q = i.find('div', attrs={'jsname': 'jIA8B'}).text
                        # finding
                        var_l = i.find_all('span', attrs={'class': 'hgKElc'})
                        # finding answer element
                        var_ll = i.find_all('div',attrs={'class':'hgKElc PZY7Gb'})
                        var_c = i.find_all('div',attrs={'class':'NPb5dd'})
                        # finding title element
                        var_d = i.find('div', attrs={'class': 'g'})
                        if var_d:
                            var_d = var_d.find_all('div', attrs={'class', 'yuRUbf'})
                        # finding displayed text element
                        var_mm = i.find('cite', attrs={'class': 'iUh30 tjvcx'})
                        # finding displayed text element
                        var_m = i.find('cite', attrs={'class': 'iUh30 qLRx3b tjvcx'})
                        var_tt = i.find('div', {'class': 'IZ6rdc'})
                        # youtube video text
                        var_gg = i.find('div', {'class': 'iMCzjd'})

                        # if element is located get snippet ,else we conclude its list or table
                        if var_c:
                            self.displayed_text1.append('None')
                            self.titles.append('None')
                            self.link1.append('None')
                            snipp = "".join([str(i) for i in var_c[0].text])
                            snipp = paragraph(snipp)
                            self.snippet.append(snipp)
                            # at the end we append question of paa
                            self.questions.append(var_q)
                        elif var_l:
                            if var_m:
                                self.displayed_text1.append(var_m.text)
                            else:
                                self.displayed_text1.append('None')
                            if var_d[0].find('h3'):
                                self.titles.append(var_d[0].find('h3').text)
                            else:
                                self.titles.append('None')
                            if var_d[0].contents[0]['href']:
                                self.link1.append(var_d[0].contents[0]['href'])
                            else:
                                self.link1.append('None')

                            snipp = "".join([str(i) for i in var_l[0].contents])
                            snipp = paragraph(snipp)
                            self.snippet.append(snipp)
                            # at the end we append question of paa
                            self.questions.append(var_q)
                        elif var_ll:
                            if var_m:
                                self.displayed_text1.append(var_m.text)
                            else:
                                self.displayed_text1.append('None')
                            if var_d[0].find('h3'):
                                self.titles.append(var_d[0].find('h3').text)
                            else:
                                self.titles.append('None')
                            if var_d[0].contents[0]['href']:
                                self.link1.append(var_d[0].contents[0]['href'])
                            else:
                                self.link1.append('None')
                            snipp = "".join([str(i) for i in var_ll[0].contents[0]])
                            snipp = paragraph(snipp)
                            self.snippet.append(snipp)
                            # at the end we append question of paa
                            self.questions.append(var_q)
                        elif var_gg:
                            # in this case we have youtube video in paa
                            # we shall add the rest of contents if they exist
                            if var_m:
                                self.displayed_text1.append(var_m.text)
                            elif var_mm:
                                self.displayed_text1.append(var_mm.text)
                            else:
                                self.displayed_text1.append('None')
                            if var_d[0].find('h3'):
                                self.titles.append(var_d[0].find('h3').text)
                            else:
                                self.titles.append('None')
                            if var_d[0].contents[0]['href']:
                                self.link1.append(var_d[0].contents[0]['href'])
                            else:
                                self.link1.append('None')
                            var_gg = i.find('span',attrs={'class':'XdBtEc'}).text
                            var_gg = paragraph(var_gg)
                            snipp = ''.join(str(var_gg))
                            self.snippet.append(snipp)
                            # at the end we append question of paa
                            self.questions.append(var_q)
                        elif tab:
                            try:
                                if var_m:
                                    self.displayed_text1.append(var_m.text)
                                else:
                                    self.displayed_text1.append('None')
                                if var_d:
                                    self.titles.append(var_d[0].find('h3').text)
                                else:
                                    self.titles.append('None')
                                if var_d:
                                    self.link1.append(var_d[0].contents[0]['href'])
                                else:
                                    self.link1.append('None')
                                # at the end we append question of paa
                                self.questions.append(var_q)
                                var_t = var_t.find('table')
                                # we remove all attrs from element
                                # and return it
                                def _remove_all_attrs(element):
                                    for tag in element.find_all(True):
                                        tag.attrs = {}
                                    return element
                                _remove_all_attrs(var_t)
                                var_t = var_t.contents
                                var_t = ''.join([str(z) for z in var_t])
                                snippet = i.find('div', attrs={'class': 'iKJnec'})
                                snip = ''.join([str(z) for z in snippet])
                                # we add <table> tag to the string
                                var_t = table(var_t)
                                # we add <p> tag to the string
                                var_t = paragraph(var_t)
                                var_tt = paragraph(var_tt)
                                snip = paragraph(snip)
                                # if Text is not None
                                # we will include it in the final answer
                                if str(var_tt) != '<p>None</p>':
                                    snippet = str(var_tt) + snip + str(var_t)
                                else:
                                    snippet = snip + str(var_t)
                                self.snippet.append(str(snippet))

                            except:
                                pass
                        else:
                            if var_m:
                                self.displayed_text1.append(var_m.text)
                            else:
                                self.displayed_text1.append('None')
                            if var_d:
                                self.titles.append(var_d[0].find('h3').text)
                            else:
                                self.titles.append('None')
                            if var_d:
                                self.link1.append(var_d[0].contents[0]['href'])
                            else:
                                self.link1.append('None')
                            title = []
                            title.clear()
                            tables = []
                            tables.clear()
                            var_g = i.find_all('div', attrs={'class': 'co8aDb'})
                            # if it has title ,get title and table
                            # else get just the table
                            if var_g:
                                title.append(''.join([str(i) for i in var_g[0].contents]))
                                rows = i.find_all('div',
                                                  attrs={'class': 'RqBzHd'})[0].find_all(
                                    'li', attrs={'li', 'TrT0Xe'})
                                for row in rows:
                                    row = str(row)
                                    row = row.replace(' class="TrT0Xe"', '')
                                    tables.append(row)
                                tables = ''.join([str(i) for i in tables])
                                # if we have ul tag list we prepare variable
                                # else if we have ol tag list, we prepare var
                                if list_ul:
                                    tag = 'ul'
                                elif list_ol:
                                    tag = 'ol'
                                else:
                                    print('list problems!!!')
                                # we provide our tag var to function
                                # the function will know what tags to put
                                tables = list_tags(elem=tables,tag=tag)
                                title_0 = paragraph(title[0])
                                final = title_0 + tables
                                final = re.sub('\.\.\.', '', final)
                                self.snippet.append(final)
                                # at the end we append question of paa
                                self.questions.append(var_q)
                            else:
                                # we get just the list rows
                                # because there is no heading
                                rows = i.find_all('li', attrs={'li', 'TrT0Xe'})
                                for row in rows:
                                    row = str(row)
                                    row = row.replace(' class="TrT0Xe"', '')
                                    tables.append(row)
                                tables = ''.join([str(i) for i in tables])
                                if list_ul:
                                    tag = 'ul'
                                elif list_ol:
                                    tag = 'ol'
                                else:
                                    print('list problems!!!')
                                # we provide our tag var to function
                                # the function will know what tags to put
                                tables = list_tags(elem=tables,tag=tag)
                                tables = re.sub('\.\.\.', '', tables)
                                self.snippet.append(tables)
                                # at the end we append question of paa
                                self.questions.append(var_q)
                    except Exception as exception:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        print(exception, exc_type, exc_obj, exc_tb.tb_lineno)
                        print(number)
                        pass
                else:
                    # the rest of unclicked questions
                    var_qq = i.find('div', attrs={'jsname': 'jIA8B'}).text
                    self.unscraped_questions.append(var_qq)
            stat = self.soup.find('div',attrs={'id':'result-stats'})
            # if results count present extract it
            # and put it to a variable results_count
            # this variable will be passed to dictionary - data2
            if stat:
                statistic = stat.contents[0].split()
                results_count = int(statistic[1].replace(',',''))
            else:
                results_count = 'None'
            # we find related searches elements,
            # for each we append content with bold text tag to list
            relser = self.soup.find_all(
                'div', attrs={'class': 's75CSd OhScic AB4Wff'})
            for i in relser:
                self.related_search.append(str(i.text))

            self.snippet = [i.replace('<br/>','<br>') for i in self.snippet]
            # we put all results to data2 dictionary
            for alpha, beta, gama, delta, epsilon in zip(self.questions, self.titles,
                                     self.link1, self.snippet,
                                     self.displayed_text1):
                self.data2.append({'question': alpha, 'title': beta,
                                   'link': gama, 'answer': delta,
                                   'displayed_link': epsilon})
            # for every content in data 2 dictionary
            # if there is None string value
            # we shall delete it from dict
            for i in self.data2:
                if (i['displayed_link']=='None')or(not i['displayed_link']):
                    del i['displayed_link']
                if (i['answer']=='None')or(not i['answer']):
                    del i['answer']
                if (i['link']=='None')or(not i['link']):
                    del i['link']
                if (i['title']=='None')or(not i['title']):
                    del i['title']
                if (i['question'] == 'None')or(not i['question']):
                    del i['question']

            #finnally we add all the data to dict
            # if data1 (dict for answerbox) is not String None
            # then we will add data1 to result dict also
            if list(self.data1.keys())[0] != 'None':
                result = {'answer_box': self.data1, 'related_questions': self.data2,
                          'related_searches': self.related_search,
                          'unclicked_questions': self.unscraped_questions,
                          'results_count': results_count
                          }
            # else if it is, we will not include data1
            # to our resulting dictionary
            else:
                result = {'related_questions': self.data2,
                          'related_searches': self.related_search,
                          'unclicked_questions': self.unscraped_questions,
                          'results_count': results_count
                          }
            # we put our dict to json for the purpose
            # of better displaying of our results
            # json_object = json.dumps(result,indent=4,ensure_ascii=False)
            # print(json_object)
            # we return our result dictionary
            return result
        except Exception as exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exception,exc_type,exc_obj,exc_tb.tb_lineno)

# we define hmtl_start function
# that is going to run our Html scrap class
# scrapping method
# we return resulting dictionary at the end
def html_start(query,num_questions_to_scraper,page_content,):
    """Running function of our code"""
    result = Scrapper(query=query,
                       num_questions_to_scraper=num_questions_to_scraper,
                       page_content=page_content).scrapping()
    return result
