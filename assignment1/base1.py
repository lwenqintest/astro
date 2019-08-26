from selenium import webdriver
import os
import unittest
import xmlrunner
import lib.mudahPage as mudahPage
import lib.carousellPage as carousellPage

validItemName = ['Iphone8', 'IPhone 8', 'iPhone 8', 'iphone 8', 'Iphone 8', 'IPHONE8', 'IPHONE 8']
CHROMEDRIVER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'bin/chromedriver'))

def _custom_sort(myList):
    return myList[2]

def _get_item_name_from_table(myList):
    nameList = []
    for item in myList:
        nameList.append(item[1])
    return nameList

class WebAutomationActions(unittest.TestCase):
    def setUp(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("headless")
        self.driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=self.chrome_options)

    def tearDown(self):
        self.driver.quit()

    def _searchOnMudah(self, searchString):
        self.driver.get(mudahPage.BASE_URL)
        self.page = mudahPage.MainPage(self.driver)
        self.page._search_deals()
        self.page = mudahPage.SearchPage(self.driver)
        self.page._search(searchString)

    def _searchOnCarousell(self, searchString):
        self.driver.get(carousellPage.BASE_URL)
        self.page = carousellPage.SearchPage(self.driver)
        self.page._search(searchString)

    def _searchItemOn(self, site, item):
        if site.lower() == "mudah":
            self._searchOnMudah(item)
        elif site.lower() == "carousell":
            self._searchOnCarousell(item)
        else:
            raise Exception("Search method is not handled for this site")

class WebAutomation(WebAutomationActions):
    def __init__(self, methodName="runTest", paramSearchSite=None, paramSearchString=None):
        super(WebAutomation, self).__init__(methodName)
        self.paramSearchSite = paramSearchSite
        self.paramSearchString = paramSearchString

    @staticmethod
    def parametrize(test_class, method, paramSearchSite=None, paramSearchString=None):
        suite = unittest.TestSuite()
        suite.addTest(test_class(method, paramSearchSite=paramSearchSite, paramSearchString=paramSearchString))
        return suite

    def test_validate_product_search(self):
        print("\n" + self._testMethodName)
        self._searchItemOn(self.paramSearchSite, self.paramSearchString)
        tableData = self.page._get_product_details(validItemName) # validItemName to filter out irrelevant search results
        nameList = _get_item_name_from_table(tableData)
        self.assertNotEqual(len(nameList), 0) # As long as list is not zero, it is validated that the product searched for is displayed

    def test_print_table_output(self):
        print("\n" + self._testMethodName)
        print "Web automation is running in headless browser mode....."
        # Navigate to mudah.my and get product details
        # Output in the form of [ <website>, <item_name>, <price>, <item_url> ]
        self._searchItemOn("mudah", "Iphone8")
        tableData1 = self.page._get_product_details(validItemName)

        # Navigate to carousell and get product details
        self._searchItemOn("carousell", "Iphone8")
        tableData2 = self.page._get_product_details(validItemName)

        # Merge result tables from both pages and sort it based on price (ascending order)
        tableData = tableData1 + tableData2
        tableData.sort(key=_custom_sort)
        for data in tableData:
            print data

suite = unittest.TestSuite()
testInput = [["mudah", "Iphone8"],
             ["carousell", "Iphone8"]
             ]
for input in testInput:
    methodname = "test_validate_product_search_on_{}".format(input[0])
    setattr(WebAutomation, methodname, WebAutomation.test_validate_product_search)
    suite.addTest(WebAutomation.parametrize(WebAutomation, methodname, paramSearchSite=input[0], paramSearchString=input[1]))

setattr(WebAutomation, "test_print_table_output", WebAutomation.test_print_table_output)
suite.addTest(WebAutomation.parametrize(WebAutomation, "test_print_table_output"))

if __name__ == "__main__":
    runner = xmlrunner.XMLTestRunner(output="output").run(suite)