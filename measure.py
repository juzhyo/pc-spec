# -*- coding: utf-8 -*-

############################
# PC-SPEC                  #
# AUTHOR: JUSTIN ZHOU YONG #
############################

from PyQt5 import QtCore as qtc
from PyQt5 import QtChart as qtch
from PyQt5 import QtGui as qtg

from collections import deque
import time

class measure(qtc.QObject):
    measure_started = qtc.pyqtSignal()
    measure_moved = qtc.pyqtSignal()
    measure_finished = qtc.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.pm100d = None
        self.sr830 = None
        self.lltf = None
        self.x_chart = None
        
        num_data_points = 80
        self.x_chart_data = deque([0]*num_data_points, maxlen=num_data_points)

        
    @qtc.pyqtSlot(object)    
    def set_sr830(self, sr830):
        self.sr830 = sr830
        
    @qtc.pyqtSlot(object)    
    def set_lltf(self, lltf):
        self.lltf = lltf
        
    @qtc.pyqtSlot(object)    
    def set_pm100d(self, pm100d):
        self.pm100d = pm100d

    @qtc.pyqtSlot()    
    def set_x_chart(self, x_chart):
        self.x_chart = x_chart
        
    @qtc.pyqtSlot()        
    def run(self):
        self.measure_started.emit()
        print('hi')
        self.x_chart_series = qtch.QLineSeries()
        self.x_chart.addSeries(self.x_chart_series)
        
        # power = self.pm100d.power*1e6
        x = self.sr830.x
        y = self.sr830.y
        r = self.sr830.magnitude
        theta = self.sr830.theta
        
        y_axis = qtch.QValueAxis()
        axisBrush = qtg.QBrush(qtg.QColor('#ffffff'))
        y_axis.setLabelsBrush(axisBrush)
        gridColor = qtg.QColor('#696969')
        # x_axis.setGridLineColor(gridColor)
        y_axis.setGridLineColor(gridColor)
        
        for i in range(10):
            x = self.sr830.x
            y = self.sr830.y
            r = self.sr830.magnitude
            theta = self.sr830.theta
            
            self.x_chart_data.append(theta)
        
            # y_axis.setRange(min(self.trace_display_data), max(self.trace_display_data))

            new_data = [qtc.QPointF(x, y) for x, y in enumerate(self.x_chart_data)]
            self.x_chart_series.replace(new_data)
            
            # self.x_chart.setAxisY(y_axis, self.x_chart_series)
            
            time.sleep(1)
        
        
        self.measure_finished.emit()