from urllib.request import Request
from urllib.request import HTTPCookieProcessor
from urllib.request import build_opener
from Config import imageConfig, pageConfig, config, reConfig
from http.cookiejar import MozillaCookieJar
import re
import os


class SexySpider:

    def __init__(self):
        self.cookie = MozillaCookieJar()
        self.handler = HTTPCookieProcessor(self.cookie)
        self.opener = build_opener(self.handler)
        self.rootDir = os.getcwd()
        self.makeRootDir()

    def fuck(self):
        for category in pageConfig["categories"]:
            sexySpider.getCategory(category)

    def makeRootDir(self):
        if os.path.exists(config["scratchFileName"]):
            print("Root file exists: " + config["scratchFileName"])
        else:
            print("creating root data file: " + config["scratchFileName"])
            os.mkdir(config["scratchFileName"])
        os.chdir(config["scratchFileName"])
        self.rootDir = os.getcwd()
        for key in pageConfig["categories"]:
            print("creating category data files: " + config["scratchFileName"] + "/" + key)
            if os.path.exists(key):
                print("Category data files exists: " + config["scratchFileName"] + "/" + key)
            else:
                print("creating category data files: " + config["scratchFileName"] + "/" + key)
                os.mkdir(key)

    def getCategory(self, category):
        os.chdir(category)
        rawPage = self.loadPage(pageConfig["url"] + pageConfig["categories"][category])
        self.makeCategoryPageFile(category, rawPage)
        self.scratchCategory(category)
        os.chdir("../")

    def makeCategoryPageFile(self, category, page):
        with open(category + '_page.txt', 'w') as pageFile:
            pageFile.writelines(pageConfig["url"] + pageConfig["categories"][category] + "\n")
            listStr, number = self.getlistPageStart_n_Num(page)
            if listStr and number:
                for page in range(2, number):
                    pageFile.writelines(pageConfig["url"] + listStr + str(page) + ".html\n")

    def getlistPageStart_n_Num(self, page):
        pageList = self.reMatch(page, reConfig['pages'])
        number = self.reMatch(pageList[-1], reConfig['lastPage'])
        if len(number):
            number = number[0]
        else:
            return None, None
        if len(pageList) > 0 and len(number) > 0:
            return pageList[-1][:pageList[-1].find(number)], int(number) + 1
        else:
            return None, None

    def grabCardPageFromListPages(self, listPageUrl):
        return self.reMatch(self.loadPage(listPageUrl), reConfig["pageMatch"])

    def scratchCategory(self, category):
        with open(category + '_page.txt', 'r') as pageFile:
            for line in pageFile.readlines():
                for listPage in self.grabCardPageFromListPages(line.strip()):
                    self.makeCard(listPage)

    def makeCard(self, cardUrl):
        rawPage = self.loadPage(cardUrl)
        carTitle = self.getCardTitle(rawPage)
        if os.path.exists(carTitle):
            print("card exists: " + carTitle)
            os.chdir("../")
            return
        else:
            print("creating card: " + carTitle)
            os.mkdir(carTitle)
        os.chdir(carTitle)
        with open(carTitle + '_page.txt', 'w') as pageFile:
            imageCount = 0
            pageFile.write(cardUrl + "\n")
            with open(str(imageCount) + '.jpg', 'wb') as pic:
                image = self.getImageFromImageHolder(cardUrl)
                if image is not None:
                    pic.write(image)
                    imageCount += 1
            for count in range(2,int(self.getCardAmount(rawPage))):
                cardUrlName = cardUrl[:-5] + '_' + str(count) + ".html"
                pageFile.write(cardUrlName + "\n")
                with open(str(imageCount) + '.jpg', 'wb') as pic:
                    print(cardUrlName)
                    try:
                        pic.write(self.getImageFromImageHolder(cardUrlName))
                    except Exception as e:
                        msg = "Get image error. URL => " + cardUrlName + "\n" + str(e)
                        self.log(msg)
                        continue
                    imageCount += 1
        os.chdir("../")

    def getCardTitle(self, rawPage):
        matchList = self.reMatch(rawPage, reConfig["cardTitle"])
        if len(matchList) > 0:
            return matchList[0][4:-5]
        else:
            return ""

    def getCardAmount(self, rawPage):
        matchList = self.reMatch(rawPage, reConfig["cardHolderAmount"])
        if len(matchList) > 0:
            return matchList[0][1:-1]
        else:
            return 0

    #######################################################################################
    """ ##This session is for retrieving image from the page which is holding the image """
    def getImageFromImageHolder(self, url):
        return self.getImageFromRawPage(self.loadPage(url))


    def getImageFromRawPage(self, rawPage):
        imageUrl = self.scratchImageUrlFromPage(rawPage)
        print(imageUrl)
        if len(imageUrl) > 0:
            requestItem = Request(imageUrl, headers=imageConfig["header"])
            return self.opener.open(requestItem).read()
        else:
            return None

    def scratchImageUrlFromPage(self, rawPage):
        matchList = self.reMatch(rawPage, reConfig["image"])
        if len(matchList) > 0:
            return matchList[0]
        else:
            return ""
    ########################################################################################

    def reMatch(self, content, reCode):
        pattern = re.compile(reCode)
        try:
            return pattern.findall(content)
        except Exception as e:
            msg = "reMatch error. reCode => " + reCode + "\n" + str(e)
            self.log(msg)
            return []

    def loadPage(self, url):
        try:
            requestItem = Request(url, headers=pageConfig["header"])
            categoryPage = self.opener.open(requestItem).read().decode(pageConfig["encode"])
            return categoryPage
        except Exception as e:
            msg = "Load page error. URL => " + url + "\n" + str(e)
            self.log(msg)
            return False

    def getCookie(self):
        requestItem = Request(self.mainUrl, headers=self.headers)
        mainPage = self.opener.open(requestItem).read()
        self.cookie.save(ignore_discard=True, ignore_expires=True)
        return mainPage

    def log(self, msg):
        with open(self.rootDir + '/log.txt', 'a') as logFile:
            logFile.write(msg + "\n\n")


if __name__ == '__main__':
    sexySpider = SexySpider()
    sexySpider.fuck()
    # sexySpider.getImageFromImageHolder(pageConfig["url"] + pageConfig["categories"]["pure"] + "3245_44.html")