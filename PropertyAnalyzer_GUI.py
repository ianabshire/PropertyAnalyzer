import sys, locale
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import Qt, QVariant


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        from Property import Property  # import after init to avoid circular dependency
        MainWindow.setObjectName("PropertyAnalyzer")
        MainWindow.resize(800, 600)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.grid = QtWidgets.QGridLayout(self.centralWidget)
        self.grid.setSpacing(10)


        # self.verticalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        # self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 800, 600))
        # self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        # self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        # self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        # self.verticalLayout.setSpacing(6)
        # self.verticalLayout.setObjectName("verticalLayout")
        #
        #
        # self.searchHorizLayoutWidget = QtWidgets.QWidget(self.verticalLayoutWidget)
        # self.searchHorizLayoutWidget.setGeometry(QtCore.QRect(0, 0, 800, 600))
        # self.searchHorizLayoutWidget.setObjectName("searchHorizLayoutWidget")
        # self.searchHorizLayout = QtWidgets.QHBoxLayout(self.searchHorizLayoutWidget)
        #
        #
        # # search label
        # self.searchLabel = QtWidgets.QLabel(self.searchHorizLayoutWidget)
        # self.searchLabel.setObjectName("searchLabel")
        # self.searchHorizLayout.addWidget(self.searchLabel)
        # # search text box
        # self.searchTextBox = QtWidgets.QLineEdit(self.searchHorizLayoutWidget)
        # self.searchTextBox.setObjectName("searchTextBox")
        # self.searchHorizLayout.addWidget(self.searchTextBox)
        # # search button
        # self.searchButton = QtWidgets.QPushButton(self.searchHorizLayoutWidget)
        # self.searchButton.setObjectName("searchButton")
        # self.searchHorizLayout.addWidget(self.searchButton)
        #
        # self.verticalLayout.addWidget(self.searchHorizLayoutWidget)
        #
        # # property list
        # self.propertyList = PropertyList()
        #
        # self.verticalLayout.addWidget(self.propertyList)
        #
        # self.verticalLayout.addWidget(gettablewidget(self))



        # search label
        self.searchLabel = QtWidgets.QLabel()
        self.searchLabel.setObjectName("searchLabel")
        self.grid.addWidget(self.searchLabel, 0, 0)
        # search text box
        self.searchTextBox = QtWidgets.QLineEdit()
        self.searchTextBox.setObjectName("searchTextBox")
        self.grid.addWidget(self.searchTextBox, 0, 1)
        # search button
        self.searchButton = QtWidgets.QPushButton()
        self.searchButton.setObjectName("searchButton")
        self.grid.addWidget(self.searchButton, 0, 2)

        #self.propertyTable = PropertyTable()
        #self.grid.addWidget(self.propertyTable, 1, 0, 1, 3)

        # property details
        defaultProp = Property(99, "123 Elm St.", "Benicia", "CA", 94510, 100000, 2000)
        self.propertyWidget = PropertyWidget(defaultProp)
        self.grid.addWidget(self.propertyWidget, 2, 0, 1, 3)

        # buttons
        self.buttonGridLayout = QtWidgets.QGridLayout()
        self.buttonGridLayout.addItem(QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum), 0, 0, 1, 1)
        self.applyButton = QtWidgets.QPushButton()
        self.applyButton.setObjectName("applyButton")
        self.buttonGridLayout.addWidget(self.applyButton, 0, 1, 1, 1)
        self.resetButton = QtWidgets.QPushButton()
        self.resetButton.setObjectName("resetButton")
        self.buttonGridLayout.addWidget(self.resetButton, 0, 2, 1, 1)
        self.buttonGridLayout.addItem(QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum), 0, 3, 1, 1)
        self.grid.addLayout(self.buttonGridLayout, 3, 1, 1, 1)


        # property table view
        self.propertyTableData = [[99, "123 Elm St.", 100000, 2000, 0, 0]]
        self.header = ['ZPID','Address','Price','Rent','Cap Rate','Net(/mo)']
        self.propertyTableView = None
        self.createTable()
        self.tableGridLayout = QtWidgets.QGridLayout()
        self.tableGridLayout.addWidget(self.propertyTableView, 0, 0, 1, 1)
        self.grid.addLayout(self.tableGridLayout, 1, 0, 1, 3)

        MainWindow.setCentralWidget(self.centralWidget)

        # menu bar
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuQT_Test = QtWidgets.QMenu(self.menuBar)
        self.menuQT_Test.setObjectName("menuQT_Test")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar.addAction(self.menuQT_Test.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("PropertyAnalyzer", "Property Analyzer"))
        self.searchButton.setText(_translate("PropertyAnalyzer", "Search"))
        self.searchLabel.setText(_translate("PropertyAnalyzer", "Enter ZIP to search:"))

        self.applyButton.setText(_translate("PropertyAnalyzer", "Apply"))
        self.resetButton.setText(_translate("PropertyAnalyzer", "Reset"))
        self.menuQT_Test.setTitle(_translate("PropertyAnalyzer", "Property Analyzer"))

    def createTable(self):
        # create the view
        self.propertyTableView = QtWidgets.QTableView()
        self.propertyTableView.setStyleSheet("gridline-color: rgb(191, 191, 191)")

        # set the table model
        self.propertyTableModel = PropertyTableModel(self.propertyTableData, self.header, self)
        self.propertyTableView.setModel(self.propertyTableModel)

        # set the minimum size
        self.propertyTableView.setMinimumSize(400, 300)

        # hide grid
        self.propertyTableView.setShowGrid(True)

        # set the font
        font = QtGui.QFont("Calibri (Body)", 12)
        self.propertyTableView.setFont(font)

        # hide vertical header
        vh = self.propertyTableView.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = self.propertyTableView.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        #self.propertyTableView.resizeColumnsToContents()

        # set row height
        nrows = len(self.propertyTableData)
        for row in range(nrows):
            self.propertyTableView.setRowHeight(row, 18)

        # enable sorting
        self.propertyTableView.setSortingEnabled(True)
        self.propertyTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)


