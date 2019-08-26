from selenium import webdriver

BASE_URL = "https://my.carousell.com"

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)

class SearchPage(BasePage):
    def _search(self, item):
        self.driver.find_element_by_xpath('//input[starts-with(@class, "styles__input___")]').send_keys(item)
        self.driver.find_element_by_xpath('//form[starts-with(@class, "styles__searchInput___")]/button[starts-with(@class, "styles__button___")] ').click()

    def _get_product_details(self, search_result_filter=None):
        output = []
        td = self.driver.find_element_by_xpath('//div[starts-with(@class, "styles__listingsWrapper___")]')
        for element in td.find_elements_by_xpath('//div[starts-with(@class, "styles__cardContent")]'):
            try:
                item_url = str(element.find_element_by_xpath('.//a[starts-with(@class, "styles__link")]').get_attribute('href'))
                item_name = str(element.find_element_by_xpath('.//a[2]/p').text)
                item_price = int(element.find_element_by_xpath('.//a[2]/p[2]').text.replace("RM", "").replace(",", ""))
                if search_result_filter != None:
                    if any(i in item_name for i in search_result_filter):
                        output.append(["Carousell", item_name, item_price, item_url])
                else:
                    output.append(["Carousell", item_name, item_price, item_url])
            except:
                pass
        return output
