import visa
import time

# Общие настройки
VNA_VISA_address = 'TCPIP0::192.168.0.10::inst0::INSTR'  # Адрес векторного анализатора цепей
points = 201
startFreq = 8000000000.0
stopFreq = 12000000000.0
brwFreq = 1000.0
power_att = 0.0
pwrLvl = 0
pwrAttCenter = -30.0
pwrLvlTest = 0
powerMeterAdd = 'USB0::0x2A8D::0x3218::MY51500003::0::INSTR'
pathModel = ''


class Pacifier:
	def write(self, cmd):
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
	global power_att, points, startFreq, stopFreq, brwFreq, pwrLvl, pwrAttCenter, pwrLvlTest
	instr.write(':SYSTem:FPReset')
	instr.write(':DISPlay:WINDow1:STATe %d' % (1))
	instr.write(':CALCulate1:PARameter:DELete:ALL')
	instr.write(':CALCulate1:CUSTom:DEFine "%s","%s","%s"' % (
		'CH1_S21', 'Standard', 'S21'))  # создание переменной с типом измерения standart
	instr.write(':CALCulate1:PARameter:SELect "%s"' % ('CH1_S21'))
	instr.write(':DISPlay:WINDow1:TRACe2:FEED "%s"' % ('CH1_S21'))  # создание трассы и присвоение ей переменной CH1_S21
	instr.write(':SENSe1:SWEep:TYPE %s' % ('LINear'))  # Задание типа перестройки по частоте
	instr.write(':SENSe1:SWEep:POINts %d' % (points))  # Колицество точек
	instr.write(':SENSe1:FREQuency:STARt %G' % (startFreq))  # Начало диапазона частот
	instr.write(':SENSe1:FREQuency:STOP %G' % (stopFreq))  # Конец диапазона частот
	instr.write(':SENSe1:BWIDth:RESolution %G' % (brwFreq))  # разрешение по ширине полосы
	instr.write(':OUTPut:STATe %d' % (0))  # отключение канала измерения
	instr.write(':SOURce1:POWer1:COUPle %d' % (pwrLvlTest))  # уровень мощности тестовых портов
	instr.write(':SOURce1:POWer1:MODE %s' % ('ON'))  # ослабление источника первого измерительног порта: вкл.
	instr.write(':SOURce1:POWer1:ATTenuation:AUTO %d' % (0))  # авторегулировка ослабления: откл.
	instr.write(':SOURce1:POWer1:ATTenuation %G' % (power_att))  # величина ослабления источника
	instr.write(':SOURce1:POWer1:CENTer %G' % (pwrAttCenter))
	instr.write(':SOURce1:POWer1:LEVel:IMMediate:AMPLitude %G' % (pwrLvl))  # уровень мощности на выходе ВАЦ
	instr.write(':SOURce1:POWer1:ALC:MODE:RECeiver:STATe %d' % (1))  # использование опорного приемника Receiver-R1
	instr.write(':SOURce1:POWer1:ALC:MODE:RECeiver:OFFSet %G' % (0.0))  # смещение по частоте
	instr.write(':SENSe1:SWEep:MODE %s' % ('SINGle'))
	instr.write(':OUTPut:STATe %d' % (1))
	instr.write(':SENSe1:CORRection:PREFerence:CSET:SAVE %s' % (
		'CALRegister'))  # калибровка с использованием опорного приемника


def calInstr():  # Калибровка ВАЦ
	global powerMeterAdd
	instr.write(':SOURce:POWer:CORRection:COLLect:ITERation:NTOLerance %G' % (0.05))
	instr.write(':SYSTem:CONFigure:EDEVice:ADD "%s"' % ('power_receiver'))  # имя устройства
	instr.write(':SYSTem:CONFigure:EDEVice:DTYPe "%s","%s"' % ('power_receiver', 'Power Meter'))  # тип устройства
	instr.write(':SYSTem:COMMunicate:PSENsor %s,"%s"' % ('USB', 'Keysight Technologies,U2002H,MY51500003'))
	instr.write(':SYSTem:CONFigure:EDEVice:IOConfig "%s","%s"' % (
		'power_receiver', powerMeterAdd))  # visa-адрес измерителя мощности
	instr.write(':SYSTem:CONFigure:EDEVice:IOENable "%s",%d' % ('power_receiver', 1))
	instr.write(':SOURce1:POWer1:CORRection:COLLect:ACQuire %s,"%s"' % ('PMETer', 'ASENSOR'))  # начало калебровки
	instr.timeot = 10000
	instr.write(':CALCulate2:CUSTom:DEFine "%s","%s","%s"' % ('CH1_R1', 'Standard', 'R_1'))
	instr.write(':DISPlay:WINDow1:TRACe3:FEED "%s"' % ('CH1_R1'))
	instr.write(':CALCulate2:PARameter:SELect "%s"' % ('CH1_R1'))


def tracking():  # включение маркеров и настройка на поиск минимального уровня мощности
	global pathModel
	instr.write(':CALCulate1:MEASure1:MARKer1:STATe %d' % (1))
	instr.write(':CALCulate1:MEASure1:MARKer1:FUNCtion:DOMain:USER:STARt %G' % (startFreq))
	instr.write(':CALCulate1:MEASure1:MARKer1:FUNCtion:DOMain:USER:STOP %G' % (stopFreq))
	instr.write(':CALCulate1:MEASure1:MARKer1:FUNCtion:EXECute %s' % ('MINimum'))
	instr.write(':CALCulate1:MEASure1:MARKer1:FUNCtion:TRACking %d' % (1))
	instr.write(':CALCulate1:MEASure1:MARKer1:FUNCtion:SELect %s' % ('MINimum'))
	instr.write(':CALCulate1:FSIMulator:SENDed:PMCircuit:STATe %d' % (1))
	instr.write(':CALCulate1:FSIMulator:SENDed:PMCircuit:PORT1:USER:FILename "%s"' % (
		pathModel))  # путь к модели измерения на ВАЦ формата s2p
	instr.write(':CALCulate1:FSIMulator:SENDed:POWer:PORT1:COMPensate %d' % (
		1))  # компенсация мощности согласно выбранной модели


def diconnectVna():
	instr.close()
	rm.close()


if __name__ == '__main__':
	print('\n')
	settingCalInstr()
	print('\n')
	calInstr()
	print('\n')
	tracking()
