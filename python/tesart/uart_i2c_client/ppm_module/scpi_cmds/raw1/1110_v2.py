from tkinter import *
from visa_control import *


## Constants
step_descriptions = [
    'Ожидание подключения к прибору',
    'Настройка векторного анализатора цепей',
    'Калибровка источника мощности (порт 1)',
    'Калибровка источника мощности (порт 3)',
    'Измерение амплитуды напряжения на выходе ПЧ1', 
    'Измерение амплитуды напряжения на выходе ПЧ2'
]


## Variables
visa_instr_address = 'TCPIP0::192.168.0.101::inst0::INSTR'

visa_sens_type = 'USB'
visa_sens_address = 'Keysight Technologies,U2002H,MY51500003'

calkit = 'N4691-60006 ECal 08195'

port1_dut_conn = 'APC 3.5 female'
port2_dut_conn = 'APC 3.5 female'

power_meter_conn = 'APC 3.5 male'

input_freq_start = 8e9
input_freq_stop = 12e9

lo_freq = 10e6

output_freq_start = input_freq_start + lo_freq
output_freq_stop = input_freq_stop + lo_freq

port1_power_level = -20
port1_power_offset = 0
port1_att = 0

port2_power_level = -45
port2_att = 20.0

port3_power_level = -30

points = 101
rbw = 1e3


## Additional functions
def inc_state():
    global cur_state, max_state
    cur_state += 1
    if cur_state > max_state:
        cur_state = max_state
    change_state()


def dec_state():
    global cur_state
    cur_state -= 1
    if cur_state < 2:
        cur_state = 2
    change_state()


def stop_program():
    global instr
    disconnect2instr()
    root.destroy()


## Main functions
# Function for connection to instrument (step 1)
def connection():
    step_label.config(text=step_descriptions[0])
    
    connect2instr(visa_instr_address)
    
    step_label.config(text='Соединение установлено. Для продолжения нажмите \"Далее\"')
    next_button.config(state=NORMAL)


# Function for configuring instrument (step 2)
# Функция ниже относится к пункту 1.1.10.4 методики
def instr_configuring():
    step_label.config(text=step_descriptions[1])

    prev_button.config(state=DISABLED)
    next_button.config(state=DISABLED)
    
    send2instr(':SYSTem:FPReset')
    send2instr(':DISPlay:WINDow:STATe %d' % (1))
    send2instr(':CALCulate:CUSTom:DEFine "%s","%s","%s"' % ('Standard meas', 'Standard', 'B_1'))
    send2instr(':DISPlay:WINDow:TRACe:FEED "%s"' % ('Standard meas'))
    
    send2instr(':SENSe:SWEep:TYPE %s' % ('LINear'))
    send2instr(':SENSe:SWEep:POINts %d' % (201))
    send2instr(':SENSe:FREQuency:STARt %G' % (8000000000.0))
    send2instr(':SENSe:FREQuency:STOP %G' % (12000000000.0))
    send2instr(':SENSe:BWIDth:RESolution %G' % (1000.0))
    
    send2instr(':SOURce:POWer1:COUPle %d' % (0))
    send2instr(':SOURce:POWer2:COUPle %d' % (0))
    
    send2instr(':SOURce:POWer1:MODE %s' % ('ON'))
    send2instr(':SOURce:POWer1:ATTenuation:AUTO %d' % (0))
    send2instr(':SOURce:POWer1:ATTenuation %G' % (port1_att))
    send2instr(':SOURce:POWer1:LEVel:IMMediate:AMPLitude %G' % (port1_power_level))
    send2instr(':SOURce:POWer1:ALC:MODE:RECeiver:STATe %d,"%s"' % (1, 'Port 1'))
    send2instr(':SOURce:POWer1:ALC:MODE:RECeiver:OFFSet %G' % (port1_power_offset))
   
    send2instr(':SOURce:POWer3:LEVel:IMMediate:AMPLitude %G' % (port3_power_level))
    send2instr(':SOURce:POWer3:ALC:MODE:RECeiver:STATe %d,"%s"' % (1, 'Port 3'))
    send2instr(':SOURce:POWer3:ALC:MODE:RECeiver:OFFSet %G' % (0))
    
    send2instr(':SENSe:FOM:STATe %d' % (1))
    send2instr(':SENSe:FOM:RANGe3:FREQuency:OFFSet %G' % (-10000000.0))
    send2instr(':SENSe:FOM:RANGe4:COUPled %d' % (0))
    send2instr(':SENSe:FOM:RANGe4:SWEep:TYPE %s' % ('CW'))
    send2instr(':SENSe:FOM:RANGe4:FREQuency:CW %G' % (10000000.0))
    send2instr(':SENSe:FOM:DISPlay:SELect "%s"' % ('Receivers'))
    
    step_label.config(justify=LEFT, text="Настройка ВАЦ прошла успешно.\nПодключите измеритель мощности к первому порту и нажмите \"Далее\"")
    
    next_button.config(state=NORMAL)