class PropertyWidget(QtWidgets.QWidget):
    def __init__(self, property, parent=None):
        #super(PropertyWidget, self).__init__(parent)
        super().__init__()
        self.property = property
        self.gridLayout = None
        self.createWidgets()


    def createWidgets(self):
        self.gridLayout = QtWidgets.QGridLayout()
        # horizontalLayout = QtWidgets.QHBoxLayout()

        # details
        self.zp_idLabel = QtWidgets.QLabel("ID: " + str(self.property.zp_id))
        self.addressLabel = QtWidgets.QLabel(self.property.address)
        self.cszLabel = QtWidgets.QLabel(self.property.city + ", " + self.property.state + " " + str(self.property.zip))

        # price
        self.priceLabel = QtWidgets.QLabel("Price ($):")
        self.priceTextBox = QtWidgets.QLineEdit()
        self.priceTextBox.setObjectName("priceTextBox")
        self.priceTextBox.setText(str(self.property.price))

        #rent
        self.rentLabel = QtWidgets.QLabel("Rent ($):")
        self.rentTextBox = QtWidgets.QLineEdit()
        self.rentTextBox.setObjectName("rentTextBox")
        self.rentTextBox.setText(str(self.property.rent))

        #cap/net
        self.capLabel = QtWidgets.QLabel("Cap Rate (%):  " + "{:-.2f}".format(self.property.cap_rate))  #locale.format("%d", self.property.cap_rate, grouping=True))
        self.netLabel = QtWidgets.QLabel("Net/Mo ($):  " + "{:-.2f}".format(self.property.total_net_month))  #locale.format("%d", self.property.total_net_month, grouping=True))

        # layout
        self.gridLayout.addWidget(self.addressLabel, 1, 0)
        self.gridLayout.addWidget(self.cszLabel, 2, 0)
        self.gridLayout.addWidget(self.zp_idLabel, 3, 0)
        self.gridLayout.addWidget(self.priceLabel, 1, 1)
        self.gridLayout.addWidget(self.priceTextBox, 1, 2)
        self.gridLayout.addWidget(self.rentLabel, 2, 1)
        self.gridLayout.addWidget(self.rentTextBox, 2, 2)
        self.gridLayout.addWidget(self.capLabel, 1, 3)
        self.gridLayout.addWidget(self.netLabel, 2, 3)

        self.tabs = QtWidgets.QTabWidget()

        self.expensesWidget = ExpensesWidget(self.property)
        self.tabs.addTab(self.expensesWidget, "Expenses")

        self.loanWidget = LoanWidget(self.property)
        self.tabs.addTab(self.loanWidget, "Loan")

        self.resultsWidget = ResultsWidget(self.property)
        self.tabs.addTab(self.resultsWidget, "Results")

        self.gridLayout.addWidget(self.tabs, 4, 0, 1, 4)

        # horizontalLayout.addWidget(self.label)
        # horizontalLayout.addWidget(self.label2)
        # self.setLayout(horizontalLayout)

        #self.setLayout(self.gridLayout)
        self.setLayout(self.gridLayout)

    def setProperty(self, prop):
        #self.property = None
        #layout = None
        #self.gridLayout = None

        self.property = prop
        layout = self.layout()
        if layout is not None:
            QtWidgets.QWidget().setLayout(self.layout())
        self.createWidgets()

    def getText(self):
        return


