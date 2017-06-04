__author__ = 'ianabshire'

class Property():
    def __init__(self, zp_id=0, address="", city="", state="", zip=0, price=0, rent=0):
        self.zp_id = zp_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.price_original = price
        self.rent_original = rent
        self.price = price
        self.rent = rent

        # expenses
        self.vacancy_rate = 0.0
        self.tax_rate = 0.0
        self.maintenance_misc_year = 0.0
        self.utilities_month = 0.0
        self.HOA_month = 0.0
        self.insurance_month = 0.0

        # loan
        self.down_payment_rate = 0.0
        self.down_payment_dollars = 0.0
        self.loan_amount = 0.0
        self.interest_rate = 0.0
        self.loan_payment_month = 0.0

        # calculated
        self.annual_income = 0.0
        self.annual_expenses = 0.0
        self.annual_net_income = 0.0
        self.cap_rate = 0.0
        self.total_cost_month = 0.0
        self.total_net_month = 0.0

        self.resetToDefaults()
        self.calculate()

    def resetToDefaults(self):
        self.price = self.price_original
        self.rent = self.rent_original

        defaults = DefaultValues()
        if defaults is not None:
            # expenses
            self.vacancy_rate = defaults.vacancy_rate
            self.tax_rate = defaults.tax_rate
            self.maintenance_misc_year = defaults.maintenance_misc_year
            self.utilities_month = defaults.utilities_month
            self.HOA_month = defaults.HOA_month
            self.insurance_month = defaults.insurance_month

            # loan
            self.down_payment_rate = defaults.down_payment_rate
            self.down_payment_dollars = defaults.down_payment_dollars
            self.loan_amount = defaults.loan_amount
            self.interest_rate = defaults.interest_rate
            self.loan_payment_month = defaults.loan_payment_month

        # calculated
        self.annual_income = 0.0
        self.annual_expenses = 0.0
        self.annual_net_income = 0.0
        self.cap_rate = 0.0
        self.total_cost_month = 0.0
        self.total_net_month = 0.0

    def isValid(self):
        if (self.zp_id != None and self.address != None and self.price != None and self.rent != None):
            return True
        else:
            return False

    def calculate(self):
        self.down_payment_dollars = self.price * (self.down_payment_rate / 100)
        self.loan_amount = self.price - self.down_payment_dollars
        rate = ((self.interest_rate / 100) /12)  # monthly interest rate
        if (rate > 0):
            self.loan_payment_month = self.loan_amount * ((rate * pow(1 + rate, 360)) / (pow(1 + rate, 360) - 1))
        else:
            self.loan_payment_month = self.loan_amount / 360
        self.annual_income = self.rent * 12
        self.annual_expenses = (self.maintenance_misc_year +
                                ((self.vacancy_rate / 100) * self.annual_income) +
                                ((self.tax_rate / 100) * self.price) +
                                (self.utilities_month * 12) +
                                (self.HOA_month * 12) +
                                (self.insurance_month * 12))
        if (self.price > 0):
            self.annual_net_income = self.annual_income - self.annual_expenses
            self.cap_rate = (self.annual_net_income / self.price) * 100
        else:
            self.annual_net_income = self.annual_income - self.annual_expenses
            self.cap_rate = 0.0
        self.total_cost_month = self.loan_payment_month + (self.annual_expenses / 12)
        self.total_net_month = self.rent - self.total_cost_month

    def updatePriceRent(self, price, rent):
        if not (price == rent == None):
            try:
                self.price = float(price)
                self.rent = float(rent)
                return True
            except:
                return False
        else:
            return False

    def updateExpenses(self, vacancy_rate, tax_rate, maintenance_misc_year, utilities_month, HOA_month, insurance_month):
        if not (vacancy_rate == tax_rate == maintenance_misc_year == utilities_month == HOA_month == insurance_month == None):
            try:
                self.vacancy_rate = float(vacancy_rate)
                self.tax_rate = float(tax_rate)
                self.maintenance_misc_year = float(maintenance_misc_year)
                self.utilities_month = float(utilities_month)
                self.HOA_month = float(HOA_month)
                self.insurance_month = float(insurance_month)
                return True
            except:
                return False
        else:
            return False

    def updateLoan(self, down_payment_rate, down_payment_dollars, interest_rate):
        if not (down_payment_rate == down_payment_dollars == interest_rate == None):
            try:
                self.down_payment_rate = float(down_payment_rate)
                self.down_payment_dollars = float(down_payment_dollars)
                self.interest_rate = float(interest_rate)
                return True
            except:
                return False
        else:
            return False

    def downPaymentRateChanged(self, newValue):
        if (newValue is not None and newValue is not ""):
            try:
                rate = float(newValue)
                self.down_payment_dollars = self.price * (rate/100)
                return True
            except:
                self.down_payment_dollars = 0.0
                return False
        return True

    def downPaymentDollarsChanged(self, newValue):
        if (newValue is not None and newValue is not ""):
            try:
                dollars = float(newValue)
                self.down_payment_rate = (dollars / self.price) * 100
                return True
            except:
                self.down_payment_rate = 0.0
                return False
        return True

    def getID(self):
        return self.zp_id

    def setID(self, zp_id):
        self.zp_id = zp_id

    def getAddress(self):
        return self.address

    def setAddress(self, address):
        self.address = address

    def getCity(self):
        return self.city

    def setCity(self, city):
        self.city = city

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def getZip(self):
        return self.zip

    def setZip(self, zip):
        self.zip = zip

    def getPrice(self):
        return self.price

    def setPrice(self, price):
        self.price = price

    def getRent(self):
        return self.rent

    def setRent(self, rent):
        self.rent = rent

    def getCapRate(self):
        return self.cap_rate

    def setCapRate(self, cap_rate):
        self.cap_rate = cap_rate

    def getTotalNetMonth(self):
        return self.total_net_month

    def setTotalNetMonth(self, total_net_month):
        self.total_net_month = total_net_month


class DefaultValues():
    def __init__(self):

        # default values
        # expenses
        self.vacancy_rate = 5.0
        self.tax_rate = 1.0
        self.maintenance_misc_year = 1000.0
        self.utilities_month = 50.0
        self.HOA_month = 350.0
        self.insurance_month = 100.0

        # loan
        self.down_payment_rate = 25.0
        self.down_payment_dollars = 0.0
        self.loan_amount = 0.0
        self.interest_rate = 4.0
        self.loan_payment_month = 0.0