# Function for configuring power sensor and calibrating power source (step 3)
# Функция ниже относится к пункту 1.1.10.5 методики
def power_sens_configuring(port):
    if port == 'Port 1':
        step_label.config(text=step_descriptions[2])
    else:
        step_label.config(text=step_descriptions[3])

    prev_button.config(state=NORMAL)
    result1_label.place_forget()
    
    send2instr(":SYSTem:COMMunicate:PSENsor " + visa_sens_type + ", '" + visa_sens_address + "'")
    query2instr(":SYSTem:COMMunicate:PSENsor?")

    if port == 'Port 1':
        send2instr(":SOURce:POWer:CORRection:COLLect:ITERation:NTOLerance 0.1")
    else:
        send2instr(":SOURce:POWer:CORRection:COLLect:ITERation:NTOLerance 1")
        
    send2instr(":SOURce:POWer:CORRection:COLLect:ITERation:COUNt 55")
    send2instr(":SOURce:POWer:CORRection:OFFSet:MAGNitude 10")
    send2instr(":SOURce:POWer:CORRection:COLLect:DISPlay:STATe 1")
    justsend2instr(':SOURce:POWer:CORRection:COLLect:ACQuire %s,"%s","%s"; *OPC' % ('PMETer', 'ASENSOR', port))

    wait()

    if port == 'Port 3':
        justsend2instr(":SOURce:POWer:CORRection:COLLect:SAVE RRECeiver")

    if port == 'Port 1':
        step_label.config(justify=LEFT, text="Калибровка прошла успешно.\nПодключите измеритель мощности к третьему порту и нажмите \"Далее\"")
    else:
        step_label.config(justify=LEFT, text="Калибровка прошла успешно.\nПодключите выход исследуемого устройства (ПЧ1) и нажмите \"Далее\"")


# Функция ниже относится к пункту 1.1.10.9 методики
def first_measure():
    step_label.config(text=step_descriptions[4])
    
    next_button.config(text = "Далее", width = 10, command = inc_state)
    result2_label.place_forget()
    
    send2instr("DISPLAY:WINDOW1:TRACE1:SELECT")
    send2instr(':CALCulate:MEASURE:MARKer1:STATe %d' % (1))
    send2instr(':CALCulate:MEASURE:MARKer1:FUNCtion:TRACking %d' % (1))
    send2instr(':CALCulate:MEASURE:MARKer1:FUNCtion:SELect %s' % ('MINimum'))
    send2instr(':CALCulate:MEASURE:MARKer1:FUNCtion:DOMain:USER:STARt %G' % (8010000000.0))
    send2instr(':CALCulate:MEASURE:MARKer1:FUNCtion:DOMain:USER:STOP %G' % (12010000000.0))

    result = query2instr(':CALCulate:MEASURE:MARKer1:Y?')
    result1_label.config(text='Амплитуда напряжения на выходе ПЧ1: %s В' % (result))
    result1_label.place(x=10, y=60)

    step_label.config(justify=LEFT, text="Измерение на выходе ПЧ1 прошло успешно.\nПодключите выход исследуемого устройства (ПЧ2) и нажмите \"Далее\"")


# Функция ниже относится к пункту 1.1.10.10 методики
def second_measure():
    step_label.config(text=step_descriptions[5])
    
    send2instr(':CALCulate:MEASURE:MARKer1:STATe %d' % (1))
    send2instr(':CALCulate:MEASURE:MARKer1:FUNCtion:TRACking %d' % (1))
    send2instr(':CALCulate:MEASURE:MARKer1:FUNCtion:SELect %s' % ('MINimum'))
    send2instr(':CALCulate:MEASURE:MARKer1:FUNCtion:DOMain:USER:STARt %G' % (8010000000.0))
    send2instr(':CALCulate:MEASURE:MARKer1:FUNCtion:DOMain:USER:STOP %G' % (12010000000.0))

    result = query2instr(':CALCulate:MEASURE:MARKer1:Y?')
    result2_label.config(text='Амплитуда напряжения на выходе ПЧ2: %s В' % (result))
    result2_label.place(x=10, y=80)

    step_label.config(justify=LEFT, text="Измерение на выходе ПЧ2 прошло успешно.")

    next_button.config(text="Закончить", command=stop_program)
    next_button.place(x=400,y=260)

    prev_button.place_forget()
    close_button.place_forget()


def change_state():
    print('\n')
    global cur_state, max_state
    
    if cur_state == 1:
        connection()
    elif cur_state == 2:
        instr_configuring()
    elif cur_state == 3:
        power_sens_configuring('Port 1')
    elif cur_state == 4:
        power_sens_configuring('Port 3')
    elif cur_state == 5:
        first_measure()
    elif cur_state == max_state:
        second_measure()


## Main
cur_state = 1
max_state = len(step_descriptions)

root = Tk()
root.geometry("500x300")
root.title("Измерение амплитуды напряжения на выходах ПЧ1 ПЧ2")

# Result UI elements
result1_label = Label(root)
result2_label = Label(root)

# Main UI elements
step_label = Label(root)
step_label.place(x=10, y=10)

prev_button = Button(root, text = "Назад", width = 10, command = dec_state)
prev_button.place(x=200,y=260)

next_button = Button(root, text = "Далее", width = 10, command = inc_state)
next_button.place(x=280,y=260)

close_button = Button(root, text = "Отмена", width = 10, command = stop_program)
close_button.place(x=400,y=260)

prev_button.config(state=DISABLED)
next_button.config(state=DISABLED)

change_state()

root.mainloop()
