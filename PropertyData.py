from Property import Property
import html5lib
import lxml
from bs4 import BeautifulSoup, SoupStrainer
import requests, timeit, re, time
import usaddress
#from pathos.multiprocessing import ProcessingPool as Pool
from multiprocessing import Pool

from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker

eng = create_engine('sqlite:///property_data.db')
Base = declarative_base()


class PropertyData():
    # def __init__(self):
    #     Session = sessionmaker(bind=eng)
    #     self.session = Session()

    def getPropertyList(self, zip, refresh=False):
        propertyList = []

        zpidList = self.getPropertyIDs(zip)
        if (len(zpidList) > 0):
            zpidsToUpdate = []
            try:
                stored_props = session.query(StoredProperty).filter_by(zip=zip).all()
            except:  # assuming no entries yet
                stored_props = []

            for zpid in zpidList:
                found = False
                for i, sprop in enumerate(stored_props):
                    if int(zpid) == sprop.zp_id:
                        found = True
                        if sprop.valid:
                            propertyList.append(self.getPropertyFromStoredProperty(sprop))
                        stored_props.pop(i)  # if found, remove from list so that
                        break;
                if not found:
                    zpidsToUpdate.append(zpid)

            # clean up properties in db that are no longer for sale
            for sprop in stored_props:
                session.delete(sprop)
                session.commit()

            #zpidsToUpdate = zpidsToUpdate[0:10]
            numProcesses = 1
            numFailed, numRecovered = 0, 0
            #pool = Pool(numProcesses)
            start = timeit.default_timer()
            #results = pool.map(self.getPropertyFromZpid, zpidsToUpdate)
            results = []
            for zpid in zpidsToUpdate:
                results.append(self.getPropertyFromZpid(zpid))
            print("Getting property details with {0} processes took {1:.2f} seconds.".format(numProcesses, timeit.default_timer() - start))
            for i, property in enumerate(results):
                #property = self.getPropertyFromZpid(zpid)
                if (property is not None and property.isValid() == True):
                    sprop = self.getStoredPropertyFromProperty(property)
                    try:
                        session.add(sprop)
                        session.commit()
                    except exc.IntegrityError:
                        print("Found duplicate (ID={0}). Skipping.".format(sprop.zp_id))
                        session.rollback()
                    property.calculate()
                    propertyList.append(property)
                else:
                    numFailed += 1
                    if (property.address == None and property.price == None): # if no other field was valid, then try again
                        print("Failed to get property details for zpid: {0}. Retrying.".format(zpidsToUpdate[i]))
                        property = self.getPropertyFromZpid(zpidsToUpdate[i])
                        if (property is not None and property.isValid() == True):
                            numRecovered += 1
                        else:
                            print("Failed retry.")
                    else: # if property is not valid, but some fields are not none, then missing data so don't retry
                        if property.getIsPreForeclosure():
                            print(
                                "Failed to get property details for zpid: {0}: Pre-Foreclosure, not retrying".format(zpidsToUpdate[i]))
                        else:
                            print("Failed to get property details for zpid: {0}: Page is missing data, not retrying.".format(zpidsToUpdate[i]))

                    # regardless of if recovered, add prop to db so invalid properties won't be checked again
                    sprop = self.getStoredPropertyFromProperty(property)
                    try:
                        session.add(sprop)
                        session.commit()
                    except exc.IntegrityError:
                        print("Found duplicate (ID={0}). Skipping.".format(sprop.zp_id))
                        session.rollback()

                    # if property is now valid (recovered), calculate and add to list
                    if (property is not None and property.isValid()):
                        property.calculate()
                        propertyList.append(property)

            print("Failed to get details for {0} IDs. {1} recovered successfully.".format(numFailed, numRecovered))
            return propertyList

    def getStoredPropertyFromProperty(self, property):
        sprop = StoredProperty()
        sprop.zp_id = property.zp_id
        sprop.address = property.address
        sprop.city = property.city
        sprop.state = property.state
        sprop.zip = property.zip
        sprop.price = property.price
        sprop.rent = property.rent

        sprop.year = property.year
        sprop.size = property.size
        sprop.beds = property.beds
        sprop.baths = property.baths
        sprop.mls_number = property.mls_number

        sprop.valid = property.valid
        sprop.isPreForeclosure = property.isPreForeclosure

        return sprop

    def getPropertyFromStoredProperty(self, sprop):
        property = Property()
        property.zp_id = sprop.zp_id
        property.address = sprop.address
        property.city = sprop.city
        property.state = sprop.state
        property.zip = sprop.zip
        property.price = sprop.price
        property.rent = sprop.rent

        property.year = sprop.year
        property.size = sprop.size
        property.beds = sprop.beds
        property.baths = sprop.baths
        property.mls_number = sprop.mls_number

        property.valid = sprop.valid
        property.isPreForeclosure = sprop.isPreForeclosure

        return property


    def getPropertyIDs(self, zip):
        # try search-pagination-wrapper and zsg-pagination
        #zpidList = []
        url = "http://www.zillow.com/homes/for_sale/" + zip
        pageNum = 1
        #finished = False
        #while not finished:
        zpidsOnPage = []
        #pageUrl = url +"/" + pageNum.__str__() + "_p/"
        pageUrls = []
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html5lib")

        pageList = soup.find('ol',attrs={"class":"zsg-pagination"})
        if (pageList is not None):
            children = pageList.find_all('li')
            i = 1
            while i < len(children):
                pageUrls.append(url +"/" + str(i) + "_p/")
                i += 1

        numProcesses = 1
        pool = Pool(numProcesses)
        start = timeit.default_timer()
        results = pool.map(self.getPropertyIDsFromWebPage, pageUrls)
        print("Getting property IDs with {0} processes took {1:.2f} seconds.".format(numProcesses, timeit.default_timer() - start))
        #results = []
        #for pageUrl in pageUrls:
            #results.append(self.getPropertyIDsFromWebPage(pageUrl))
            #sleep(5)
        for i, idList in enumerate(results):
            if len(idList) == 0:
                print("Failed to get IDs from page. Retrying.")
                time.sleep(1)
                result = self.getPropertyIDsFromWebPage(pageUrls[i])
                if len(result) == 0:
                    print("Failed retry.")
                else:
                    results.append(result)
        if results is not None:
            flat_list = [item for sublist in results for item in sublist]
            zpidList = list(set(flat_list))

            #pageNum += 1
            #temporary, limit results for testing
            #if pageNum > 1:
            #    break

        for id in zpidList:
            print(id)
            #self.zpidList = zpidList

        return zpidList

    def getPropertyIDsFromWebPage(self, url):
        zpidList = []
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html5lib")

        # zpidTags = soup.find_all(attrs={"data-zpid":True})
        zpidTags = soup.find_all(attrs={"data-zpid": True})

        #lock = Lock()
        #lock.acquire(True)
        for tag in zpidTags:
            zpid = tag['data-zpid']
            if (not zpidList.__contains__(zpid)):
                zpidList.append(zpid)
        #lock.release()
        return zpidList

    def validatePostalCode(self, zip):
        if len(zip) == 5 and zip.isdigit():
            return True
        return False



    def getPropertyFromZpid(self, zpid):
        url = "http://www.zillow.com/homes/" + zpid + "_zpid/"
        response = requests.get(url)
        html = response.content
        #html = '<html><body><div class="something-else"><div class=" status-icon-row for-sale-row home-summary-row"></div><div class=" home-summary-row"><span class=""> $1,342,144 </span></div></div></body></html>'
        #bad_soup = BeautifulSoup(html, "html5lib")
        #soup = BeautifulSoup(bad_soup.prettify(), "html5lib")
        soup = BeautifulSoup(html, "lxml")

        property = Property()
        property.setID(zpid)
        price = self.getPriceFromWebPage(soup)
        property.setPrice(price)
        rent = self.getRentFromWebPage(soup)
        property.setRent(rent)
        print(property.getRent())
        address, city, state, zip = self.getAddressFromWebPage(soup)
        property.setAddress(address)
        property.setCity(city)
        property.setState(state)
        property.setZip(zip)
        year, size, beds, baths = self.getOtherDetailsFromWebPage(soup)
        property.setYear(year)
        property.setSize(size)
        property.setBeds(beds)
        property.setBaths(baths)
        MLSNum = self.getMLSNumberFromWebPage(soup)
        property.setMLSNumber(MLSNum)
        isPreForeclosure = self.getIsPreForeclosureFromWebpage(soup)
        property.setIsPreForeclosure(isPreForeclosure)

        return property

    def getPriceFromWebPage(self, soup):
        price = None
        if (soup is not None):
            results = soup.find_all('div', attrs={"class":"main-row home-summary-row"})
            if len(results) > 0:
                text = results[0].text
                try:
                    price = int(re.sub('[^0-9]', '', text))
                except:
                    price = None
        return price

    def getAddressFromWebPage(self, soup):
        address = None
        city = None
        state = None
        zip = None
        if (soup is not None):
            results = soup.find_all(attrs={"class":"addr"})
            if (len(results) > 0):
                children = results[0].find_all('h1')
                if (len(children) > 0):
                    address = children[0].text
                    parsed, type = usaddress.tag(address)
                    address = ""
                    for key in parsed:
                        if key == 'PlaceName':
                            city = parsed['PlaceName']
                        elif key == 'StateName':
                            state = parsed['StateName']
                        elif key == 'ZipCode':
                            zip = parsed['ZipCode']
                        else:
                            address += parsed[key] + " "
        return address, city, state, zip

    def getRentFromWebPage(self, soup):
        rent = None
        if (soup is not None):
            #results = soup.find_all(attrs={"class":"tertiary-item"})
            # 'div',
            #<input id="HDPZestimateProxiedAssetsConfig"
            #footer
            results = soup.find_all('input', attrs={"id":"HDPZestimateProxiedAssetsConfig"})
            #print (results[0].prettify())
            if (len(results) > 0):
                reg = re.search(r"\"restimate\\\\\\\":[0-9]*,", str(results[0]))
                if (reg is not None):
                    try:
                        rent = int(re.sub('[^0-9]', '', reg.group()))
                    except:
                        rent = None
        return rent

    def getRentFromWebPage(self, soup):
        rent = None
        if (soup is not None):
            #results = soup.find_all(attrs={"class":"tertiary-item"})
            # 'div',
            #<input id="HDPZestimateProxiedAssetsConfig"
            #footer
            results = soup.find_all('input', attrs={"id":"HDPZestimateProxiedAssetsConfig"})
            if (len(results) > 0):
                reg = re.search(r"\"restimate\\\\\\\":[0-9]*,", str(results[0]))
                if (reg is not None):
                    try:
                        rent = int(re.sub('[^0-9]', '', reg.group()))
                    except:
                        rent = None
        return rent

    def getOtherDetailsFromWebPage(self, soup): # (year, size, beds, baths)
        year, size, beds, baths = None, None, None, None
        if (soup is not None):
            results = soup.find_all('input', attrs={"id":"HDPZestimateProxiedAssetsConfig"})
            if (len(results) > 0):
                reg = re.search(r"\"yearBuilt\\\\\\\":[0-9]*,", str(results[0]))
                if (reg is not None):
                    try:
                        year = int(re.sub('[^0-9]', '', reg.group()))
                    except:
                        year = None
                reg = re.search(r"\"livingArea\\\\\\\":[0-9]*,", str(results[0]))
                if (reg is not None):
                    try:
                        size = int(re.sub('[^0-9]', '', reg.group()))
                    except:
                        size = None
                reg = re.search(r"\"bedrooms\\\\\\\":[0-9.]*,", str(results[0]))
                if (reg is not None):
                    try:
                        beds = float(re.sub('[^0-9^.]', '', reg.group()))
                    except:
                        beds = None
                reg = re.search(r"\"bathrooms\\\\\\\":[0-9.]*,", str(results[0]))
                if (reg is not None):
                    try:
                        baths = float(re.sub('[^0-9^.]', '', reg.group()))
                    except:
                        baths = None

        return year, size, beds, baths

    def getMLSNumberFromWebPage(self, soup):
        MLSNum = None
        if (soup is not None):
            result = soup.find(text=re.compile(r'MLS.*[0-9]*'))
            if (result is not None):
                reg = re.search(r'MLS.*#[0-9]*', str(result))
                if (reg is not None):
                    try:
                        MLSNum = int(re.sub('[^0-9]', '', reg.group()))
                    except:
                        MLSNum = None
        return MLSNum

    def getIsPreForeclosureFromWebpage(self, soup):
        isPreForeclosure = None
        if (soup is not None):
            result = soup.find(text=re.compile(r'Pre-Foreclosure'))
            if (result is not None):
                isPreForeclosure = True
            else:
                isPreForeclosure = False
        return isPreForeclosure

class StoredProperty(Base):
    __tablename__ = "Properties"

    zp_id = Column(Integer, primary_key=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(Integer)
    price = Column(Integer)
    rent = Column(Integer)

    year = Column(Integer)
    size = Column(Integer)
    beds = Column(Integer)
    baths = Column(Integer)
    mls_number = Column(Integer)

    valid = Column(Boolean)
    isPreForeclosure = Column(Boolean)

Base.metadata.bind = eng
Base.metadata.create_all()
Session = sessionmaker(bind=eng)
session = Session()