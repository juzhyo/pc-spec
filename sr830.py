# -*- coding: utf-8 -*-

############################
# THE ONE-MAN ARMY KNIFE   #
# AUTHOR: JUSTIN ZHOU YONG #
############################

from pymeasure.instruments.srs import SR830

def connect(self, resource_name):
    try:
        SR830(resource_name).id
        self.parameters_sr830.setEnabled(True)
        self.parameters_sr830_input_coupling_ac.setEnabled(True)
        self.sr830 = SR830(resource_name)
        
        sr830_parameters = read_parameters(self)
        
        # print(sr830_parameters.get('sensitivity'))
        
        # self.parameters_sr830_time_constant.setCurrentIndex(10)
        
        set_parameters(self,initialize=True)	

        # self.parameters_sr830_time_constant.setItemText("asdf")        
                
    except:
        self.log_box.append('<span style="color:lightcoral">[ERROR] SR830 connection failed<\span>')
        self.parameters_sr830.setDisabled(True)
        return
            
    self.log_box.append('<span style="color:palegreen">[SUCCESS] SR830 connected</span>')
    
    return SR830(resource_name)

def read_parameters(self):
    ### Returns parameters displayed on the SR830
    
    time_constant = [30000,10000,3000,1000,300,100,30,10,3,1,0.3,0.1,0.03,0.01,0.003,0.001,0.0003,0.0001,0.00003,0.00001]
    filter_slope = [24,16,12,6]
    input_config = ['A','A - B','I (1 MOhm)', 'I (100 MOhm)']
    input_coupling = ['AC','DC']
    input_grounding = ['Float','Ground']
    input_notch_config = ['None', 'Line', '2 x Line', 'Both']
    # if input_config[self.parameters_sr830_input_config.currentIndex()] in ['A','A - B']:
    #     sensitivity = [1,5e-1,2e-1,1e-1,5e-2,2e-2,1e-2,5e-3,2e-3,1e-3,5e-4,2e-4,1e-4,5e-5,2e-5,1e-5,5e-6,2e-6,1e-6,5e-7,2e-7,1e-7,5e-8,2e-8,1e-8,5e-9,2e-9,1e-9]
    # elif input_config[self.parameters_sr830_input_config.currentIndex()] in ['I (1 MOhm)', 'I (100 MOhm)']:
    #     sensitivity = [1e-6,5e-7,2e-7,1e-7,5e-8,2e-8,1e-8,5e-9,2e-9,1e-9,5e-10,2e-10,1e-10,5e-11,2e-11,1e-11,5e-12,2e-12,1e-12,5e-13,2e-13,1e-13,5e-14,2e-14,1e-14,5e-15,2e-15]
    sensitivity = [1,5e-1,2e-1,1e-1,5e-2,2e-2,1e-2,5e-3,2e-3,1e-3,5e-4,2e-4,1e-4,5e-5,2e-5,1e-5,5e-6,2e-6,1e-6,5e-7,2e-7,1e-7,5e-8,2e-8,1e-8,5e-9,2e-9,1e-9]
    channel1 = ['X', 'R', 'X Noise', 'Aux In 1', 'Aux In 2']
    channel2 = ['Y', 'Theta', 'Y Noise', 'Aux In 3', 'Aux In 4'] 
    
    return {'time_constant':time_constant.index(self.sr830.time_constant),
            'filter_slope':filter_slope.index(self.sr830.filter_slope),
            'input_config':input_config.index(self.sr830.input_config),
            'frequency':self.sr830.frequency,
            'input_coupling':input_coupling.index(self.sr830.input_coupling),
            'input_grounding':input_grounding.index(self.sr830.input_grounding),
            'sensitivity':sensitivity.index(self.sr830.sensitivity),
            'channel1':int(self.sr830.channel1[0]),
            'channel2':int(self.sr830.channel2[0])}

