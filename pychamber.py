# -*- coding: utf-8 -*-

'''
PyChamber
By Doctus (kirikayuumura.noir@gmail.com)

	A minimalist, low-distraction text editor based on PyQt.

    PyChamber is free software: you can
    redistribute it and/or modify it under the terms of the GNU General
    Public License as published by the Free Software Foundation, either
    version 3 of the License, or (at your option) any later version.

    RandomGameGenerator is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PyChamber.  If not, see <http://www.gnu.org/licenses/>.
'''

try:
	from PyQt5.QtCore import *
	from PyQt5.QtGui import *
	from PyQt5.QtWidgets import *
except ImportError:
	from PyQt4.QtCore import *
	from PyQt4.QtGui import *
import os, sys

if sys.version_info >= (3, 0):
	PYTHON_THREE = True
else:
	PYTHON_THREE = False

class MainWidget(QTextEdit):

	def __init__(self, *args, **kwargs):
		super(MainWidget, self).__init__(*args, **kwargs)
		self.setStyleSheet("background-color:black; color:green;")
		
	def changeColors(self, bg="black", fg="green"):
		self.setStyleSheet("background-color:%s; color:%s;" % (bg, fg))

class MainWindow(QMainWindow):

	def __init__(self):
		QMainWindow.__init__(self)

		self.setObjectName("MainWindow")
		self.setWindowTitle("PyChamber")
		self.settings = QSettings("Doctus", "PyChamber")
		self.mainWidget = MainWidget()
		self.setCentralWidget(self.mainWidget)
		self.showFullScreen()
		self.currentFilePath = None
		self.openShortcut = QShortcut(QKeySequence("Ctrl+O"), self)
		self.openShortcut.activated.connect(self.openFile)
		self.saveShortcut = QShortcut(QKeySequence("Ctrl+S"), self)
		self.saveShortcut.activated.connect(self.saveFile)
		self.saveAsShortcut = QShortcut(QKeySequence("Ctrl+Shift+S"), self)
		self.saveAsShortcut.activated.connect(self.saveFileAs)
		self.newShortcut = QShortcut(QKeySequence("Ctrl+N"), self)
		self.newShortcut.activated.connect(self.newFile)
		self.colorShortcut = QShortcut(QKeySequence("Ctrl+K"), self)
		self.colorShortcut.activated.connect(self.selectColors)
		self.exitShortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
		self.exitShortcut.activated.connect(sys.exit)
		if not PYTHON_THREE:
			self.errorDialog = QErrorMessage(self)
			self.errorDialog.showMessage("It is recommended to run PyChamber with Python 3 if you plan to edit non-ASCII files; this version does not have Unicode support. (Your Python version is %s)" % ".".join([str(i) for i in sys.version_info[:3]]), "updatepython")
		
	def selectColors(self, *args, **kwargs):
		newForeground = QColorDialog.getColor(Qt.darkGreen, self)
		if newForeground.isValid():
			fg = newForeground.name()
		else:
			fg = "green"
		newBackground = QColorDialog.getColor(Qt.black, self)
		if newBackground.isValid():
			bg = newBackground.name()
		else:
			bg = "black"
		self.mainWidget.changeColors(fg=fg, bg=bg)
		
	def newFile(self, *args, **kwargs):
		self.mainWidget.setPlainText("")
		self.currentFilePath = None
		
	def openFile(self, *args, **kwargs):
		oldFilePath = self.currentFilePath
		filePath = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*.*)")
		if PYTHON_THREE:
			filePath = filePath[0]
		if filePath is not None and len(filePath) > 0:
			try:
				if PYTHON_THREE:
					kw = {"encoding":"utf-8"}
				else:
					kw = {}
				with open(filePath, "r", **kw) as f:
					data = f.read()
				self.mainWidget.setPlainText(data)
				self.currentFilePath = filePath
			except Exception as e:
				self.currentFilePath = oldFilePath
				self.errorDialog = QErrorMessage(self)
				self.errorDialog.showMessage("Couldn't open file as text. (%s)" % e, "fileopenfail")
			
	def _saveFile(self, filePath):
		oldFilePath = self.currentFilePath
		try:
			if PYTHON_THREE:
				kw = {"encoding":"utf-8"}
			else:
				kw = {}
			with open(filePath, "w", **kw) as f:
				f.write(self.mainWidget.toPlainText())
			self.currentFilePath = filePath
		except Exception as e:
			self.currentFilePath = oldFilePath
			self.errorDialog = QErrorMessage(self)
			self.errorDialog.showMessage("Couldn't save file to that path. (%s)" % e, "filesavefail")
			
	def saveFile(self, *args, **kwargs):
		if self.currentFilePath is not None:
			filePath = self.currentFilePath
		else:
			filePath = QFileDialog.getSaveFileName(self, "Save As...", "", "Text Files (*.txt);;All Files (*.*)")
			if PYTHON_THREE:
				filePath = filePath[0]
		if filePath is not None and len(filePath) > 0:
			self._saveFile(filePath)
		
	def saveFileAs(self, *args, **kwargs):
		filePath = QFileDialog.getSaveFileName(self, "Save As...", "", "Text Files (*.txt);;All Files (*.*)")
		if PYTHON_THREE:
				filePath = filePath[0]
		if filePath is not None and len(filePath) > 0:
			self._saveFile(filePath)

app = QApplication(["PyChamber"])
app.setApplicationName("PyChamber");
app.setOrganizationName("Doctus");
app.setOrganizationDomain("daydreamspiral.com");
main = MainWindow()
main.show()
app.exec_()