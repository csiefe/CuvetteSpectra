import sys
#Note that I have PyQt5 in which I don't need the package 'QtUi', QtWidgets is fine
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

qtCreatorFile = 'Tax_Calculator.ui'

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

#Note that here in the tutorial 'QtWidgets' was actually 'QtUi'
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.calc_tax_button.clicked.connect(self.CalculateTax)

    def CalculateTax(self):
        price = int(self.price_box.toPlainText())
        tax = (self.tax_rate.value())
        total_price = price + ((tax / 100) * price)
        total_price_string = 'The total price with tax is: ' + str(total_price)
        self.results_window.setText(total_price_string)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

