import visa
import time

# Общие настройки
VNA_VISA_address = 'TCPIP0::192.168.0.10::inst0::INSTR' # Адрес векторного анализатора цепей
VISA_address_SA = 'TCPIP0::192.168.0.103::hislip0::INSTR' # visa-адрес анализатора сигнала
points = 201
startFreq = 8000000000.0
stopFreq = 12000000000.0
brwFreq = 1000.0
power_att = 0.0
pwrLvl = 0
pwrAttCenter = -30.0
pwrLvlTest = 0
powerMeterAdd = 'USB0::0x2A8D::0x3218::MY51500003::0::INSTR'
CWfreq = 10000000000.0
CWpoints = 1
centerFreqSA= 1000000000.0
spanFreqSA=1000000.0
BDwRes=1000.0
pwrRefLvl=20.0
spurLvl=20.0
atten=30.0
SAstartFreq='8000000000,10100000000'
SAstopFreq='9900000000,12000000000'
SABdwRes='1000,1000'
THRpower='-60,-60'
LimPowerStart='-70,-70'
LimPowerStop='-70,-70'


class Pacifier:
    def write(self, cmd):
        print(cmd)
    
    def query(self, cmd):
        print(cmd)


instr = Pacifier()
SCPI_90x0_SA = Pacifier()


def connectVna(VISA_address):
    global instr, check_state, rm
    rm = visa.ResourceManager()
    instr = rm.open_resource(VISA_address)
    instr.timeot = 5000
    check_state = 1

def checkConnect():
    global check_state
    if check_state > 0:
        settingCalInstr()
    return instr.query(":SYSTem:ERRor?")

def settingCalInstr (): # настройка ВАЦ
    global power_att, points, startFreq, stopFreq, brwFreq, pwrLvl, pwrAttCenter, pwrLvlTest
    instr.write(':SYSTem:FPReset')
    instr.write(':DISPlay:WINDow1:STATe %d' % (1))
    instr.write(':CALCulate1:PARameter:DELete:ALL')
    instr.write(':CALCulate1:CUSTom:DEFine "%s","%s","%s"' % ('CH1_S21', 'Standard', 'S21'))# создание переменной с типом измерения standart
    instr.write(':CALCulate1:PARameter:SELect "%s"' % ('CH1_S21'))
    instr.write(':DISPlay:WINDow1:TRACe2:FEED "%s"' % ('CH1_S21'))# создание трассы и присвоение ей переменной CH1_S21
    instr.write(':SENSe1:SWEep:TYPE %s' % ('LINear')) #Задание типа перестройки по частоте
    instr.write(':SENSe1:SWEep:POINts %d' % (points)) #Колицество точек
    instr.write(':SENSe1:FREQuency:STARt %G' % (startFreq))  # Начало диапазона частот
    instr.write(':SENSe1:FREQuency:STOP %G' % (stopFreq)) #Конец диапазона частот
    instr.write(':SENSe1:BWIDth:RESolution %G' % (brwFreq)) #разрешение по ширине полосы
    instr.write(':OUTPut:STATe %d' % (0)) # отключение канала измерения
    instr.write(':SOURce1:POWer1:COUPle %d' % (pwrLvlTest)) #уровень мощности тестовых портов
    instr.write(':SOURce1:POWer1:MODE %s' % ('ON')) #ослабление источника первого измерительног порта: вкл.
    instr.write(':SOURce1:POWer1:ATTenuation:AUTO %d' % (0)) #авторегулировка ослабления: откл.
    instr.write(':SOURce1:POWer1:ATTenuation %G' % (power_att)) #величина ослабления источника
    instr.write(':SOURce1:POWer1:CENTer %G' % (pwrAttCenter))
    instr.write(':SOURce1:POWer1:LEVel:IMMediate:AMPLitude %G' % (pwrLvl)) #уровень мощности на выходе ВАЦ
    instr.write(':SOURce1:POWer1:ALC:MODE:RECeiver:STATe %d' % (1)) #использование опорного приемника Receiver-R1
    instr.write(':SOURce1:POWer1:ALC:MODE:RECeiver:OFFSet %G' % (0.0)) #смещение по частоте
    instr.write(':SENSe1:SWEep:MODE %s' % ('SINGle'))
    instr.write(':OUTPut:STATe %d' % (1))
    instr.write(':SENSe1:CORRection:PREFerence:CSET:SAVE %s' % ('CALRegister')) #калибровка с использованием опорного приемника

def calInstr(): # Калибровка ВАЦ
    global powerMeterAdd
    instr.write(':SOURce:POWer:CORRection:COLLect:ITERation:NTOLerance %G' % (0.05))
    instr.write(':SYSTem:CONFigure:EDEVice:ADD "%s"' % ('power_receiver')) #имя устройства
    instr.write(':SYSTem:CONFigure:EDEVice:DTYPe "%s","%s"' % ('power_receiver', 'Power Meter')) #тип устройства
    instr.write(':SYSTem:COMMunicate:PSENsor %s,"%s"' % ('USB', 'Keysight Technologies,U2002H,MY51500003'))
    instr.write(':SYSTem:CONFigure:EDEVice:IOConfig "%s","%s"' % ('power_receiver', powerMeterAdd)) #visa-адрес измерителя мощности
    instr.write(':SYSTem:CONFigure:EDEVice:IOENable "%s",%d' % ('power_receiver', 1))
    instr.write(':SOURce1:POWer1:CORRection:COLLect:ACQuire %s,"%s"' % ('PMETer', 'ASENSOR')) #начало калебровки
    instr.timeot = 10000
    instr.write(':CALCulate2:CUSTom:DEFine "%s","%s","%s"' % ('CH1_R1', 'Standard', 'R_1'))
    instr.write(':DISPlay:WINDow1:TRACe3:FEED "%s"' % ('CH1_R1'))
    instr.write(':CALCulate2:PARameter:SELect "%s"' % ('CH1_R1'))

