__author__ = 'ianabshire'

import sys, locale
from PyQt5 import QtCore, QtGui, QtWidgets
from PropertyAnalyzer_GUI import Ui_MainWindow
from Property import Property
from PropertyData import PropertyData


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
        #self.zpidList = []
        self.propertyList = []
        self.currentPropertyIndex = -1

        self.propertyData = PropertyData()

        #testing
        #prop = Property(99, "123 Elm St.", "Benicia", "CA", 94510, 100000, 2000)
        #self.propertyList.append(prop)
        #self.updatePropertyTable()
        #self.currentPropertyIndex = 0

    def searchButton_Clicked(self):
        zip = self.searchTextBox.text()
        if zip != "":
            if (self.propertyData.validatePostalCode(zip)):
                #self.zpidList = self.propertyData.getPropertyIDs(zip)
                #if (len(self.zpidList) > 0):
                self.propertyList = self.propertyData.getPropertyList(zip)
                if self.propertyList is not None:
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
