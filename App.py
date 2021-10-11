# importar modulos a utilizar
import style
from PyQt5.QtWidgets import QVBoxLayout, \
QFrame,QWidget, QGridLayout, QHBoxLayout, QFileDialog, \
QLabel, QLineEdit, QPushButton, QTableWidget,QTableWidgetItem
from PyQt5 import QtCore
from pyqtgraph import PlotWidget ,exporters,mkPen
import database
from numpy import arange,exp
from PIL import Image

class App(QWidget):
    def __init__(self):
        super().__init__()
        
        #todo: Agregar estilos a nuestro proyecto
        self.setStyleSheet(style.style)
        self.layoutUI()
        
        self.tabletas_zipra = 28;
        self.tabletas_rispe = 40
        self.tabletas_halo = 20
        self.tabletas_olan = 14
        self.tabletas_cloza = 30
        
        self.zipra_dia = 2
        self.rispe_dia = 2
        self.halo_dia = 2
        self.olan_dia = 1
        self.cloza_dia = 2
      
    def layoutUI(self):   
        # layout principal
        self.principalLayout = QHBoxLayout(self)
        
        # primer Frame
        self.firstFrame = QFrame(self)
        self.firstFrame.setFrameShape(QFrame.StyledPanel)
        self.firstFrame.setFrameShadow(QFrame.Raised)
        self.firstFrame.setObjectName("contenedor1")
        # Frame II
        self.second_Frame = QFrame()
        self.second_Frame.setObjectName("contenedor2")
        
        
        # Layouts
        self.verticalLayout = QVBoxLayout(self.firstFrame)
        self.gridLayout = QGridLayout()
        
        self.grafic_principal = QVBoxLayout(self.second_Frame)
        self.grafic_plot = QVBoxLayout()
        
        self.layout_button =  QGridLayout()

        self.text_title = QLabel(
        "Análisis de Simulación de coste - efectividad en el\ntratamiento de la esquizofrenia")
        self.text_title.setAlignment(QtCore.Qt.AlignCenter)
        self.text_title.setObjectName("tittle")
        self.grafic_principal.addWidget(self.text_title)
        
        self.text_salida = QLabel(
        "Salidas")
        self.text_salida.setAlignment(QtCore.Qt.AlignCenter)
        self.text_salida.setObjectName("salida")
    
    
        labels = {(1,0):"Ziprasidona", (2,0):"Risperidona",
        (3,0):"Haloperidol",(4,0):"Olanzapina",(5,0):"Clozapina",(6,1):""}
        self.lbl_costo = QLabel("COSTO $")
        self.lbl_costo.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.lbl_costo, 0, 1)
        a = database.CargarDatos()
        
        self.text_ziprasidona = QLineEdit(str(a[0][2]))
        self.text_ziprasidona.setAlignment(QtCore.Qt.AlignCenter)
        self.text_ziprasidona.setEnabled(False)
        self.gridLayout.addWidget(self.text_ziprasidona, 1, 1)
        
        self.text_Risperidona = QLineEdit(str(a[1][2]))
        self.text_Risperidona.setAlignment(QtCore.Qt.AlignCenter)
        self.text_Risperidona.setEnabled(False)
        self.gridLayout.addWidget(self.text_Risperidona, 2, 1)
        
        
        self.text_haloperidol = QLineEdit(str(a[2][2]))
        self.text_haloperidol.setAlignment(QtCore.Qt.AlignCenter)
        self.text_haloperidol.setEnabled(False)
        self.gridLayout.addWidget(self.text_haloperidol, 3, 1)
        
        self.text_olanzapina = QLineEdit(str(a[3][2]))
        self.text_olanzapina.setAlignment(QtCore.Qt.AlignCenter)
        self.text_olanzapina.setEnabled(False)
        self.gridLayout.addWidget(self.text_olanzapina, 4, 1)
        
        self.text_clozapina = QLineEdit(str(a[4][2]))
        self.text_clozapina.setEnabled(False)
        self.text_clozapina.setAlignment(QtCore.Qt.AlignCenter)
        
        
        
        self.gridLayout.addWidget(self.text_clozapina, 5, 1)
        
        for pos, name in labels.items():
            x, y = pos
            lbl = QLabel(self.firstFrame)
            lbl.setText(name)
            self.gridLayout.addWidget(lbl, x, y)
            
        self.verticalLayout.addLayout(self.gridLayout)
        self.principalLayout.addWidget(self.firstFrame)
        
    
        #?   Parte de la Grafica 
        self.graphWidget = PlotWidget()
        self.graphWidget.showGrid(x = True, y = True)
        self.graphWidget.addLegend()
        
        self.graphWidget.setTitle("Entrada",color="w", size="22px")
        
        styles = {"color": "#fff", "font-size": "23px"}
        self.graphWidget.setLabel("left", " Pr (la intervención es óptima) ", **styles)
        self.graphWidget.setLabel("bottom", "Financiamiento disponible para IMSS", **styles)        
        self.grafic_plot.addWidget(self.graphWidget)
        
        self.grafic_principal.addLayout(self.grafic_plot)
        self.principalLayout.addWidget(self.second_Frame)
        
        
        self.verticalLayout.addWidget(self.text_salida)
        #! Tabla 
        
        self.table = QTableWidget(5, 4,self.firstFrame) 
        self.table.setHorizontalHeaderLabels(['TRATAMIENTO ',
        'PRESENTACIÓN  ', 'PRECIO IMSS  ','COSTO DIARIO '])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        
        
        self.verticalLayout.addWidget(self.table)
    
        #! Boton 
        
        self.start_simulation = QPushButton(" Iniciar simulación")
        self.start_simulation.clicked.connect(self.event_simulation)
        self.start_simulation.setObjectName("buttonsim")
        
        self.button_save = QPushButton("Guardar plot")
        self.button_save.setObjectName("save")
        self.button_save.hide()
        self.button_save.clicked.connect(self.saveFig)
        
        self.grafic_plot.addWidget(self.button_save)
        
        self.layout_button.addWidget(self.start_simulation,0,1)
        self.verticalLayout.addLayout(self.layout_button)
        
    #Todo cargar datos desde la bdd
    def simulation_data(self):
        database.connnection()
        a = database.CargarDatos()
        
        for i in range(len(a)):
            for j in range(len(a[i])):
                self.table.setItem(i,j,QTableWidgetItem(str(a[i][j])))
    
    #Todo Event simulator
    def event_simulation(self):
        self.simulation_data()
        prob_zipra=4.4
        prob_aloper=0.06
        prob_clozapina=0.9
        prob_risper=0.007
        prob_olanzap=0.01
        y_zipra = []
        y_aloper = []
        y_clozapina = []
        y_olanzap = []
        y_risper = []
        x = arange(0,1000,1)

        for y in x:
            y_zipra.append(1+exp(-prob_zipra*int(y)))
            y_aloper.append(1+exp(-prob_aloper*int(y)))
            y_clozapina.append(1-exp(-prob_clozapina*int(y)))
            y_olanzap.append(1-exp(-prob_olanzap*int(y)))
            y_risper.append(1-exp(-prob_risper*int(y)))  
    
        self.graphWidget.setXRange(-0.2,22,padding=0)
        self.graphWidget.setYRange(-0.1,2.3,padding=0)
        
        self.plot(x,y_zipra,'Ziprasidona','r',"o")
        self.plot(x,y_aloper,'Haloperidol','y',"t1")
        self.plot(x,y_clozapina,'Clozapina','b',"x")
        self.plot_2(x,y_olanzap,'Olanzapina','g',"p")
        self.plot_2(x,y_risper,'Risperidona','s',"+")
        
        self.costo_diario_zipra = round(float(self.text_ziprasidona.text())/(self.tabletas_zipra/self.zipra_dia),4)
        self.costo_diario_rispe = round(float(self.text_Risperidona.text())/(self.tabletas_rispe/self.rispe_dia),4)
        self.costo_diario_halo = round(float(self.text_haloperidol.text())/(self.tabletas_halo/self.halo_dia),4)
        self.costo_diario_olan = round(float(self.text_olanzapina.text())/(self.tabletas_olan/self.olan_dia),4)
        self.costo_diario_cloza = round(float(self.text_clozapina.text())/(self.tabletas_cloza/self.cloza_dia),4)
        
        self.table.setItem(0,3,QTableWidgetItem(str(self.costo_diario_zipra)))
        self.table.setItem(1,3,QTableWidgetItem(str(self.costo_diario_rispe)))
        self.table.setItem(2,3,QTableWidgetItem(str(self.costo_diario_halo)))
        self.table.setItem(3,3,QTableWidgetItem(str(self.costo_diario_olan)))
        self.table.setItem(4,3,QTableWidgetItem(str(self.costo_diario_cloza)))
        
        
        self.button_save.show()
        self.start_simulation.setEnabled(False)       
    
    def plot(self, x, y, plotname, color,symbol):
        pen = mkPen(color=color,style=QtCore.Qt.DashLine)
        self.graphWidget.plot(x, y, name=plotname, pen=pen, symbol=symbol, symbolSize=10, symbolBrush=(color))
    
    def plot_2(self, x, y, plotname, color,symbol):
        pen = mkPen(color=color,style=QtCore.Qt.DashLine)
        self.graphWidget.plot(x, y, name=plotname, symbol=symbol,pen=pen, symbolSize=10, symbolBrush=(color))
    
    # Guardar la imagen en un directorio de nuestro ordenador
    def saveFig(self):
        exp = exporters.ImageExporter(self.graphWidget.plotItem)
        exp.parameters()['width'] = 1000
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName,_ = QFileDialog.getSaveFileName(self,
        "QFileDialog.getSaveFileName()","Plot.png","All Files (*);;Text Files (*.png)", options=options)
        
        if fileName !="":
            exp.export(fileName)
            imagen = Image.open(fileName)
            imagen.show()
            