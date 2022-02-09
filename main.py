#!/usr/bin/env python

############################
# PC-SPEC                  #
# AUTHOR: JUSTIN ZHOU YONG #
############################

import sys
import pyvisa
import qdarkstyle
import sr830
import lltf
import pm100d
import measure
import numpy as np

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import uic
from PyQt5 import QtChart as qtch
from PyQt5 import QtGui as qtg

from collections import deque

MW_Ui, MW_Base = uic.loadUiType('mainwindow.ui')

class MainWindow(MW_Base, MW_Ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_buttons()
        self.populate_resources()
        self.measure_chart_setup()

        
        # SR830 lock-in amplifier
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
        
        
        # self.sr830_channel_view_thread = qtc.QThread()
        # self.sr830_channel_view_thread.start()
        self.sr830_channel_view()
        
        # Laser line tunable filter
        self.equipments_lltf_connect.clicked.connect(lambda: lltf.connect(self))
        self.parameters_lltf_current_wavelength.valueChanged.connect(lambda: lltf.update_current_wavelength_slider(self))
        self.parameters_lltf_current_wavelength_slider.valueChanged.connect(lambda: lltf.update_current_wavelength(self))
        # self.parameters_lltf_current_wavelength.keyPressEvent = qtc.pyqtSignal(int)
        
        # Thorlabs PM100D powermeter
        # self.equipments_pm100d_connect.clicked.connect(lambda: pm100d.connect(self, self.equipments_pm100d_address.currentText()))
        
        # self.pm100d = pm100d.instrument()
        
        self.equipments_pm100d_connect.clicked.connect(lambda: pm100d.connect(self, self.equipments_pm100d_address.currentText()))
        self.pm100d_chart_view()
        
        # self.pm100d.log_str.connect(self.update_log)
        # self.pm100d.enable_instrument.connect(self.enable_parameter_box)
        # self.pm100d.instrument.connect(self.pm100d_run_live)
        
        # self.pm100d_chart_setup()
       

        # self.pm100d_thread = qtc.QThread()
        # self.pm100d_live = pm100d.live()
        # self.pm100d_live.moveToThread(self.pm100d_thread)
        # self.pm100d_live.set_instrument(self.pm100d)
        # self.pm100d_live.set_lcd(self.parameters_pm100d_lcd)
        # self.pm100d_live.run()
        # self.pm100d_thread.start()
        
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
        
        run_action.setCheckable(True)
        
        run_action.changed.connect(lambda: self.run(run_action))
        
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
    
    def update_log(self, string):
        self.log_box.append(string)
        
    def enable_parameter_box(self, instrument):
        if instrument == "PM100D":
            self.parameters_pm100d.setEnabled(True)
            
    def pm100d_run_live(self,instrument):   
            self.pm100d_thread = qtc.QThread()
            self.pm100d_live = pm100d.live()
            self.pm100d_live.moveToThread(self.pm100d_thread)
            self.pm100d_live.set_instrument(instrument)
            self.pm100d_live.set_lcd(self.parameters_pm100d_lcd)
            self.pm100d_live.set_trace_display(self.parameters_pm100d_trace_display)
            self.pm100d_live.set_trace_display_chart(self.pm100d_trace_display_chart)
            self.pm100d_live.set_trace_display_series(self.pm100d_trace_display_series)
            self.pm100d_live.run()
            self.pm100d_thread.start()
            
    def pm100d_chart_view(self):
        num_data_points = 40
    
        x_axis = qtch.QValueAxis()
        x_axis.setRange(0, num_data_points)
        x_axis.setLabelsVisible(False)
        y_axis = qtch.QValueAxis()
        y_axis.setRange(-1e-5, 10)
    
        gridColor = qtg.QColor('#696969')
        x_axis.setGridLineColor(gridColor)
        y_axis.setGridLineColor(gridColor)
        
        self.pm100d_chart = qtch.QChart()
        self.pm100d_chart.setMargins(qtc.QMargins(0,-25,0,0))
        self.pm100d_chart.setTheme(qtch.QChart.ChartThemeLight)
        self.pm100d_chart.setBackgroundVisible(False)
        self.pm100d_chart.setBackgroundRoundness(0)
        self.pm100d_chart.layout().setContentsMargins(0,0,0,0)
        
        self.parameters_pm100d_trace_display.setChart(self.pm100d_chart)

        self.pm100d_series = qtch.QLineSeries()
        self.pm100d_chart.addSeries(self.pm100d_series)
            
        self.pm100d_data = deque([0]*num_data_points, maxlen=num_data_points)
        self.pm100d_series.append([qtc.QPointF(x,y) for x, y in enumerate(self.pm100d_data)])
        
        self.pm100d_chart.setAxisX(x_axis, self.pm100d_series)
        self.pm100d_chart.setAxisY(y_axis, self.pm100d_series)
    
        # chart.setRenderHint(qtg.QPainter.Antialiasing)

        self.pm100d_timer=qtc.QTimer(interval=500, timeout=self.pm100d_refresh_stats)
        # self.timer.timeout.connect(lambda: refresh_stats)
        self.pm100d_timer.start()
        
    def pm100d_refresh_stats(self):
        if self.parameters_pm100d.isEnabled():
            y_axis = qtch.QValueAxis()
            axisBrush = qtg.QBrush(qtg.QColor('#ffffff'))
            y_axis.setLabelsBrush(axisBrush)
            gridColor = qtg.QColor('#696969')
            # x_axis.setGridLineColor(gridColor)
            y_axis.setGridLineColor(gridColor)

            self.pm100d_data.append(self.pm100d.power*1e6)
            y_axis.setRange(np.floor(min(self.pm100d_data)), np.ceil(max(self.pm100d_data)))
                
            new_data = [qtc.QPointF(x, y) for x, y in enumerate(self.pm100d_data)]
            self.pm100d_series.replace(new_data)
            
            self.pm100d_chart.setAxisY(y_axis, self.pm100d_series)
            
            self.parameters_pm100d_lcd.display(self.pm100d.power*1e6)
    
    def sr830_channel_view(self):    
        num_data_points = 80
    
        channel1_x_axis = qtch.QValueAxis()
        channel1_x_axis.setRange(0, num_data_points)
        channel1_x_axis.setLabelsVisible(False)
        channel1_y_axis = qtch.QValueAxis()
        channel1_y_axis.setRange(-1e-5, 1e-5)
    
        channel1_gridColor = qtg.QColor('#696969')
        channel1_x_axis.setGridLineColor(channel1_gridColor)
        channel1_y_axis.setGridLineColor(channel1_gridColor)
        
        self.channel1_chart = qtch.QChart()
        self.channel1_chart.setMargins(qtc.QMargins(0,-25,0,0))
        self.channel1_chart.setTheme(qtch.QChart.ChartThemeLight)
        self.channel1_chart.setBackgroundVisible(False)
        self.channel1_chart.setBackgroundRoundness(0)
        self.channel1_chart.layout().setContentsMargins(0,0,0,0)
        
        self.parameters_sr830_channel1_display.setChart(self.channel1_chart)

        self.channel1_series = qtch.QLineSeries()
        self.channel1_chart.addSeries(self.channel1_series)
            
        self.channel1_data = deque([0]*num_data_points, maxlen=num_data_points)
        self.channel1_series.append([qtc.QPointF(x,y) for x, y in enumerate(self.channel1_data)])
        
        self.channel1_chart.setAxisX(channel1_x_axis, self.channel1_series)
        self.channel1_chart.setAxisY(channel1_y_axis, self.channel1_series)

        channel2_x_axis = qtch.QValueAxis()
        channel2_x_axis.setRange(0, num_data_points)
        channel2_x_axis.setLabelsVisible(False)
        channel2_y_axis = qtch.QValueAxis()
        channel2_y_axis.setRange(-1e-5, 1e-5)
    
        channel2_gridColor = qtg.QColor('#696969')
        channel2_x_axis.setGridLineColor(channel2_gridColor)
        channel2_y_axis.setGridLineColor(channel2_gridColor)
        
        self.channel2_chart = qtch.QChart()
        self.channel2_chart.setMargins(qtc.QMargins(0,-25,0,0))
        self.channel2_chart.setTheme(qtch.QChart.ChartThemeLight)
        self.channel2_chart.setBackgroundVisible(False)
        self.channel2_chart.setBackgroundRoundness(0)
        self.channel2_chart.layout().setContentsMargins(0,0,0,0)
        
        self.parameters_sr830_channel2_display.setChart(self.channel2_chart)
        
        self.channel2_series = qtch.QLineSeries()
        self.channel2_chart.addSeries(self.channel2_series)
            
        self.channel2_data = deque([0]*num_data_points, maxlen=num_data_points)
        self.channel2_series.append([qtc.QPointF(x,y) for x, y in enumerate(self.channel2_data)])
        
        self.channel2_chart.setAxisX(channel2_x_axis, self.channel2_series)
        self.channel2_chart.setAxisY(channel2_y_axis, self.channel2_series)
        
        # chart.setRenderHint(qtg.QPainter.Antialiasing)

        self.timer=qtc.QTimer(interval=500, timeout=self.refresh_stats)
        # self.timer.timeout.connect(lambda: refresh_stats)
        self.timer.start()
        
    def refresh_stats(self):
        if self.parameters_sr830.isEnabled():
            channel1_y_axis = qtch.QValueAxis()
            channel1_axisBrush = qtg.QBrush(qtg.QColor('#ffffff'))
            channel1_y_axis.setLabelsBrush(channel1_axisBrush)
            channel1_gridColor = qtg.QColor('#696969')
            # x_axis.setGridLineColor(gridColor)
            channel1_y_axis.setGridLineColor(channel1_gridColor)

            if self.sr830.channel1 == [0.0, 0.0]:
                self.channel1_data.append(self.sr830.x)
                
                if self.sr830.input_config in ['A','A - B']:
                    channel1_y_axis.setRange(-self.sr830.sensitivity, self.sr830.sensitivity)
                elif self.sr830.input_config in ['I (1 MOhm)', 'I (100 MOhm)']:
                    channel1_y_axis.setRange(-self.sr830.sensitivity/1e6, self.sr830.sensitivity/1e6)
                    
            elif self.sr830.channel1 == [1.0, 0.0]:
                self.channel1_data.append(self.sr830.magnitude)
                
                if self.sr830.input_config in ['A','A - B']:
                    # channel1_y_axis.setRange(-self.sr830.sensitivity, self.sr830.sensitivity)
                    channel1_y_axis.setRange(0, np.sqrt(2)*self.sr830.sensitivity)
                elif self.sr830.input_config in ['I (1 MOhm)', 'I (100 MOhm)']:
                    channel1_y_axis.setRange(0, np.sqrt(2)*self.sr830.sensitivity/1e6)
                
            channel1_new_data = [qtc.QPointF(x, y) for x, y in enumerate(self.channel1_data)]
            self.channel1_series.replace(channel1_new_data)
            
            self.channel1_chart.setAxisY(channel1_y_axis, self.channel1_series)

            channel2_y_axis = qtch.QValueAxis()
            channel2_axisBrush = qtg.QBrush(qtg.QColor('#ffffff'))
            channel2_y_axis.setLabelsBrush(channel2_axisBrush)
            channel2_gridColor = qtg.QColor('#696969')
            # x_axis.setGridLineColor(gridColor)
            channel2_y_axis.setGridLineColor(channel2_gridColor)
            
            if self.sr830.channel2 == [0.0, 0.0]:
                self.channel2_data.append(self.sr830.y)
                
                if self.sr830.input_config in ['A','A - B']:
                    channel2_y_axis.setRange(-self.sr830.sensitivity, self.sr830.sensitivity)
                elif self.sr830.input_config in ['I (1 MOhm)', 'I (100 MOhm)']:
                    channel2_y_axis.setRange(-self.sr830.sensitivity/1e6, self.sr830.sensitivity/1e6)
                    
            elif self.sr830.channel2 == [1.0, 0.0]:
                self.channel2_data.append(self.sr830.theta)
                # y_axis.setRange(-self.sr830.sensitivity, self.sr830.sensitivity) 
                channel2_y_axis.setRange(-180,180) 

            channel2_new_data = [qtc.QPointF(x, y) for x, y in enumerate(self.channel2_data)]
            self.channel2_series.replace(channel2_new_data)
                
            self.channel2_chart.setAxisY(channel2_y_axis, self.channel2_series)
    
            
    def pm100d_chart_setup(self):
        num_data_points = 80
    
        x_axis = qtch.QValueAxis()
        x_axis.setRange(0, num_data_points)
        x_axis.setLabelsVisible(False)
        y_axis = qtch.QValueAxis()
        y_axis.setRange(0, 1e-3)
    
        gridColor = qtg.QColor('#696969')
        x_axis.setGridLineColor(gridColor)
        y_axis.setGridLineColor(gridColor)
        
        self.pm100d_trace_display_chart = qtch.QChart()
        self.pm100d_trace_display_chart.setMargins(qtc.QMargins(0,-25,0,0))
        self.pm100d_trace_display_chart.setTheme(qtch.QChart.ChartThemeLight)
        self.pm100d_trace_display_chart.setBackgroundVisible(False)
        self.pm100d_trace_display_chart.setBackgroundRoundness(0)
        self.pm100d_trace_display_chart.layout().setContentsMargins(0,0,0,0)
        
        self.parameters_pm100d_trace_display.setChart(self.pm100d_trace_display_chart)

        self.pm100d_trace_display_series = qtch.QLineSeries()
        self.pm100d_trace_display_chart.addSeries(self.pm100d_trace_display_series)
            
        self.data = deque([0]*num_data_points, maxlen=num_data_points)
        self.pm100d_trace_display_series.append([qtc.QPointF(x,y) for x, y in enumerate(self.data)])
        
        self.pm100d_trace_display_chart.setAxisX(x_axis, self.pm100d_trace_display_series)
        self.pm100d_trace_display_chart.setAxisY(y_axis, self.pm100d_trace_display_series)
        
    def measure_chart_setup(self):
        num_data_points = 0
    
        x_axis = qtch.QValueAxis()
        x_axis.setRange(0, num_data_points)
        x_axis.setLabelsVisible(False)
        y_axis = qtch.QValueAxis()
        y_axis.setRange(0, 1)
    
        gridColor = qtg.QColor('#696969')
        x_axis.setGridLineColor(gridColor)
        y_axis.setGridLineColor(gridColor)
        
        self.measure_display_chart = qtch.QChart()
        self.measure_display_chart.setMargins(qtc.QMargins(0,0,0,0))
        self.measure_display_chart.setTheme(qtch.QChart.ChartThemeLight)
        self.measure_display_chart.setBackgroundVisible(False)
        self.measure_display_chart.setBackgroundRoundness(0)
        self.measure_display_chart.layout().setContentsMargins(0,0,0,0)
        
        self.plots_x.setChart(self.measure_display_chart)

        self.measure_display_series = qtch.QScatterSeries()
        self.measure_display_chart.addSeries(self.measure_display_series)
            
        self.measure_data = deque([0]*num_data_points, maxlen=num_data_points)
        self.measure_display_series.append([qtc.QPointF(x,y) for x, y in enumerate(self.measure_data)])
        
        self.measure_display_chart.setAxisX(x_axis, self.measure_display_series)
        self.measure_display_chart.setAxisY(y_axis, self.measure_display_series)

        num_data_points = 0
    
        x_axis = qtch.QValueAxis()
        x_axis.setRange(0, num_data_points)
        x_axis.setLabelsVisible(False)
        y_axis = qtch.QValueAxis()
        y_axis.setRange(0, 1)
    
        gridColor = qtg.QColor('#696969')
        x_axis.setGridLineColor(gridColor)
        y_axis.setGridLineColor(gridColor)
        
        self.theta_display_chart = qtch.QChart()
        self.theta_display_chart.setMargins(qtc.QMargins(0,0,0,0))
        self.theta_display_chart.setTheme(qtch.QChart.ChartThemeLight)
        self.theta_display_chart.setBackgroundVisible(False)
        self.theta_display_chart.setBackgroundRoundness(0)
        self.theta_display_chart.layout().setContentsMargins(0,0,0,0)
        
        self.plots_theta.setChart(self.theta_display_chart)

        self.theta_display_series = qtch.QScatterSeries()
        self.theta_display_chart.addSeries(self.theta_display_series)
            
        self.theta_data = deque([0]*num_data_points, maxlen=num_data_points)
        self.theta_display_series.append([qtc.QPointF(x,y) for x, y in enumerate(self.theta_data)])
        
        self.theta_display_chart.setAxisX(x_axis, self.theta_display_series)
        self.theta_display_chart.setAxisY(y_axis, self.theta_display_series)
        
    def run(self,run_action,parameters_sr830=[],parameters_galvo=[]):
        if run_action.isChecked() == True:
            
            if (self.parameters_sr830.isEnabled() and self.parameters_lltf.isEnabled() and self.parameters_pm100d.isEnabled()):
                self.measure = measure.measure()
                self.measure_thread = qtc.QThread()
                self.measure.moveToThread(self.measure_thread)
                self.measure.measure_finished.connect(self.measure_thread.quit)

                # # self.measure.set_lltf(self.lltf)


                self.measure_thread.start()
                self.measure_thread.started.connect(self.measure.run)
                self.measure.set_sr830(self.sr830)
                self.measure.set_pm100d(self.pm100d)
                self.measure.set_x_chart(self.measure_display_chart)
                self.measure.set_plots_theta(self.plots_theta)
                
                # self.mapper.set_sr830(self.sr830)
                # self.mapper.set_parameters_galvo(self.parameters_galvo)
                # self.mapper_thread.started.connect(self.mapper.do_mapping)
                # self.mapper.mapping_started.connect(lambda: self.log_box.append('[MEASUREMENT] Starting...'))
                # self.mapper.mapping_finished.connect(lambda: self.log_box.append('<span style="color:palegreen">[MEASUREMENT] Complete</span>'))
                # self.mapper.mapping_moved.connect(self.refresh_plots)
                
                self.measure.measure_finished.connect(lambda: run_action.setChecked(False))     
                print('hi')
                
            else:
                self.log_box.append('<span style="color:lightcoral">[ERROR] SR830 not connected<\span>')
                run_action.setChecked(False)
             
        else:
            pass


# class test(MainWindow):
#     def __init__(self):
#         print('hi')
            



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    mv = MainWindow()
    sys.exit(app.exec())
