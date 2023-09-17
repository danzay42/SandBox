import time
from .visa_device_api import AbstractDevice, visa, visa_constants

DUT_MODE_WRITE = 0b00
DUT_MODE_READ = 0b01
DUT_MODE_SELECT = 0b10

FPGA_MODE_RST = 0b00
FPGA_MODE_DUT = 0b01
FPGA_MODE_ADC = 0b10
FPGA_MODE_PWM = 0b11

FPGA_DUT_READ = 1 << 5
FPGA_DUT_WRITE = 0
FPGA_DUT_TRIG = 1 << 4

PWM_BITS = 2 ** 5
ADC_BITS = 2 ** 12
ADC_VOLTAGE = 3.3
TMP36_TERM_BIAS = -0.5
TMP36_TERM_K = 0.01
FAN_FULL = 100
FAN_MEDIUM = 50


class FpgaDev(AbstractDevice):
    
    def __init__(self):
        super(FpgaDev, self).__init__()

    @staticmethod
    def get_fpga_bytes(fpga_mode, fpga_data=0, data=None):
        data = data or []
        return bytes([fpga_mode << 6 | 1 + fpga_data + len(data)] + data)

    @staticmethod
    def bytes_str(bytes_: bytes):
        return str(','.join(list(map(hex, bytes_))) + '|' + ','.join(list(map(bin, bytes_))))
    
    def connect_device(self, name):
        res = False
        try:
            res = super(FpgaDev, self).connect_device(name)
        except visa.VisaIOError as err:
            self.signal_error.emit(str(err))
        if res:
            self.transport = self.rm.open_resource(name)
            self.transport: visa.resources.SerialInstrument
            self.transport.baud_rate = 115200
            self.transport.stop_bits = visa_constants.StopBits.one
            self.transport.parity = visa_constants.Parity.even
            self.transport.timeout = self.default_timeout
            self.transport.read_termination = ''
            self.transport.write_termination = ''
        return res
        
    def device_list(self):
        return [dev for dev in super(FpgaDev, self).device_list() if 'ASRL' in dev]
    
    def write_bytes(self, data):
        try:
            super(FpgaDev, self).write_bytes(data)
        except AttributeError:
            self.signal_error.emit('')
            raise Exception('Устройство не подключено')
        print("FPGA WRITE:", FpgaDev.bytes_str(data))
        time.sleep(0.01)

    def read_bytes(self, size=1):
        time.sleep(0.01)
        try:
            data = super(FpgaDev, self).read_bytes(size)
        except AttributeError:
            self.signal_error.emit('')
            raise Exception('Устройство не подключено')
        print("FPGA READ:", FpgaDev.bytes_str(data))
        return data

    def rst(self):
        self.write_bytes(FpgaDev.get_fpga_bytes(FPGA_MODE_RST))

    def dut_write(self, dut_data: list):
        dut_data[0] |= DUT_MODE_WRITE
        self.write_bytes(FpgaDev.get_fpga_bytes(FPGA_MODE_DUT, FPGA_DUT_WRITE, dut_data))

    def dut_read(self, dut_data: list):
        dut_data[0] |= DUT_MODE_READ
        self.write_bytes(FpgaDev.get_fpga_bytes(FPGA_MODE_DUT, FPGA_DUT_READ, dut_data))
        data = self.read_bytes(10)
        return bin(data[0])

    def dut_select(self, dut_data: list):
        """clk_sel & trig"""
        dut_data[0] |= DUT_MODE_SELECT
        self.write_bytes(FpgaDev.get_fpga_bytes(FPGA_MODE_DUT, FPGA_DUT_TRIG, dut_data))

    def set_pwm(self, percent):
        """FAN_PUR"""
        pwm_data = (percent * PWM_BITS) // 100
        self.write_bytes(bytes([FPGA_MODE_PWM << 6 | pwm_data]))
        # self.write(get_fpga_bytes(FPGA_MODE_PWM, pwm_data))

    def get_temp(self):
        """ANALOG_TO_ADC"""
        self.write_bytes(FpgaDev.get_fpga_bytes(FPGA_MODE_ADC))
        res = self.read_bytes(2)
        temp_raw = int.from_bytes(res, byteorder='little', signed=True)
        voltage = temp_raw * (2 * ADC_VOLTAGE / ADC_BITS)
        temp = (voltage + TMP36_TERM_BIAS) / TMP36_TERM_K
        return int(temp), voltage

    def pulse(self):
        """SIGN"""
        self.write_bytes(bytes([FPGA_MODE_ADC << 6]))


# ____________________________________ tests ____________________________________
def test_i2c_device(port):
    bb = bytes([
        3, 0x68 << 1, 0x75,         # write: 0x68, 0x75
        1 << 5 | 2, 0x68 << 1 | 1   # read:  0x68, xxxx
    ])
    port.write(bb)
    port.read(512)


def test_temp(port, cycles):
    bb = FpgaDev.get_fpga_bytes(FPGA_MODE_ADC)
    for i in range(cycles):
        port.write(bb)
        res = port.read(512)
        if len(res) == 2:
            voltage = int.from_bytes(res, byteorder='little', signed=True) * (2 * ADC_VOLTAGE / ADC_BITS)
            print(f"U[{voltage:.2f}V]")
        else:
            print(f"[{len(res)}]error")
# ____________________________________ tests ____________________________________


if __name__ == '__main__':
    fpga = FpgaDev()
    print(fpga.device_list())
    fpga.connect_device('ASRL/dev/ttyUSB0')
   
    # fpga.reset()
    # time.sleep(1)
    # fpga.pulse()
    # fpga.dut_write([0xaa, 0x11])
    # fpga.dut_read([0x0])
    fpga.dut_select([0xAF])
    # fpga.set_pwm(50)
    # fpga.write(bytes([0b1100_0000]))
    # test_temp(fpga, cycles=10)
    # test_i2c_device(fpga)

