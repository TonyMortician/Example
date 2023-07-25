from playwright.sync_api import sync_playwright, expect
import playwright.sync_api
from time import sleep
import requests

class BasicElement:
    page = 0
    def __init__(self, dataIn):
        self.locator = 0
        self.dataIn = dataIn

    def findElement(self):
        if self.dataIn[0]==0:
            self.locator = BasicElement.page.get_by_role(self.dataIn[1], name=self.dataIn[2], exact=True)

        if self.dataIn[0]==1:
            self.locator = BasicElement.page.get_by_test_id(self.dataIn[1])

        if self.dataIn[0]==2:
            self.locator = BasicElement.page.locator(self.dataIn[1])

        if self.dataIn[0]==3:
            self.locator = BasicElement.page.get_by_placeholder(self.dataIn[1])

        if self.dataIn[0]==4:
            self.locator = BasicElement.page.get_by_alt_text(self.dataIn[1])

    def Click(self):
        self.findElement()
        self.locator.click()

    def Input(self, inputData):
        self.findElement()
        self.locator.fill(inputData)



class CaseData:
    def __init__(self):
        self.url = 0
        self.response = 0
        self.payload = {
                            "jsonrpc": "2.0",
                            "id": "healthcheck",
                            "method": "getmininginfo",
                            "params": []
                        }
    def Show(self):
        print("URL: ", self.url)
        print("Response: ", self.response)

class Page:
    def __init__(self):
        self.page = 0
        self.browser = 0
        self.elements = list()
        self.testData = CaseData()


    def Start(self, p):
        self.browser = p.chromium.launch()
        BasicElement.page = self.page = self.browser.new_page()

    def Goto(self, url):
        self.page.goto(url)

    def FillElements(self, elementsData):
        for data in elementsData:
            self.elements.append(BasicElement(data))

    def PassAuth(self, loginData):
        self.elements[0].Click()
        self.elements[1].Click()
        self.elements[2].Input(loginData[0])
        self.elements[3].Input(loginData[1])
        self.elements[4].Click()
        sleep(5)

    def GetUrl(self):
        self.elements[5].Click()
        self.elements[6].Click()
        self.elements[7].Click()
        self.elements[8].Click()
        self.elements[9].Click()
        self.elements[10].findElement()
        self.testData.url = self.elements[10].locator.get_by_role("textbox").input_value()


    def Post(self):
        self.testData.response = (requests.post(self.testData.url, json = self.testData.payload)).json()

    def CleanUp(self):
        self.elements[11].Click()
        self.elements[12].Click()
        sleep(3)



pageData = ([0, "link", "Account"],
            [1, "signInEmailButton"],
            [2, 'xpath=//input[@type="email"]'],
            [2, 'xpath=//input[@type="password"]'],
            [1, 'signInButton'],
            [3, 'Search Protocols'],
            [2, 'xpath=//p[text()="Bitcoin"]'],
            [1, "networkDropdown"],
            [2, 'xpath=//p[text()="Testnet"]'],
            [1, 'createEndpointButton'],
            [1, 'endpoint'],
            [1, 'endpointOptionsButton'],
            [2, 'xpath=//p[text()="Remove from list"]'])

if __name__ == '__main__':
    with sync_playwright() as pp:
        p = Page()
        p.Start(pp)
        p.FillElements(pageData)
        p.Goto("https://getblock.io/")
        p.PassAuth(["for.testing.333666@gmail.com", "##19dA89_"])
        p.GetUrl()
        p.Post()
        p.testData.Show()
        p.CleanUp()

