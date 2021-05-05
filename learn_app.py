#!/usr/bin/env python
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
import sys
import dictionary_lookup
import project_handling
import json

class CustomTextEdit(QTextEdit):
	def selectText(self, status):
		if status == True:
			word = QApplication.clipboard().text()
			#print(word)
	
	def lookupWord(self):
		command = self._message
		#print(command)
		if len(command)>0:
			result = dictionary_lookup.lookup_meaning(command)
			msg = QMessageBox()
			msg.setWindowTitle("Meaning")
			msg.setText(result)
			x = msg.exec_() 
			
	def showMenu(self):
		self._normalMenu = self.createStandardContextMenu()
		self._normalMenu.addSeparator()
		self._normalMenu.addAction("Lookup", self.lookupWord)
		self._normalMenu.exec_(QCursor.pos())
		
	def setMessage(self, message):
		self._message=message
		
			
	def __init__(self, parent=None):
		self.parent = parent
		super(CustomTextEdit, self).__init__(parent)
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.showMenu)
		self.copyAvailable.connect(self.selectText)
		


class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		
		self.main_widget = MainWidget(parent=self)
		self.setCentralWidget(self.main_widget)
		
		#self.menuBar = QtGui.QMenuBar(self)
		mainMenu = self.menuBar()
		
		fileMenu = mainMenu.addMenu('File')
		open_action = QtWidgets.QAction('Open', self)
		fileMenu.addAction(open_action)
		
		save_action = QtWidgets.QAction('Save', self)
		save_action.setShortcut("Ctrl+S")
		save_action.setStatusTip('Save Project')
		save_action.triggered.connect(self.file_save)
		fileMenu.addAction(save_action)
		
		close_action = QtWidgets.QAction('Close', self)
		fileMenu.addAction(close_action)
		close_action.triggered.connect(self.close)
		
		self.resize(1000,700)
		
	
		
	def file_save(self):
		data = {	
			'text' : "sample text",
			'words' : {
				'wört1': 'Bedeutung'
			}
		}
		filename = QFileDialog.getSaveFileName(self, 'Save File', '', 'Json Files (*.json)', options=QFileDialog.DontUseNativeDialog)
		print(filename)
		if filename[0] == '':
			return 0
		if not str(filename[0]).endswith('.json'):
			filename = str(filename[0]) + ".json"
		else:
			filename = str(filename[0])
		with open(filename, 'w', encoding='utf8') as fp:
			json.dump(data, fp, ensure_ascii=False) 
		#file = open(name,'w')
		#text = self.textEdit.toPlainText()
		#file.write(text)
		#file.close()

class MainWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		

		'''self.createTopLeftGroupBox()
		self.createTopRightGroupBox()'''
		self.createBottomLeftTabWidget()
		'''self.createBottomRightGroupBox()
		self.createProgressBar()'''

		'''styleComboBox.activated[str].connect(self.changeStyle)
		self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
		disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
		disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
		disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
		disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)'''

		topLayout = QHBoxLayout()
		#topLayout.addWidget(styleLabel)
		#topLayout.addWidget(styleComboBox)
		topLayout.addStretch(1)
		
		mainLayout = QGridLayout()
		mainLayout.addLayout(topLayout,0, 0, 1, 1)
		#mainLayout.addLayout(topLayout, 0, 0, 1, 0)
		'''mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
		mainLayout.addWidget(self.topRightGroupBox, 1, 1)'''
		mainLayout.addWidget(self.bottomLeftTabWidget,1,0)
		'''mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
		mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
		mainLayout.setRowStretch(1, 1)
		mainLayout.setRowStretch(2, 1)
		mainLayout.setColumnStretch(0, 1)
		mainLayout.setColumnStretch(1, 1)'''
		self.setLayout(mainLayout)

		self.setWindowTitle("Learn German")
		self.changeStyle('Fusion')
		
		
	def changeStyle(self, styleName):
		QApplication.setStyle(QStyleFactory.create(styleName))
		QApplication.setPalette(QApplication.style().standardPalette())
		
	
			
	def createBottomLeftTabWidget(self):
		self.bottomLeftTabWidget = QTabWidget()
		self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
				QSizePolicy.Ignored)

		tab1 = QWidget()
		tableWidget = QTableWidget(10, 2)

		tab1hbox = QHBoxLayout()
		tab1hbox.setContentsMargins(5, 5, 5, 5)
		tab1hbox.addWidget(tableWidget)
		tab1.setLayout(tab1hbox)

		tab2 = QWidget()
		textEdit = CustomTextEdit()
		self.edit = textEdit
		self.edit.selectionChanged.connect(self.handleSelectionChanged)
		#textEdit.copyAvailable.connect(self.lookupWord)

		tab2hbox = QHBoxLayout()
		tab2hbox.setContentsMargins(5, 5, 5, 5)
		tab2hbox.addWidget(textEdit)
		tab2.setLayout(tab2hbox)

		self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")
		#self.bottomLeftTabWidget.addTab(tab1, "&Table")
		
	def handleSelectionChanged(self):
		selected_text = self.edit.textCursor().selectedText()
		# process text here...
		#print(selected_text)
		self.edit.setMessage(selected_text)

	




if __name__ == '__main__':
	# Every GUI app must have exactly one instance of QApplication
	app = QApplication([])
	app.setApplicationName("Learn German")
	app.setWindowIcon(QtGui.QIcon('images/logo.png')) 
	cb = QApplication.clipboard()
	cb.clear(mode=cb.Clipboard )
	gallery = MainWindow()
	gallery.show()
	
	# Run the application until the user closes it
	sys.exit(app.exec_())