class ExpensesWidget(QtWidgets.QWidget):
    def __init__(self, property):
        super().__init__()

        self.property = property

        self.grid = QtWidgets.QGridLayout()
        # expenses
        self.expensesLabel = QtWidgets.QLabel("Expenses")
        self.grid.addWidget(self.expensesLabel, 0, 0)
        # vacancy rate
        self.vacancyRateLabel = QtWidgets.QLabel("Vacancy Rate (%):")
        self.grid.addWidget(self.vacancyRateLabel, 1, 0)
        self.vacancyRateTextBox = QtWidgets.QLineEdit()
        self.vacancyRateTextBox.setObjectName("vacancyRateTextBox")
        self.vacancyRateTextBox.setText(str(self.property.vacancy_rate))
        self.grid.addWidget(self.vacancyRateTextBox, 1, 1)
        # tax rate
        self.taxRateLabel = QtWidgets.QLabel("Tax Rate (%):")
        self.grid.addWidget(self.taxRateLabel, 2, 0)
        self.taxRateTextBox = QtWidgets.QLineEdit()
        self.taxRateTextBox.setObjectName("taxRateTextBox")
        self.taxRateTextBox.setText(str(self.property.tax_rate))
        self.grid.addWidget(self.taxRateTextBox, 2, 1)
        # maint/misc
        self.maintenanceMiscYearLabel = QtWidgets.QLabel("Maint & Misc/Year ($):")
        self.grid.addWidget(self.maintenanceMiscYearLabel, 3, 0)
        self.maintenanceMiscYearTextBox = QtWidgets.QLineEdit()
        self.maintenanceMiscYearTextBox.setObjectName("maintenanceMiscYearTextBox")
        self.maintenanceMiscYearTextBox.setText(str(self.property.maintenance_misc_year))
        self.grid.addWidget(self.maintenanceMiscYearTextBox, 3, 1)
        # utilities
        self.utilitiesMonthLabel = QtWidgets.QLabel("Utilities/Month ($):")
        self.grid.addWidget(self.utilitiesMonthLabel, 1, 3)
        self.utilitiesMonthTextBox = QtWidgets.QLineEdit()
        self.utilitiesMonthTextBox.setObjectName("utilitiesMonthTextBox")
        self.utilitiesMonthTextBox.setText(str(self.property.utilities_month))
        self.grid.addWidget(self.utilitiesMonthTextBox, 1, 4)
        # HOA
        self.HOAMonthLabel = QtWidgets.QLabel("HOA/Month ($):")
        self.grid.addWidget(self.HOAMonthLabel, 2, 3)
        self.HOAMonthTextBox = QtWidgets.QLineEdit()
        self.HOAMonthTextBox.setObjectName("HOAMonthTextBox")
        self.HOAMonthTextBox.setText(str(self.property.HOA_month))
        self.grid.addWidget(self.HOAMonthTextBox, 2, 4)
        # insurance
        self.insuranceMonthLabel = QtWidgets.QLabel("Insurance/Month ($):")
        self.grid.addWidget(self.insuranceMonthLabel, 3, 3)
        self.insuranceMonthTextBox = QtWidgets.QLineEdit()
        self.insuranceMonthTextBox.setObjectName("insuranceMonthTextBox")
        self.insuranceMonthTextBox.setText(str(self.property.insurance_month))
        self.grid.addWidget(self.insuranceMonthTextBox, 3, 4)

        self.setLayout(self.grid)


