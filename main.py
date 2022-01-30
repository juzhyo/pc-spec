#!/usr/bin/env python

############################
# THE ONE-MAN ARMY KNIFE   #
# AUTHOR: JUSTIN ZHOU YONG #
############################

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from PyQt5 import QtChart as qtch
from PyQt5 import QtGui as qtg

MW_Ui, MW_Base = uic.loadUiType('mainwindow.ui')

class MainWindow(MW_Base, MW_Ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_buttons()

        self.show()

    def set_buttons(self):
        run_action = self.toolBar.addAction('Run')
        stop_action = self.toolBar.addAction('Stop')
        
        open_icon = self.style().standardIcon(qtw.QStyle.SP_DirOpenIcon)
        save_icon = self.style().standardIcon(qtw.QStyle.SP_DriveHDIcon)
        run_icon = self.style().standardIcon(qtw.QStyle.SP_MediaPlay)
        stop_icon = self.style().standardIcon(qtw.QStyle.SP_MediaStop)
                
        run_action.setIcon(run_icon)
        stop_action.setIcon(stop_icon)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    mv = MainWindow()
    sys.exit(app.exec())
