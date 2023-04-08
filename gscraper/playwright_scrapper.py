"""Importing necessary modules."""
import time
from threading import Thread
import queue
import sys
import requests
from playwright.sync_api import sync_playwright
from tqdm import tqdm
from .html_scrapper import html_start
# pylint: disable=R1705,R0915,R0914,R0903,W0102,W0702,W0703,R0913,R0912,R0902
# variables that we will pass across code
returning_value = queue.Queue()
page_content = queue.Queue()


class GoogleScrapper:
    """GoogleScrapper main class."""

    def __init__(self, query, num_questions_to_scraper, headless, proxy):
        try:
            # if proxy is set
            # we will prepare our dictionary
            # that will be used as arg
            if proxy is not None:
                self.proxy = proxy.split(':')
                self.proxy_dict_arg = {
                    'server' : self.proxy[0] + ':' + self.proxy[1],
                    'username' : self.proxy[2],
                    'password' : self.proxy[3]
                }
            self.query = query
            # we put our query to returning value variable
            returning_value.put(self.query)
            self.num_questions_to_scraper = int(num_questions_to_scraper)
            # arguments that will be passed to our browser
            args = [
                '--disable-logging',
                '--disable-and-delete-previous-log',
                '--deny-permission-prompts',
                '--no-default-browser-check',
                '--deny-permission-prompts',
                '--disable-popup-blocking',
                '--ignore-certificate-errors',
                '--no-service-autorun',
                '--password-store=basic',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                '--disable-audio-output'
            ]
            # if headless is set to true in google_scrapper
            # browser will be hidden
            # if proxy is set we will include it
            with sync_playwright() as self.playwr:
                if proxy is not None:
                    if headless is True:
                        self.browser = self.playwr.chromium.launch(
                            proxy={'server':'http://per-context'},args=args)
                    else:
                        self.browser = self.playwr.chromium.launch(
                            headless=False,
                            proxy={'server':'http://per-context'},args=args)
                    self.context = self.browser.new_context(proxy=self.proxy_dict_arg)
                # else we wont include proxy in our browser
                else:
                    if headless is True:
                        self.browser = self.playwr.chromium.launch(args=args)
                    else:
                        self.browser = self.playwr.chromium.launch(
                            args=args,
                            headless=False)
                    self.context = self.browser.new_context()
                self.page = self.context.new_page()
                # we are replacing empty spaces in query
                # with %20 for to be used in url string
                page_url = f'https://www.google.com/search?hl=en&q=' \
                           f'{self.query.replace(" ", "%20").replace("  ", "%20")}'
                # opening the url
                self.page.goto(page_url)

                # we are trying to wait for recapthca
                # to be shown for 1 second, else we pass
                if self.page.is_visible \
                            ("div.g-recaptcha", timeout=1000):
                    self._solve_captcha(page_url)
                else:
                    pass

                def popup():
                    try:
                        # if pop up is visible click on button
                        if self.page.is_visible('button#L2AGLb',
                                                timeout=250) is True:
                            self.page.wait_for_selector \
                                ("button#L2AGLb", state='visible', timeout=500).click()

                    except Exception as exception:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        print(exception, exc_type, exc_obj, exc_tb.tb_lineno)
                popup()
                # we define our clicking function
                # for i - number of current click
                # we return no string if we don't want to break the for loop
                # in case that there are no more question we return yes
                # to break from for loop
                def elem_clicker(i):  # clicking function
                    try:
                        self.page.wait_for_selector(f'//*[@jsname="Cpkphb"][{i}]', state='visible',
                                                    timeout=50).click()  # clicking
                        return 'no'
                    except:
                        if self.page.is_visible('//*[@id="rso"]') is True:
                            return 'yes'
                        else:
                            elem_clicker(i)
                            return 'no'

                # if element - paa questions is visible,
                # start clicking for set range of clicks
                # (num_questions_to_scraper input)
                # if breaking variable == yes, break from loop
                if self.page.is_visible(
                        '//*[@jsname="Cpkphb"]') is True:
                    for i in tqdm(range(1, int(
                            self.num_questions_to_scraper) + 1), desc='Scrapping...'):
                        breaking = elem_clicker(i)
                        if breaking == 'no':
                            try:
                                self.page.wait_for_selector(
                                    '//*[@jsname="grQLgb"]', state='visible', timeout=2000)
                                self.page.wait_for_selector(
                                    '//*[@jsname="grQLgb"]', state='hidden', timeout=2000)
                            except:
                                pass
                        elif breaking == 'yes':
                            print('No more questions to scrape  ')
                            break
                    time.sleep(0.5)
                    # get html page content and put it to variable
                    page_c = self.page.content()
                    page_content.put(page_c)
                    # closing broswer
                    self.context.close()
                    self.browser.close()
                else:
                    # no questions to click on
                    print('no paa')
                    # get html page content and put it to variable
                    page_c = self.page.content()
                    page_content.put(page_c)
                    # close browser
                    self.context.close()
                    self.browser.close()


        except Exception as exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exception, exc_type, exc_obj, exc_tb.tb_lineno)

    def _solve_captcha(self, page_url):
        """'Our captcha solving function"""
        print('=== CAPTCHA SOLVING ===')
        # locating site key elem
        site_key_element = self.page.locator("div.g-recaptcha")
        site_key = None
        # if located, we get attributes
        if site_key_element:
            site_key = site_key_element.get_attribute('data-sitekey')
            datas = site_key_element.get_attribute('data-s')

        method = "userrecaptcha"
        key = "4a883993f594c4012ea1bb775f7a8c79"
        url = f"http://2captcha.com/in.php?key=" \
              f"{key}&method={method}&googlekey={site_key}&pageurl={page_url}&data-s={datas}"

        response = requests.request("GET", url)
        # if response is not valid, exit the code
        if response.text[0:2] != 'OK':
            print('Service error. Error code:' + response.text)
            sys.exit()
        captcha_id = response.text[3:]
        token_url = f"http://2captcha.com/res.php?key={key}&action=get&id={captcha_id}"
        # we set while loop to repeat requests
        # until it gets valid response - OK
        # then it breaks the loop
        while True:
            time.sleep(5)
            response = requests.get(token_url)
            print('while/response.text:  ', response.text)
            if response.text[0:2] == 'OK':
                break
        captha_results = response.text[3:]

        try:
            # javascript that will make element visible by deleting display:
            # none parameter from style attribute
            self.page.eval_on_selector(
                "[name='g-recaptcha-response']", "el => el.removeAttribute('style')")
            self.page.fill("[name='g-recaptcha-response']", captha_results)
            self.page.evaluate('document.getElementById("captcha-form").submit();')
            print('=== CAPTCHA SOLVED ===')
            # for speed boost we can try to set here time.sleep(0.5)
            time.sleep(2)
        except Exception as exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exception, exc_type, exc_obj, exc_tb.tb_lineno)


class HtmlThread(Thread):
    """Our thread class that will return the variable."""

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    # defining join method of our thread to return variable
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


def scrapper_g(query, num_questions_to_scraper=0, headless_mode=True, proxy=None):
    """Our scrapper_g function that will run the whole program."""
    GoogleScrapper(query=query, num_questions_to_scraper=num_questions_to_scraper,
                   headless=headless_mode, proxy=proxy)
    # we run html scrapper as a thread and return results into variable "result"
    result = HtmlThread(target=html_start, args=(returning_value.get(),
                                                num_questions_to_scraper, page_content.get(),))
    # we start our thread
    result.start()
    # we wait for thread to finish
    # we also return results to our google_scrapper
    return result.join()