class LoanWidget(QtWidgets.QWidget):
    def __init__(self, property):
        super(LoanWidget, self).__init__()

        self.property = property

        self.grid = QtWidgets.QGridLayout()
        # loan
        self.loanLabel = QtWidgets.QLabel("Loan")

        # down payment rate
        self.downPaymentRateLabel = QtWidgets.QLabel("Down Payment Rate (%):")
        self.downPaymentRateTextBox = QtWidgets.QLineEdit()
        self.downPaymentRateTextBox.setObjectName("downPaymentRateTextBox")
        self.downPaymentRateTextBox.setText(str(self.property.down_payment_rate))

        # down payment dollars
        self.downPaymentDollarsLabel = QtWidgets.QLabel("Down Payment ($):")
        self.downPaymentDollarsTextBox = QtWidgets.QLineEdit()
        self.downPaymentDollarsTextBox.setObjectName("downPaymentDollarsTextBox")
        self.downPaymentDollarsTextBox.setText(str(self.property.down_payment_dollars))

        # interest rate
        self.interestRateLabel = QtWidgets.QLabel("Interest Rate (%):")
        self.interestRateTextBox = QtWidgets.QLineEdit()
        self.interestRateTextBox.setObjectName("interestRateTextBox")
        self.interestRateTextBox.setText(str(self.property.interest_rate))

        # loan amount
        self.loanAmountLabel = QtWidgets.QLabel("Loan Amount ($): " + "{:-.2f}".format(self.property.loan_amount))
        #self.loanAmountTextBox = QtWidgets.QLineEdit()
        #self.loanAmountTextBox.setObjectName("maintenanceMiscYearTextBox")
        #self.loanAmountTextBox.setText(str(self.property.loan_amount))
        #self.grid.addWidget(self.loanAmountTextBox, 3, 1)

        # loan payment month
        self.loanPaymentMonthLabel = QtWidgets.QLabel("Loan Payment/Month ($): " + "{:-.2f}".format(self.property.loan_payment_month))
        #self.loanPaymentMonthTextBox = QtWidgets.QLineEdit()
        #self.loanPaymentMonthTextBox.setObjectName("loanPaymentMonthTextBox")
        #self.loanPaymentMonthTextBox.setText(str(self.property.loan_payment_month))
        #self.grid.addWidget(self.loanPaymentMonthTextBox, 2, 4)

        #layout
        self.grid.addWidget(self.loanLabel, 0, 0)

        self.grid.addWidget(self.downPaymentRateLabel, 1, 0)
        self.grid.addWidget(self.downPaymentRateTextBox, 1, 1)
        self.grid.addWidget(self.downPaymentDollarsLabel, 2, 0)
        self.grid.addWidget(self.downPaymentDollarsTextBox, 2, 1)
        self.grid.addWidget(self.interestRateLabel, 3, 0)
        self.grid.addWidget(self.interestRateTextBox, 3, 1)

        self.grid.addWidget(self.loanAmountLabel, 1, 3, 1, 2)
        self.grid.addWidget(self.loanPaymentMonthLabel, 2, 3, 1, 2)

        self.setLayout(self.grid)


class ResultsWidget(QtWidgets.QWidget):
    def __init__(self, property):
        super().__init__()

        self.property = property

        self.grid = QtWidgets.QGridLayout()
        # results
        self.resultsLabel = QtWidgets.QLabel("Results")

        # total cost/month
        self.totalCostMonthLabel = QtWidgets.QLabel("Total Cost/Month ($): " + "{:-.2f}".format(self.property.total_cost_month))

        # total net/month
        self.totalNetMonthLabel = QtWidgets.QLabel("Total Net/Month ($): " + "{:-.2f}".format(self.property.total_net_month))

        self.grid.addWidget(self.resultsLabel, 0, 0)
        self.grid.addWidget(self.totalCostMonthLabel, 1, 0)
        self.grid.addWidget(self.totalNetMonthLabel, 2, 0)

        self.setLayout(self.grid)


# class PropertyList(QtWidgets.QListWidget):
#     def __init__(self):
#         QtWidgets.QListWidget.__init__(self)
#         self.itemClicked.connect(self.findSel)
#
#     def addItemToList(self, zp_id, address, city, state, zip, price, rent):
#         itemSize = QtCore.QSize(200, 110)
#         label = PropertyWidget(zp_id, address, city, state, zip, price, rent)
#         item = QtWidgets.QListWidgetItem()
#         item.setSizeHint(itemSize)
#         self.addItem(item)
#         self.setItemWidget(item, label)
#         self.setSelectionMode(1)            # 1 = SingleSelection, 2 = MultiSelection, not necessary, default mode is singleSelection
#         self.setGeometry(200, 200, 300, 500)
#
#     def findSel(self, current):
#         currentItem = self.itemWidget(current)
#         lblTxt = currentItem.getText()
#         print(lblTxt)