def get_parameters(self):
    time_constant = [30000,10000,3000,1000,300,100,30,10,3,1,0.3,0.1,0.03,0.01,0.003,0.001,0.0003,0.0001,0.00003,0.00001]
    filter_slope = [24,16,12,6]
    input_config = ['A','A - B','I (1 MOhm)', 'I (100 MOhm)']
    input_coupling = ['AC','DC']
    input_grounding = ['Float','Ground']
    input_notch_config = ['None', 'Line', '2 x Line', 'Both']
    # if input_config[self.parameters_sr830_input_config.currentIndex()] in ['A','A - B']:
    #     sensitivity = [1,5e-1,2e-1,1e-1,5e-2,2e-2,1e-2,5e-3,2e-3,1e-3,5e-4,2e-4,1e-4,5e-5,2e-5,1e-5,5e-6,2e-6,1e-6,5e-7,2e-7,1e-7,5e-8,2e-8,1e-8,5e-9,2e-9,1e-9]
    # elif input_config[self.parameters_sr830_input_config.currentIndex()] in ['I (1 MOhm)', 'I (100 MOhm)']:
    #     sensitivity = [1e-6,5e-7,2e-7,1e-7,5e-8,2e-8,1e-8,5e-9,2e-9,1e-9,5e-10,2e-10,1e-10,5e-11,2e-11,1e-11,5e-12,2e-12,1e-12,5e-13,2e-13,1e-13,5e-14,2e-14,1e-14,5e-15,2e-15]
    sensitivity = [1,5e-1,2e-1,1e-1,5e-2,2e-2,1e-2,5e-3,2e-3,1e-3,5e-4,2e-4,1e-4,5e-5,2e-5,1e-5,5e-6,2e-6,1e-6,5e-7,2e-7,1e-7,5e-8,2e-8,1e-8,5e-9,2e-9,1e-9]
    channel1 = ['X', 'R', 'X Noise', 'Aux In 1', 'Aux In 2']
    channel2 = ['Y', 'Theta', 'Y Noise', 'Aux In 3', 'Aux In 4']                
        
    return {'time_constant':time_constant[self.parameters_sr830_time_constant.currentIndex()],
            'filter_slope':filter_slope[self.parameters_sr830_filter_slope.currentIndex()],
            'input_config':input_config[self.parameters_sr830_input_config.currentIndex()],
            'frequency':self.parameters_sr830_frequency,
            'input_coupling':input_coupling[self.parameters_sr830_input_coupling_dc.isChecked()],
            'input_grounding':input_grounding[self.parameters_sr830_input_grounding_ground.isChecked()],
            'sensitivity':sensitivity[self.parameters_sr830_sensitivity.currentIndex()],
            'channel1':channel1[self.parameters_sr830_channel1.currentIndex()],
            'channel2':channel2[self.parameters_sr830_channel2.currentIndex()]}

def set_parameters(self,parameter='all',initialize=False):
    if initialize:
        set_parameters_list = read_parameters(self)
    else:
        set_parameters_list = get_parameters(self)
            
    if parameter=='all':     
        parameter_names = ['time_constant',
                            'filter_slope',
                            'input_config',
                            'frequency',
                            'input_coupling',
                            'input_grounding',
                            'sensitivity',
                            'channel1',
                            'channel2']
            
        for i in range(len(set_parameters_list)):
            parameter_name = parameter_names[i]

            if parameter_name == 'frequency':
                self.parameters_sr830_frequency = set_parameters_list['frequency']
            elif parameter_name == 'input_coupling':
                if set_parameters_list['input_coupling'] == 0:
                    self.parameters_sr830_input_coupling_ac.setChecked(True)
                    self.parameters_sr830_input_coupling_ac.setChecked(False)
                else:
                    self.parameters_sr830_input_coupling_ac.setChecked(False)
                    self.parameters_sr830_input_coupling_ac.setChecked(True)
            elif parameter_name == 'input_grounding':
                if set_parameters_list['input_grounding'] == 0:
                    self.parameters_sr830_input_grounding_float.setChecked(True)
                    self.parameters_sr830_input_grounding_ground.setChecked(False)
                else:
                    self.parameters_sr830_input_grounding_float.setChecked(False)
                    self.parameters_sr830_input_grounding_ground.setChecked(True)
            else:
                exec('self.parameters_sr830_' + parameter_name + '.setCurrentIndex(' + str(set_parameters_list[parameter_name]) + ')')
            
    else:
        parameter_name = parameter
        
        if isinstance(set_parameters_list[parameter_name],str) == True:
            exec('self.sr830.' + parameter_name + '= "' + set_parameters_list[parameter_name] + '"')
        else:
            exec('self.sr830.' + parameter_name + '=' + str(set_parameters_list[parameter_name]))
                
    return