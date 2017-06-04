__author__ = 'ianabshire'

import sys, locale
from PyQt5 import QtCore, QtGui, QtWidgets
from PropertyAnalyzer_GUI import Ui_MainWindow
from Property import Property
import html5lib
import lxml
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import usaddress


class PropertyAnalyzerApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        locale.setlocale(locale.LC_ALL, 'en_US')
        self.setupUi(self)

        self.searchButton.clicked.connect(self.searchButton_Clicked)
        self.searchTextBox.returnPressed.connect(self.searchButton_Clicked)
        #self.propertyTable.itemSelectionChanged.connect(self.propertySelectionChanged)
        self.propertyTableView.selectionModel().selectionChanged.connect(self.propertyTableSelectionChanged)
        self.applyButton.clicked.connect(self.applyButton_Clicked)
        self.resetButton.clicked.connect(self.resetButton_Clicked)

        #self.propertyList.addItemToList(1, "123 Elm St.", "Benicia", "CA", 94510, 100000, 2000)
        #prop = Property(99, "123 Elm St.", "Benicia", "CA", 94510, 100000, 2000)
        #self.propertyWidget.setProperty(prop)
        self.zpidList = []
        self.propertyList = []
        self.currentPropertyIndex = -1

        #testing
        #prop = Property(99, "123 Elm St.", "Benicia", "CA", 94510, 100000, 2000)
        #self.propertyList.append(prop)
        #self.updatePropertyTable()
        #self.currentPropertyIndex = 0

    def searchButton_Clicked(self):
        zip = self.searchTextBox.text()
        if zip != "":
            if (self.validatePostalCode(zip)):
                self.getPropertyIDs(zip)
                if (len(self.zpidList) > 0):
                    self.getPropertyList()
                    self.updatePropertyTable()
                    self.currentPropertyIndex = -1
                    self.propertyTableView.selectRow(0)
            else:
                print("Invalid ZIP code.")

    def applyButton_Clicked(self):
        success = False
        if (self.currentPropertyIndex >= 0 and len(self.propertyList) > self.currentPropertyIndex and
                    self.propertyList[self.currentPropertyIndex] is not None):
            if (self.propertyWidget is not None):
                success = self.propertyList[self.currentPropertyIndex].updatePriceRent(
                    self.propertyWidget.priceTextBox.text(),
                    self.propertyWidget.rentTextBox.text())

                if (self.propertyWidget.expensesWidget is not None):
                    expensesWidget = self.propertyWidget.expensesWidget
                    success &= self.propertyList[self.currentPropertyIndex].updateExpenses(
                        expensesWidget.vacancyRateTextBox.text(),
                        expensesWidget.taxRateTextBox.text(),
                        expensesWidget.maintenanceMiscYearTextBox.text(),
                        expensesWidget.utilitiesMonthTextBox.text(),
                        expensesWidget.HOAMonthTextBox.text(),
                        expensesWidget.insuranceMonthTextBox.text())

                if (self.propertyWidget.loanWidget is not None):
                    loanWidget = self.propertyWidget.loanWidget
                    success &= self.propertyList[self.currentPropertyIndex].updateLoan(
                        loanWidget.downPaymentRateTextBox.text(),
                        loanWidget.downPaymentDollarsTextBox.text(),
                        loanWidget.interestRateTextBox.text())

                if (success):
                    self.propertyList[self.currentPropertyIndex].calculate()
                    self.updatePropertyTable() # - may still be needed
                    #self.propertySelectionChanged()
                    self.updateTableSelection()

    def resetButton_Clicked(self):
        if (self.currentPropertyIndex >= 0 and len(self.propertyList) > self.currentPropertyIndex and
                    self.propertyList[self.currentPropertyIndex] is not None):
            self.propertyList[self.currentPropertyIndex].resetToDefaults()
            self.propertyList[self.currentPropertyIndex].calculate()
            self.updatePropertyTable() # - may still be needed
            #self.propertySelectionChanged()

    # ignoreSelectionChange = False
    # def propertySelectionChanged(self):
    #     if not self.ignoreSelectionChange:
    #         row = self.propertyTable.currentRow()
    #         zpidCell = self.propertyTable.item(row, 0)
    #         if zpidCell is not None:
    #             zpid = zpidCell.text()
    #             for i, prop in enumerate(self.propertyList):
    #                 if (zpid == prop.zp_id):
    #                     self.propertyWidget.setProperty(prop)
    #                     self.currentPropertyIndex = i
    #                     # connect property specific signals
    #                     self.propertyWidget.loanWidget.downPaymentRateTextBox.textChanged.connect(self.downPaymentRateChanged)
    #                     self.propertyWidget.loanWidget.downPaymentDollarsTextBox.textChanged.connect(self.downPaymentDollarsChanged)

    def propertyTableSelectionChanged(self, selected, deselected):
        indexes = selected.indexes()
        if len(indexes) > 0:
            selectedItem = indexes[0]
            zpid = selectedItem.data()
            self.updateTableSelection(zpid)
        #     for i, prop in enumerate(self.propertyList):
        #         if (zpid == prop.zp_id):
        #             self.propertyWidget.setProperty(prop)
        #             self.currentPropertyIndex = i
        #             self.propertyWidget.loanWidget.downPaymentRateTextBox.textChanged.connect(self.downPaymentRateChanged)
        #             self.propertyWidget.loanWidget.downPaymentDollarsTextBox.textChanged.connect(self.downPaymentDollarsChanged)

    def updateTableSelection(self, zpid = None):
        if (zpid is None):
            indexes = self.propertyTableView.selectedIndexes()
            if len(indexes) > 0:
                selectedItem = indexes[0]
                zpid = selectedItem.data()
        for i, prop in enumerate(self.propertyList):
            if (zpid != None and zpid == prop.getID()):
                self.propertyWidget.setProperty(prop)
                self.propertyWidget.loanWidget.downPaymentRateTextBox.textChanged.connect(self.downPaymentRateChanged)
                self.propertyWidget.loanWidget.downPaymentDollarsTextBox.textChanged.connect(self.downPaymentDollarsChanged)
                self.currentPropertyIndex = i

    def updatePropertyTable(self):
        #self.ignoreSelectionChange = True
        #self.propertyTable.clearRows()
        self.propertyTableData.clear()
        for prop in self.propertyList:
            if prop is not None:
                #self.propertyTable.addRow(prop.zp_id, prop.address, prop.price, prop.rent, prop.cap_rate, prop.total_net_month)
                self.propertyTableModel.insertRows(self.propertyTableModel.rowCount(), 1, [prop.getID(), prop.getAddress(), prop.getPrice(), prop.getRent(), prop.getCapRate(), prop.getTotalNetMonth()])
        #self.updateTableView()
        #self.ignoreSelectionChange = False

    def getPropertyIDs(self, zip):
        zpidList = []
        url = "http://www.zillow.com/homes/for_sale/" + zip
        pageNum = 1
        finished = False
        while not finished:
            zpidsOnPage = []
            pageUrl = url +"/" + pageNum.__str__() + "_p/"
            response = requests.get(pageUrl)
            html = response.content
            soup = BeautifulSoup(html, "html5lib")
            #zpidTags = soup.find_all(attrs={"data-zpid":True})
            zpidTags = soup.find_all(attrs={"data-zpid":True})

            for tag in zpidTags:
                zpid = tag['data-zpid']
                if (not zpidList.__contains__(zpid)):
                    zpidList.append(zpid)
                else:
                    finished = True

            pageNum += 1
            #temporary, limit results for testing
            #if pageNum > 1:
            #    break

        for id in zpidList:
            print(id)
        self.zpidList = zpidList

    def validatePostalCode(self, zip):
        if len(zip) == 5 and zip.isdigit():
            return True
        return False

    def getPropertyList(self):
        if (len(self.zpidList) > 0):
            #i = 0
            self.propertyList.clear()
            for zpid in self.zpidList:
                property = self.getPropertyFromZpid(zpid)
                if (property is not None and property.isValid() == True):
                    property.calculate()
                    self.propertyList.append(property)
                    # temporary, limits results for testing
                    #i += 1
                    #if (i > 2):
                    #    return

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
            results = soup.find_all(attrs={"class":"zest-title"})
            if (len(results) > 0):
                for result in results:
                    if ("Rent" in result.text):
                        rentNode = result.parent.find(attrs={"class":"zest-value"})
                        if (rentNode is not None):
                            try:
                                rent = int(re.sub('[^0-9]', '', rentNode.text))
                            except:
                                rent = None
                            break  # found rent estimate
        return rent

    downPaymentRateChanging = False
    downPaymentDollarsChanging = False
    def downPaymentRateChanged(self, newValue):
        if not self.downPaymentDollarsChanging:
            if (len(self.propertyList) > self.currentPropertyIndex and
                        self.propertyList[self.currentPropertyIndex] is not None):
                self.downPaymentRateChanging = True
                if self.propertyList[self.currentPropertyIndex].downPaymentRateChanged(newValue):
                    self.propertyWidget.loanWidget.downPaymentDollarsTextBox.setText(str(self.propertyList[self.currentPropertyIndex].down_payment_dollars))
        else:
            self.downPaymentDollarsChanging = False

    def downPaymentDollarsChanged(self, newValue):
        if not self.downPaymentRateChanging:
            if (len(self.propertyList) > self.currentPropertyIndex and
                        self.propertyList[self.currentPropertyIndex] is not None):
                self.downPaymentDollarsChanging = True
                if self.propertyList[self.currentPropertyIndex].downPaymentDollarsChanged(newValue):
                    self.propertyWidget.loanWidget.downPaymentRateTextBox.setText(str(self.propertyList[self.currentPropertyIndex].down_payment_rate))
        else:
            self.downPaymentRateChanging = False

def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = PropertyAnalyzerApp()            # We set the form to be our ExampleApp (design)
    form.show()                             # Show the form
    app.exec_()                             # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
