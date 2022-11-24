from PyQt5 import QtWidgets
from table_widgets import OutputTableWidget

class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.inputUI = InputUI()
        self.tableOutput = OutputTableWidget()    
        
        main_layout = QtWidgets.QVBoxLayout()
        self.inputUI.addToLayout(main_layout)
        main_layout.addWidget(self.tableOutput)
        
        self.setLayout(main_layout)
        
class InputUI():
    def __init__(self):
        expression = "2*x1 + 4*x2 - x1**2 - 2*x2**2"
        bounds = "x1 + 2*x2 >= 8\n2*x1 - x2 <= 12"
        startPoint = [0, 0]
        accuracy = 0.01
        
        self.expressionLine = QtWidgets.QLineEdit(expression)
        self.boundsText = QtWidgets.QPlainTextEdit(bounds)
        self.startPoint = [QtWidgets.QLineEdit(str(point)) for point in startPoint]
        self.accuracy = QtWidgets.QLineEdit(str(accuracy))
        
        UI = (
            self.expressionLine,
            self.boundsText,
            self.startPoint,
            self.accuracy
        )
        
    def addToLayout(self, layout):
        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(QtWidgets.QLabel("F="))
        hLayout.addWidget(self.expressionLine)
        hLayout.addWidget(QtWidgets.QLabel("X="))
        for point in self.startPoint: hLayout.addWidget(point)
        hLayout.addWidget(QtWidgets.QLabel("E="))
        hLayout.addWidget(self.accuracy)
        layout.addLayout(hLayout)
        
        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(QtWidgets.QLabel("g="))
        hLayout.addWidget(self.boundsText)

        layout.addLayout(hLayout)
        
    def getUIContains(self):
        return self.expressionLine.text(), self.boundsText.toPlainText(), \
            [pointEdit.text() for pointEdit in self.startPoint], self.accuracy.text()
        