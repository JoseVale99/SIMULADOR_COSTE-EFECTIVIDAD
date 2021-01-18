
import sys
from PyQt5.QtWidgets import QApplication
from App import*
from qtpy.QtGui import QIcon


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_simulator = App()
    app_simulator.setWindowIcon(QIcon("icoApp.ico"))
    app_simulator.resize(1200, 530)
    app_simulator.setWindowTitle("Simulador COSTE-EFECTIVIDAD en el tratamiento de la esquizofrenia ")
    app_simulator.show()
    sys.exit(app.exec_())
    
