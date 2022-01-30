#!/usr/bin/env python

############################
# THE ONE-MAN ARMY KNIFE   #
# AUTHOR: JUSTIN ZHOU YONG #
############################

import sys
import pyvisa
import qdarkstyle
import sr830

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
        
        # SR830 Lock-in amplifier
        self.equipments_sr830_connect.clicked.connect(lambda: sr830.connect(self, self.equipments_sr830_address.currentText()))
        self.parameters_sr830_time_constant.currentIndexChanged.connect(lambda: sr830.set_parameters(self,'time_constant'))
        self.parameters_sr830_filter_slope.currentIndexChanged.connect(lambda: sr830.set_parameters(self,'filter_slope'))
        self.parameters_sr830_input_config.currentIndexChanged.connect(lambda: sr830.set_parameters(self,'input_config'))
        self.parameters_sr830_frequency.valueChanged.connect(lambda: sr830.set_parameters(self,'frequency'))
        self.parameters_sr830_input_coupling_ac.clicked.connect(lambda: sr830.set_parameters(self,'input_coupling'))
        self.parameters_sr830_input_coupling_dc.clicked.connect(lambda: sr830.set_parameters(self,'input_coupling'))
        self.parameters_sr830_input_grounding_float.clicked.connect(lambda: sr830.set_parameters(self,'input_grounding'))
        self.parameters_sr830_input_grounding_ground.clicked.connect(lambda: sr830.set_parameters(self,'input_grounding'))
        self.parameters_sr830_sensitivity.currentIndexChanged.connect(lambda: sr830.set_parameters(self,'sensitivity'))
        self.parameters_sr830_channel1.currentIndexChanged.connect(lambda: sr830.set_parameters(self,'channel1'))
        self.parameters_sr830_channel2.currentIndexChanged.connect(lambda: sr830.set_parameters(self,'channel2'))


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
    

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    mv = MainWindow()
    sys.exit(app.exec())
