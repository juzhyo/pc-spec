# -*- coding: utf-8 -*-

############################
# PC-SPEC                  #
# AUTHOR: JUSTIN ZHOU YONG #
############################

from pyxphyspec import *
import win32com.client
from win32com.client import DispatchBaseClass

# IXPHySpecTunableFilter.MovetoWavelength(lltf,532)

def connect(self):
    try:
        # lltfApp = win32com.client.Dispatch("XPHySpec.XPhySpec.1")
        # lltf = win32com.client.Dispatch("XPHySpec.XPhySpec")

        # lltfApp.InitializeSystem()
        # lltfApp.DetectDevices()
        # self.lltf = lltfApp.GetDeviceInterface("M000236001")

        self.parameters_lltf.setEnabled(True)
                
    except:
        self.log_box.append('<span style="color:lightcoral">[ERROR] LLTF connection failed<\span>')
        self.parameters_sr830.setDisabled(True)
        return
            
    self.log_box.append('<span style="color:palegreen">[SUCCESS] LLTF connected</span>')
    
    return

def MovetoWavelength(wavelength):
    IXPHySpecTunableFilter.MovetoWavelength(self.lltf, wavelength)
    
def update_current_wavelength(self):
    self.parameters_lltf_current_wavelength.setValue(self.parameters_lltf_current_wavelength_slider.value())
    
def update_current_wavelength_slider(self):
    self.parameters_lltf_current_wavelength_slider.setValue(self.parameters_lltf_current_wavelength.value())
