from selenium import webdriver

BASE_URL = "https://www.mudah.my"

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)

class MainPage(BasePage):
    def _search_deals(self):
        self.driver.find_element_by_xpath('//div[starts-with(@class, "header-menu")]/a[contains(text(), "SEARCH DEALS")]').click()

class SearchPage(BasePage):
    def _search(self, item):
        self.driver.find_element_by_xpath('//*[@id="searchtext"]').send_keys(item)
        self.driver.find_element_by_id('searchbutton').click()

    def _get_product_details(self, search_result_filter=None):
        output = []
        for element in self.driver.find_elements_by_class_name('listing_ads_params'):
            try:
                name_element = element.find_element_by_class_name('list_title')
                item_name = str(name_element.text)
                item_url = str(name_element.find_element_by_xpath('.//a').get_attribute('href'))
                item_price = int(element.find_element_by_class_name('ads_price').text.replace("RM", "").replace(" ", ""))
                # item_seller =
                if search_result_filter != None:
                    if any(i in item_name for i in search_result_filter):
                        output.append(["Mudah", item_name, item_price, item_url])
                else:
                    output.append(["Mudah", item_name, item_price, item_url])

            except:
                pass
        return output

