from tkinter import *
from visa_control import *


## Constants
step_descriptions = [
    'Ожидание подключения к прибору',
    'Настройка векторного анализатора цепей',
    'Калибровка источника мощности',
    'Калибровка векторного анализатора цепей',
    'Измерение'
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

center_freq = 10e9
span = 2e9

output_freq_start = input_freq_start + lo_freq
output_freq_stop = input_freq_stop + lo_freq

port1_power_level = -44
port1_att = 20.0

port2_power_level = -40
port2_att = 20.0

port3_power_level = -40

points = 51
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
# Весь скрипт относится к пункту 1.1.9.3 методики
# Функция ниже относится к пункту 1.1.8.3 методики
def instr_configuring():
    step_label.config(text=step_descriptions[1])
    
    prev_button.config(state=DISABLED)
    next_button.config(state=DISABLED)
    
    send2instr(':SYSTem:FPReset')
    send2instr(':DISPlay:WINDow1:STATe %d' % (1))
    send2instr(':CALCulate:PARameter:DELete:ALL')

    send2instr(':CALCulate1:CUSTom:DEFine "%s","%s","%s"' % ('CompIn21', 'Gain Compression Converters', 'CompIn21'))
    send2instr(':CALCulate1:CUSTom:DEFine "%s","%s","%s"' % ('CompOut21', 'Gain Compression Converters', 'CompOut21'))

    send2instr(':DISPlay:WINDow1:TRACe1:FEED "%s"' % ('CompIn21'))
    send2instr(':DISPlay:WINDow1:TRACe2:FEED "%s"' % ('CompOut21'))
    
    send2instr(':CALCulate1:MEASure1:FORMat %s' % ('MLOG'))
    send2instr(':CALCulate1:MEASure2:FORMat %s' % ('MLOG'))

    send2instr(':SOURce:POWer1:COUPle %d' % (0))
    send2instr(':SOURce:POWer2:COUPle %d' % (0))
    
    send2instr(':SOURce:POWer1:ATTenuation:AUTO %d' % (0))
    send2instr(':SOURce:POWer1:ATTenuation %G' % (port1_att))
    send2instr(':SOURce:POWer1:LEVel:IMMediate:AMPLitude %G' % (port1_power_level))
    
    send2instr(':SOURce:POWer2:ATTenuation:AUTO %d' % (0))
    send2instr(':SOURce:POWer2:ATTenuation %G' % (port2_att))
    send2instr(':SOURce:POWer2:LEVel:IMMediate:AMPLitude %G' % (port2_power_level))
    
    send2instr(':SOURce:POWer3:LEVel:IMMediate:AMPLitude %G' % (port3_power_level))
    send2instr(':SOURce:POWer3:ALC:MODE:RECeiver:STATe %d,"%s"' % (1, 'Port 3'))
    send2instr(':SOURce:POWer3:ALC:MODE:RECeiver:OFFSet %G' % (0.1))

    send2instr(':SENSe:MIXer:LO1:FREQuency:FIXed %G' % (lo_freq))
    send2instr(':SENSe:MIXer:LO1:NAME "%s"' % ('Port 3'))
    
    send2instr(':SENSe:SWEep:TYPE %s' % ('LINear'))
    send2instr(':SENSe:GCSetup:AMODe %s' % ('SMARtsweep'))
    send2instr(':SENSe:SWEep:POINts %d' % (points))
    
    send2instr(':SENSe:BWIDth:RESolution %G' % (rbw))
    
    send2instr(':SENSe:MIXer:INPut:FREQuency:STARt %G' % (input_freq_start))
    send2instr(':SENSe:MIXer:INPut:FREQuency:STOP %G' % (input_freq_stop))
    send2instr(':SENSe:MIXer:OUTPut:FREQuency:SIDeband %s' % ('HIGH'))
    send2instr(':SENSe:MIXer:OUTPut:FREQuency:STARt %G' % (output_freq_start))
    send2instr(':SENSe:MIXer:OUTPut:FREQuency:STOP %G' % (output_freq_stop))
    send2instr(':SENSe:MIXer:APPLy')
    
    step_label.config(justify=LEFT, text="Настройка ВАЦ прошла успешно.\nПодключите измеритель мощности к третьему порту и нажмите \"Далее\"")
    
    next_button.config(state=NORMAL)


# Function for configuring power sensor and calibrating power source (step 3)
# Функция ниже относится к пункту 1.1.8.4 методики
def power_sens_configuring():
    step_label.config(text=step_descriptions[2])

    prev_button.config(state=NORMAL)
    result_label.place_forget()
    
    send2instr(":SYSTem:COMMunicate:PSENsor " + visa_sens_type + ", '" + visa_sens_address + "'")
    query2instr(":SYSTem:COMMunicate:PSENsor?")

    send2instr(":SOURce:POWer:CORRection:COLLect:ITERation:NTOLerance 0.05")
    send2instr(":SOURce:POWer:CORRection:COLLect:ITERation:COUNt 255")
    send2instr(":SOURce:POWer:CORRection:OFFSet:MAGNitude 0")
    send2instr(":SOURce:POWer:CORRection:COLLect:DISPlay:STATe 1")
    justsend2instr(':SOURce:POWer:CORRection:COLLect:ACQuire %s,"%s","%s"; *OPC' % ('PMETer', 'ASENSOR', 'Port 3'))

    wait()

    justsend2instr(":SOURce:POWer:CORRection:COLLect:SAVE RRECeiver")

    step_label.config(justify=LEFT, text="Калибровка прошла успешно.")


# Function for configuring smart calibration (step 4)
# Функция ниже относится к пункту 1.1.8.5 методики
def smart_cal_configuring():
    global max_state, max_cal_step
    
    step_label.config(text=step_descriptions[3])

    send2instr(":SENSe:CORRection:COLLect:GUIDed:CONNector:PORT1:SELect '" + port1_dut_conn + "'")
    send2instr(":SENSe:CORRection:COLLect:GUIDed:CONNector:PORT2:SELect '" + port2_dut_conn + "'")
    send2instr(":SENSe:CORRection:COLLect:GUIDed:CKIT:PORT1:SELect '" + calkit + "'")
    send2instr(":SENSe:CORRection:COLLect:GUIDed:CKIT:PORT2:SELect '" + calkit + "'")
    send2instr(":SENSe:CORRection:COLLect:GUIDed:INITiate:IMMediate")

    max_cal_step = query2instr(":SENSe:CORRection:COLLect:GUIDed:STEPs?")
    max_cal_step = 4
    max_state = len(step_descriptions) + max_cal_step
    step_label.config(justify=LEFT, text="Конфигурация калибровки прошла успешно. Нажмите \"Далее\"")


# Function for changing steps in smart calibration
# Функция ниже относится к пункту 1.1.8.5 методики
def cal_steps():
    step_label.config(text="Шаг %d из %d" % (cur_state-4, max_state-len(step_descriptions)))

    meas_button.place(x=280,y=260)
    next_button.place_forget()
    
    cal_label.place(x=10, y=60)
    cal_label.config(text=query2instr("SENS:CORR:COLL:GUID:DESC? " + str(cur_state-4)))

    meas_button.config(state=NORMAL)
    prev_button.config(state=NORMAL)
    next_button.config(state=DISABLED)


# Function for measure in smart cal step
# Функция ниже относится к пункту 1.1.8.5 методики
def meas():
    global instr, cur_state
    
    justsend2instr("SENS:CORR:COLL:GUID:ACQ STAN" + str(cur_state-4) + ",SYNC; *OPC")

    wait()

    meas_button.place_forget()
    next_button.place(x=280,y=260)
    meas_button.config(state=DISABLED)
    prev_button.config(state=NORMAL)
    next_button.config(state=NORMAL)

    if (cur_state-4 == max_cal_step):
        justsend2instr("SENSe:CORRection:COLLect:GUIDed:SAVE:IMMediate 1")
        justsend2instr("DISPLAY:WINDOW2:STATE OFF")
        step_label.config(justify=LEFT, text="Калибровка прошла успешно.")
        cal_label.place_forget()


# Функция ниже относится к пункту 1.1.8.10 методики
def marker_measure():
    step_label.config(text=step_descriptions[4])
    
    send2instr("DISPLAY:WINDOW1:TRACE1:SELECT")
    
    send2instr(':CALCulate:MARKer1:STATe %d' % (1))
    send2instr(':CALCulate:MARKer1:FUNCtion:TRACking %d' % (1))
    send2instr(':CALCulate:MARKer1:FUNCtion:SELect %s' % ('MINimum'))
    send2instr(':CALCulate:MARKer1:FUNCtion:DOMain:USER:STARt %G' % (8010000000.0))
    send2instr(':CALCulate:MARKer1:FUNCtion:DOMain:USER:STOP %G' % (12010000000.0))

    result = query2instr(':CALCulate:MARKer1:Y?')
    result_label.config(text='Минимальное значение точки компрессии: %s дБ' % (result))
    result_label.place(x=10, y=80)

    step_label.config(justify=LEFT, text="Измерение прошло успешно.")

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
        power_sens_configuring()
    elif cur_state == 4:
        smart_cal_configuring()
    elif cur_state == max_state:
        marker_measure()
    else:
        cal_steps()


## Main
cur_state = 1
max_state = len(step_descriptions)

root = Tk()
root.geometry("500x300")
root.title("Калибровка для измерения верхней границы линейности амплитудной характеристики приёмного тракта по входу")

# Calibration UI elements
cal_label = Label(root)
meas_button = Button(root, text = "Измерить", width = 10, command = meas)

# Result UI elements
result_label = Label(root)

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
