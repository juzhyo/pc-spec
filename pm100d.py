# -*- coding: utf-8 -*-

############################
# PC-SPEC                  #
# AUTHOR: JUSTIN ZHOU YONG #
############################

from PyQt5 import QtCore as qtc
from PyQt5 import QtChart as qtch
from PyQt5 import QtGui as qtg
from pymeasure.instruments.thorlabs import ThorlabsPM100USB

from collections import deque

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
        self.trace_display = None
        self.trace_display_chart = None
        self.trace_display_series = None
        
        num_data_points = 80
        self.trace_display_data = deque([0]*num_data_points, maxlen=num_data_points)
        
    @qtc.pyqtSlot(object)    
    def set_instrument(self, instrument):
        self.pm100d = instrument
    
    @qtc.pyqtSlot(object)    
    def set_lcd(self, lcd):
        self.lcd = lcd
        
    @qtc.pyqtSlot(object)    
    def set_trace_display(self, trace_display):
        self.trace_display = trace_display

    @qtc.pyqtSlot(object)    
    def set_trace_display_chart(self, chart):
        self.trace_display_chart = chart
        
    @qtc.pyqtSlot(object)    
    def set_trace_display_series(self, series):
        self.trace_display_series = series
    
    @qtc.pyqtSlot()
    def run(self):      
        self.timer=qtc.QTimer(interval=1000, timeout=self.refresh)
        self.timer.start()
        
        # self.lcd.display(self.pm100d.power*1e6)

    def refresh(self):
        self.lcd.display(self.pm100d.power*1e6)
        
        y_axis = qtch.QValueAxis()
        axisBrush = qtg.QBrush(qtg.QColor('#ffffff'))
        y_axis.setLabelsBrush(axisBrush)
        gridColor = qtg.QColor('#696969')
        # x_axis.setGridLineColor(gridColor)
        y_axis.setGridLineColor(gridColor)
        
        self.trace_display_data.append(self.pm100d.power*1e6)
        
        # print(max(self.trace_display_data))

        y_axis.setRange(min(self.trace_display_data), max(self.trace_display_data))

        new_data = [qtc.QPointF(x, y) for x, y in enumerate(self.trace_display_data)]
        self.trace_display_series.replace(new_data)
            
        # self.pm100d_trace_display_chart.setAxisY(y_axis, self.trace_display_series)
        # self.trace_display.setChart(self.trace_display_chart)
        

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