def postCalInstrSet():
    global CWfreq, CWpoints
    instr.write(':DISPlay:ANNotation:MESSage:STATe %d' % (0))
    instr.write(':SENSe1:FREQuency:CW %G' % (CWfreq))
    instr.write('*CLS')
    instr.write(':DISPlay:ANNotation:MESSage:STATe %d' % (1))
    instr.write(':SENSe1:SWEep:TYPE %s' % ('CW'))
    instr.write(':SENSe1:SWEep:POINts %d' % (CWpoints))
    instr.write(':SOURce1:POWer1:LEVel:IMMediate:AMPLitude %G' % (0.0))

def connectSA(VISA_address_SA):
    global SCPI_90x0_SA, check_state_SA
    rm = visa.ResourceManager()
    SCPI_90x0_SA = rm.open_resource(VISA_address_SA)
    SCPI_90x0_SA.timeot = 5000
    check_state_SA = 1

def checkConnectSA():
    global check_state_SA
    if check_state_SA > 0:
        setSA()
    return SCPI_90x0_SA.query(":SYSTem:ERRor?")

def setSA():
    global centerFreqSA, spanFreqSA, BDwRes, pwrRefLvl, spurLvl, atten, SAstartFreq, SAstopFreq, SABdwRes, THRpower, LimPowerStart, LimPowerStop
    SCPI_90x0_SA.write(':INITiate:SANalyzer')
    SCPI_90x0_SA.write(':SENSe:FREQuency:CENTer %G' % (centerFreqSA)) # Центральная чатсота диапазона измерений для анализатора спектра
    SCPI_90x0_SA.write(':SENSe:FREQuency:SPAN %G' % (spanFreqSA)) # Полоса обзора
    SCPI_90x0_SA.write(':SENSe:BANDwidth:RESolution %G' % (BDwRes)) #Полоса обзора
    SCPI_90x0_SA.write(':DISPlay:WINDow1:TRACe:Y:SCALe:RLEVel %G' % (pwrRefLvl)) #Опорный уровень обнаружения
    SCPI_90x0_SA.write(':CALCulate:MARKer1:STATe %d' % (1))
    SCPI_90x0_SA.write(':CALCulate:MARKer1:MAXimum')
    
    SCPI_90x0_SA.write(':CONFigure:SPURious:NDEFault')# обнаружение внеполосных излучений и выббросов
    SCPI_90x0_SA.write(':DISPlay:SPURious:VIEW1:SELect %s' % ('ALL'))
    SCPI_90x0_SA.write(':DISPlay:SPURious:VIEW:WINDow1:TRACe:Y:SCALe:RLEVel %G' % (spurLvl)) # опорный уровень отображения
    SCPI_90x0_SA.write(':SENSe:POWer:RF:ATTenuation %G' % (atten)) #ослабление аттенюатора
    SCPI_90x0_SA.write(':SENSe:SPURious:TYPE %s' % ('FULL'))    # измерение паразитных составляющих во всех диапазонах
    SCPI_90x0_SA.write(':SENSe:SPURious:REPT:MODE %s' % ('LIMTest'))
    SCPI_90x0_SA.write(':SENSe:SPURious:RANGe:LIST:STATe %s' % ('False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False'))
    SCPI_90x0_SA.write(':SENSe:SPURious:RANGe:LIST:STATe %s' % ('True,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False')) #утановка двух активных диапазонов
    SCPI_90x0_SA.write(':SENSe:SPURious:RANGe:LIST:FREQuency:STARt %s' % (SAstartFreq)) # начальные частоты 1 и 2 диапазона
    SCPI_90x0_SA.write(':SENSe:SPURious:RANGe:LIST:FREQuency:STOP %s' % (SAstopFreq)) # конечные частоты 1 и 2 диапазона
    SCPI_90x0_SA.write(':SENSe:FREQuency:CENTer %G' % (centerFreqSA)) # центральная частота диапазона измерений для анализатора спектра
    SCPI_90x0_SA.write(':SENSe:SPURious:RANGe:LIST:BANDwidth:RESolution %s' % (SABdwRes)) #полоса обзора каждого диапазона
    SCPI_90x0_SA.write(':SENSe:SPURious:RANGe:LIST:PEAK:THReshold %s' % (THRpower)) #минимальный уровень поиска для каждого диапазона
    SCPI_90x0_SA.write(':CALCulate:SPURious:RANGe:LIST:LIMit:ABSolute:UPPer:DATA:STOP:AUTO %s' % ('False,False')) #отключения автолимита ограничения поиска
    SCPI_90x0_SA.write(':CALCulate:SPURious:RANGe:LIST:LIMit:ABSolute:UPPer:DATA:STARt %s' % (LimPowerStart)) # уровень ограничения поиска
    SCPI_90x0_SA.write(':CALCulate:SPURious:RANGe:LIST:LIMit:ABSolute:UPPer:DATA:STOP %s' % (LimPowerStop))

def diconnectVna():
    instr.close()
    SCPI_90x0_SA.close()
    rm.close()

if __name__ == '__main__':
    print('\n')
    settingCalInstr()
    print('\n')
    calInstr()
    print('\n')
    postCalInstrSet()
    print('\n\n')
    setSA()
