import visa
import time

# Общие настройки
VNA_VISA_address = 'TCPIP0::192.168.0.101::hislip0::INSTR' # Адрес векторного анализатора цепей
points = 201
startFreq = 8000000000.0
stopFreq = 12000000000.0
brwFreq = 1000.0
power_att = 0.0
pwrLvl = 0
pwrLvlTest = 0
pathModel = ''
pwrAtt2 = 30.0
pwrLvl2 = -30.0
centerFreqPhase = 10000000000.0


class Pacifier:
    def write(self, cmd):
        print(cmd)
    
    def query(self, cmd):
        print(cmd)


instr = Pacifier()


def connectVna(VISA_address):
    global instr, check_state
    rm = visa.ResourceManager()
    instr = rm.open_resource(VISA_address)
    instr.timeot = 5000
    check_state = 1


def checkConnect():
    global check_state
    if check_state > 0:
        settingCalInstr()
    return instr.query(":SYSTem:ERRor?")


def settingCalInstr():  # настройка ВАЦ
    global power_att, points, startFreq, stopFreq, brwFreq, pwrLvl, pwrAtt2
    instr.write(':SYSTem:FPReset')
    instr.write(':DISPlay:WINDow1:STATe %d' % (1))
    instr.write(':CALCulate1:PARameter:DELete:ALL')
    instr.write(':CALCulate1:CUSTom:DEFine "%s","%s","%s"' % (
    'CH1_S21', 'Standard', 'S21'))  # создание переменной с типом измерения standart
    instr.write(':CALCulate1:PARameter:SELect "%s"' % ('CH1_S21'))
    instr.write(':DISPlay:WINDow1:TRACe2:FEED "%s"' % ('CH1_S21'))  # создание трассы и присвоение ей переменной CH1_S21
    instr.write(':CALCulate1:MEASure1:FORMat %s' % ('PHASe'))  # изменение фомата измерения на phase
    instr.write(':SENSe1:SWEep:POINts %d' % (points))  # Колицество точек
    instr.write(':SENSe1:FREQuency:STARt %G' % (startFreq))  # Начало диапазона частот
    instr.write(':SENSe1:FREQuency:STOP %G' % (stopFreq))  # Конец диапазона частот
    instr.write(':SENSe1:BWIDth:RESolution %G' % (brwFreq))  # разрешение по ширине полосы
    instr.write(':OUTPut:STATe %d' % (0))  # отключение канала измерения
    instr.write(':SOURce1:POWer1:COUPle %d' % (0))
    instr.write(':SOURce1:POWer1:ATTenuation:AUTO %d' % (0))  # авторегулировка ослабления: откл.
    instr.write(':SOURce1:POWer1:ATTenuation %G' % (power_att))  # величина ослабления источника
    instr.write(':SOURce1:POWer1:LEVel:IMMediate:AMPLitude %G' % (pwrLvl))  # уровень мощности на выходе ВАЦ
    instr.write(':SOURce1:POWer1:ALC:MODE:RECeiver:STATe %d' % (1))  # использование опорного приемника Receiver-R1
    instr.write(':SOURce1:POWer1:ALC:MODE:RECeiver:OFFSet %G' % (0.0))  # смещение по частоте
    instr.write(':SOURce1:POWer2:ATTenuation:AUTO %d' % (0))
    instr.write(':SENSe1:POWer:ATTenuator %s,%G' % (
    'BRECeiver', pwrAtt2))  # ослабление аттенюатора второго измерительного порта
    instr.write(':SOURce1:POWer2:LEVel:IMMediate:AMPLitude %G' % (pwrLvl2))  # мощность на выходе второго порта
    instr.write(':OUTPut:STATe %d' % (1))


def calInstr():  # Калибровка ВАЦ
    global data
    data = instr.query(':SENSe1:CORRection:COLLect:CKIT:INFormation? %s,%s' % (
    'ECAL1', 'CHAR0'))  # опрос о подключенной калебровочной мере
    instr.write(':SENSe1:CORRection:COLLect:GUIDed:ECAL:ACQuire %s,%s' % ('SOLT', '1,2'))  # калибровка


def memory():
    # на исследуемое устройство подается напряжение питания производится настройка ВАЦ и полученная трасса записывается в память как опорная
    instr.write(':SENSe1:AVERage:COUNt %d' % (10))
    instr.write(':SENSe1:AVERage:STATe %d' % (1))
    instr.write(':CALCulate1:MEASure1:MATH:MEMorize')  # внешение в память откаллиброванной фазы


def tracking():  # включение маркеров и настройка на отслеживание сдвина фазы в 3 точках, начало диапазона, центр диапазона, конец диапазона
    global centerFreqPhase
    # на ислледуемое устройство подается напряжение питания для изменения фазы
    instr.write(':CALCulate1:MEASure1:MATH:FUNCtion %s' % (
        'DIVide'))  # рассчет отношения между опорной трассой и измеряемой в данный момент
    instr.write(':CALCulate1:MEASure1:MARKer1:STATe %d' % (1))
    instr.write(':CALCulate1:MEASure1:MARKer2:STATe %d' % (1))
    instr.write(':CALCulate1:MEASure1:MARKer3:STATe %d' % (1))
    instr.write(':CALCulate1:MEASure1:MARKer1:X %s' % ('MIN'))
    instr.write(':CALCulate1:MEASure1:MARKer2:X %G' % (centerFreqPhase))
    instr.write(':CALCulate1:MEASure1:MARKer3:X %s' % ('MAX'))


def diconnectVna():
    instr.close()
    rm.close()


if __name__ == '__main__':
    print('\n')
    settingCalInstr()
    print('\n')
    calInstr()
    print('\n')
    memory()
    print('\n')
    tracking()
