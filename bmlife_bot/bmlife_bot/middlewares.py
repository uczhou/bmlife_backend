from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')

driver = webdriver.Chrome(chrome_options=options, executable_path='/home/honglei/Projects/bmlife_bot/chromedriver')


class BmlifeDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        meta_data = request.meta
        if meta_data.get('chrome') is None:
            return None

        driver.get(request.url)
        body = driver.page_source
        if meta_data.get('click'):
            try:
                next_page_btn = driver.find_elements_by_xpath("//div[@class='check-more']")
                if len(next_page_btn) < 1:
                    print("No more pages left")
                else:
                    print(next_page_btn)
                    # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[@class='next']")))
                    driver.find_elements_by_xpath("//div[@class='check-more']")[0].click()
                    body += driver.page_source
            except Exception as e:
                print(e)

        else:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='vhtell']"))
            )
            iframes = driver.find_elements_by_tag_name('iframe')
            driver.switch_to.frame(iframes[0])
            ds = driver.find_elements_by_tag_name('iframe')
            driver.switch_to.frame(ds[0])
            body = driver.page_source
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
