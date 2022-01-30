#!/usr/bin/env python

############################
# THE ONE-MAN ARMY KNIFE   #
# AUTHOR: JUSTIN ZHOU YONG #
############################

import sys
import pyvisa
import qdarkstyle

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
        self.populate_resources()

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
        
    def populate_resources(self):
        """Populate a combobox with available resource addresses"""
    
        resources_list = pyvisa.ResourceManager().list_resources()
        
        resources_list_ASRL = sorted(resources_list,key=self.sort_ASRL)
        resources_list_GPIB = sorted(resources_list,key=self.sort_GPIB)
        resources_list_USB = sorted(resources_list,key=self.sort_USB)
        
        
        for i in range(len(resources_list)):
            self.equipments_sr830_address.addItem(resources_list_GPIB[i],i)
            self.equipments_lltf_address.addItem(resources_list_ASRL[i],i)
            self.equipments_b2902a_address.addItem(resources_list_ASRL[i],i)
            self.equipments_pm100d_address.addItem(resources_list_USB[i],i)

    def sort_ASRL(self, value):
        return value[0:4] != 'ASRL'
            
    def sort_GPIB(self, value):
        return value[0:4] != 'GPIB'
    
    def sort_USB(self, value):
        return value[0:3] != 'USB'
            
    def get_resources(self):
        return pyvisa.ResourceManager().list_resources()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    mv = MainWindow()
    sys.exit(app.exec())
