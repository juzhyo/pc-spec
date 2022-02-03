# -*- coding: utf-8 -*-

############################
# PC-SPEC                  #
# AUTHOR: JUSTIN ZHOU YONG #
############################

from PyQt5 import QtCore as qtc
from pymeasure.instruments.thorlabs import ThorlabsPM100USB

class instrument(qtc.QObject):
    # dataChanged = pyqtSignal(float, float, float, float)
    log_str = qtc.pyqtSignal(str)
    enable_instrument = qtc.pyqtSignal(str)
    instrument = qtc.pyqtSignal(object)

    def __init__(self, parent=None):
        qtc.QThread.__init__(self, parent)
        
    
    def connect(self, resource_name):
        try:
            ThorlabsPM100USB(resource_name).id
            # self.parameters_pm100d.setEnabled(True)
            self.pm100d = ThorlabsPM100USB(resource_name)
            self.enable_instrument.emit('PM100D')
        
            # sr830_parameters = read_parameters(self)
        
            # print(sr830_parameters.get('sensitivity'))
        
            # self.parameters_sr830_time_constant.setCurrentIndex(10)
        
            # set_parameters(self,initialize=True)	

            # self.parameters_sr830_time_constant.setItemText("asdf")        
                
        except:
            self.log_str.emit('<span style="color:lightcoral">[ERROR] PM100D connection failed<\span>')
            # self.log_box.append('<span style="color:lightcoral">[ERROR] PM100D connection failed<\span>')
            # self.parameters_pm100d.setDisabled(True)
            return
            
        self.log_str.emit('<span style="color:palegreen">[SUCCESS] PM100D connected</span>')
        self.instrument.emit(ThorlabsPM100USB(resource_name))
    
        return ThorlabsPM100USB(resource_name)
    
    # def update_lcd(self):
    #     self.power.emit(self.pm100d.power)
        
    #     return
    
    
    
class live(qtc.QObject):
    
    def __init__(self):
        super().__init__()
        self.pm100d = None
        self.lcd = None
        
    @qtc.pyqtSlot(object)    
    def set_instrument(self, instrument):
        self.pm100d = instrument
    
    @qtc.pyqtSlot(object)    
    def set_lcd(self, lcd):
        self.lcd = lcd

    # def onDataChanged(self, RPM, Torque, HorsePower, Run_Time):
    #     self.lcdNumber_4.display(RPM)
    #     self.lcdNumber_5.display(Torque)
    #     self.lcdNumber_6.display(HorsePower)
    #     self.lcdNumber_7.display(Run_Time)
    
    @qtc.pyqtSlot()
    def run(self):
        self.timer=qtc.QTimer(interval=500, timeout=self.refresh)
        self.timer.start()
        
        # self.lcd.display(self.pm100d.power*1e6)

    def refresh(self):
        self.lcd.display(self.pm100d.power*1e6)
        

    # def __del__(self):  # part of the standard format of a QThread
    #     self.wait()

    # def run(self):  # also a required QThread function, the working part
    #     self.Arduino.close()
    #     self.Arduino.open()

    #     self.Arduino.flush()
    #     self.Arduino.reset_input_buffer()
    #     start_time = time.time()

    #     while True:
    #         while self.Arduino.inWaiting() == 0:
    #             pass
    #         try:
    #             data = self.Arduino.readline()
    #             dataarray = data.decode().rstrip().split(',')
    #             self.Arduino.reset_input_buffer()
    #             Force = round(float(dataarray[0]), 3)
    #             RPM = round(float(dataarray[1]), 3)
    #             Torque = round(Force * GetData.Distance, 3)
    #             HorsePower = round(Torque * RPM / 5252, 3)
    #             Run_Time = round(time.time() - start_time, 3)
    #             print(Force, 'Grams', ",", RPM, 'RPMs', ",", Torque, "ft-lbs", ",", HorsePower, "hp", Run_Time,
    #                   "Time Elasped")
    #             self.dataChanged.emit(RPM, Torque, HorsePower, Run_Time)
    #         except (KeyboardInterrupt, SystemExit, IndexError, ValueError):
    #             pass