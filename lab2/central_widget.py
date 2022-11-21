from PyQt5 import QtWidgets
from table_widgets import InputTableWidget, OutputTableWidget

class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
                
        self.tableInput = InputTableWidget()
        
        self.tableOutput = OutputTableWidget(self.tableInput)    
        
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.tableInput)
        main_layout.addWidget(self.tableOutput)
        
        self.setLayout(main_layout)