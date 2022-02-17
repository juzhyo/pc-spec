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
    x = qtc.pyqtSignal(float)
    theta = qtc.pyqtSignal(float)
    power = qtc.pyqtSignal(float)

    
    def __init__(self):
        super().__init__()
        self.pm100d = None
        self.sr830 = None
        self.lltf = None
        self.x_chart = None
        self.plots_theta = None
        
        # num_data_points = 80
        # self.x_chart_data = deque([0]*num_data_points, maxlen=num_data_points)

        
    @qtc.pyqtSlot(object)    
    def set_sr830(self, sr830):
        self.sr830 = sr830
        
    @qtc.pyqtSlot(object)    
    def set_lltf(self, lltf):
        self.lltf = lltf
        
    @qtc.pyqtSlot(object)    
    def set_pm100d(self, pm100d):
        self.pm100d = pm100d
        
    @qtc.pyqtSlot(int)    
    def set_num_data_points(self, num_data_points):
        self.num_data_points = num_data_points

    @qtc.pyqtSlot()    
    def set_x_chart(self, x_chart):
        self.x_chart = x_chart
        
    @qtc.pyqtSlot()    
    def set_plots_theta(self, plots_theta):
        self.plots_theta = plots_theta
        
    @qtc.pyqtSlot()        
    def run(self):
        self.measure_started.emit()
        
        print('started')
        self.x_chart_series = qtch.QScatterSeries()
        self.x_chart.addSeries(self.x_chart_series)
        
        # self.theta_chart = qtch.QChart()
        # self.theta_chart.setMargins(qtc.QMargins(0,0,0,0))
        # self.theta_chart.setTheme(qtch.QChart.ChartThemeLight)
        # self.theta_chart.setBackgroundVisible(False)
        # self.theta_chart.setBackgroundRoundness(0)
        # self.theta_chart.layout().setContentsMargins(0,0,0,0)
        self.theta_chart_series = qtch.QScatterSeries()
        # self.theta_chart.addSeries(self.theta_chart_series)
        
        self.x_data = []
        self.x.connect(self.plot_x)
        
        self.theta_data = []
        # self.theta.connect(self.plot_theta)
        
        for i in range(self.num_data_points):
            time.sleep(2*self.sr830.time_constant)
            # time.sleep(1)
            try:
                self.update()
            except VisaIOError:
                self.update()
        
        # power = self.pm100d.power*1e6
        # x = self.sr830.x
        # y = self.sr830.y
        # r = self.sr830.magnitude
        # theta = self.sr830.theta
        
        # y_axis = qtch.QValueAxis()
        # axisBrush = qtg.QBrush(qtg.QColor('#ffffff'))
        # y_axis.setLabelsBrush(axisBrush)
        # gridColor = qtg.QColor('#696969')
        # # x_axis.setGridLineColor(gridColor)
        # y_axis.setGridLineColor(gridColor)
        
        # for i in range(10):
        #     x = self.sr830.x
        #     y = self.sr830.y
        #     r = self.sr830.magnitude
        #     theta = self.sr830.theta
            
        #     print(theta)
            
        #     self.x_chart_data.append(theta)
        
        #     # y_axis.setRange(min(self.trace_display_data), max(self.trace_display_data))

        #     new_data = [qtc.QPointF(x, y) for x, y in enumerate(self.x_chart_data)]
        #     self.x_chart_series.replace(new_data)
            
        #     self.x_chart.setAxisY(y_axis, self.x_chart_series)
            
        #     time.sleep(1)
        
        
        self.measure_finished.emit()

    @qtc.pyqtSlot()        
    def update(self):
        # move wavelength
        # wait
        # measure pc
        # measure power
        # wait
        
        time.sleep(self.sr830.time_constant)
        self.x.emit(self.sr830.x)
        self.theta.emit(self.sr830.theta)
        self.power.emit(self.pm100d.power*1e6)
        time.sleep(self.sr830.time_constant)
        
    @qtc.pyqtSlot(float)
    def plot_x(self, x):
        # append data point to series
        # add series to chart
        # set chart
        
        self.x_data.append(x)
        new_data = [qtc.QPointF(x, y) for x, y in enumerate(self.x_data)]
        self.x_chart_series.replace(new_data)

    # @qtc.pyqtSlot(float)
    # def plot_theta(self, theta):
    #     # append data point to series
    #     # add series to chart
    #     # set chart
        
    #     self.theta_chart = self.plots_theta.chart()
        
    #     y_axis = qtch.QValueAxis()
    #     y_axis.setRange(-1e-5, 1e-5)
    
    #     gridColor = qtg.QColor('#696969')
    #     y_axis.setGridLineColor(gridColor)
        
    #     # y_axis = self.plots_theta.axisY()
    #     # self.theta_chart.setMargins(qtc.QMargins(0,0,0,0))
    #     # self.theta_chart.setTheme(qtch.QChart.ChartThemeLight)
    #     # self.theta_chart.setBackgroundVisible(False)
    #     # self.theta_chart.setBackgroundRoundness(0)
    #     # self.theta_chart.layout().setContentsMargins(0,0,0,0)
        
    #     # self.plots_theta.setChart(self.theta_chart)
        
    #     self.theta_data.append(theta)
    #     new_data = [qtc.QPointF(x, y) for x, y in enumerate(self.theta_data)]
    #     self.theta_chart_series.replace(new_data)
        
    #     # x_axis = qtch.QValueAxis()
    #     # x_axis.setRange(0, len(self.theta_data))
        
    #     # y_axis.setRange(0, 2)
    
    #     # gridColor = qtg.QColor('#696969')
    #     # x_axis.setGridLineColor(gridColor)
    #     # y_axis.setGridLineColor(gridColor)
        
    #     # self.theta_chart.setAxisX(x_axis, self.theta_chart_series)
        # self.theta_chart.setAxisY(y_axis, self.theta_chart_series)