# class PropertyTableItem(QtWidgets.QTableWidgetItem):
#     def __lt__(self, other):
#         if ( isinstance(other, QtWidgets.QTableWidgetItem) ):
#             if type(self.data(Qt.EditRole)) == int:
#                 my_value = self.data(Qt.EditRole)
#                 my_ok = True
#             else:
#                 my_value, my_ok = self.data(Qt.EditRole).toInt()
#             if type(other.data(Qt.EditRole)) == int:
#                 other_value = other.data(Qt.EditRole)
#                 other_ok = True
#             else:
#                 other_value, other_ok = other.data(Qt.EditRole).toInt()
#
#             if ( my_ok and other_ok ):
#                 return my_value < other_value
#
#         return super(PropertyTableItem, self).__lt__(other)
#
#
# class PropertyTable(QtWidgets.QTableWidget):
#     def __init__(self):
#         QtWidgets.QTableWidget.__init__(self)
#
#         #widget.setWindowFlags(QtWidgets.Dialog)
#         self.setSortingEnabled(True)
#
#         #self.setHorizontalHeaderLabels()
#
#         self.setRowCount(0)
#         self.setColumnCount(6)
#
#         headers = "ZPID;Address;Price;Rent;Cap Rate;Net(/mo)".split(";")
#         self.setHorizontalHeaderLabels(headers)
#         #for i, header in enumerate(headers):
#          #   self.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(header))
#         # for row in range(50):
#         #     # create a normal QTableWidgetItem
#         #     a = QtWidgets.QTableWidgetItem()
#         #     a.setText(str(row))
#         #     self.setItem(row, 0, a)
#         #
#         #     # create a proper sorted item
#         #     b = QtWidgets.QTableWidgetItem()
#         #     b.setData(Qt.EditRole, QVariant(row))
#         #     self.setItem(row, 1, b)
#         #
#         #     # create a custom sorted item
#         #     c = PropertyTableItem()
#         #     c.setData(Qt.EditRole, QVariant(row))
#         #     self.setItem(row, 2, c)
#
#     def addRow(self, zpid, address=None, price=None, rent=None, cap=None, net=None):
#         numRows = self.rowCount()
#         self.setRowCount(numRows + 1)
#
#         zpidItem = QtWidgets.QTableWidgetItem()
#         zpidItem.setData(Qt.EditRole, QVariant(zpid))
#         self.setItem(numRows, 0, zpidItem)
#
#         addressItem = QtWidgets.QTableWidgetItem()
#         addressItem.setData(Qt.EditRole, QVariant(address))
#         self.setItem(numRows, 1, addressItem)
#
#         priceItem = QtWidgets.QTableWidgetItem()
#         priceItem.setData(Qt.EditRole, QVariant(price))
#         self.setItem(numRows, 2, priceItem)
#
#         rentItem = QtWidgets.QTableWidgetItem()
#         rentItem.setData(Qt.EditRole, QVariant(rent))
#         self.setItem(numRows, 3, rentItem)
#
#         capItem = QtWidgets.QTableWidgetItem()
#         capItem.setData(Qt.EditRole, QVariant(cap))
#         self.setItem(numRows, 4, capItem)
#
#         netItem = QtWidgets.QTableWidgetItem()
#         netItem.setData(Qt.EditRole, QVariant(net))
#         self.setItem(numRows, 5, netItem)
#
#     def clearRows(self):
#         while (self.rowCount() > 0):
#             self.removeRow(0)




class PropertyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, header, parent=None, *args):
        """ datain: a list of lists
            headerdata: a list of strings
        """

        super(PropertyTableModel, self).__init__()
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.__data = data     # Initial Data
        self.header = header

    def rowCount( self, parent=None ):
        return len(self.__data)

    def columnCount( self , parent=None ):
        return len(self.__data[0])

    def data ( self , index , role ):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__data[row][column]
            return str(value)

    def setData(self, index, value):
        self.__data[index.row()][index.column()] = value
        return True

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsSelectable

    def insertRows(self , position , rows , item , parent=QtCore.QModelIndex()):
        # beginInsertRows (self, QModelIndex parent, int first, int last)
        self.beginInsertRows(QtCore.QModelIndex(),position,position)
        self.__data.append(item) # Item must be an array
        self.endInsertRows()
        return True

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header[col])
        return QVariant()

    #def sort(self, Ncol, order):
    #    """Sort table by given column number.
    #    """
    #    self.emit(QtWidgets.SIGNAL("layoutAboutToBeChanged()"))
    #    self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
    #    if order == Qt.DescendingOrder:
    #        self.arraydata.reverse()
    #    self.emit(QtWidgets.SIGNAL("layoutChanged()"))