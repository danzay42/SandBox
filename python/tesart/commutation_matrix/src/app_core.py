from header import *
import src.logger
from src.ethernet_drive import TCPDrive
from src.async_ethernet_drive import AsyncSocketServer
from src.uart_drive import UARTDrive
from src.matrix import MatrixBase
from src.qt_gui import MainWindow
from src.app_errors import *
import typing


class Core(QApplication):
    OPERATION_COMPLETE: bool = False
    _save_path = path + '/save_config.ini'
    _log_path = path

    ERRORS:         typing.List[MatrixError] = []
    MATRIX:         MatrixBase = None
    GUI:            MainWindow = None
    TCP:            AsyncSocketServer = None
    UART:           UARTDrive = None

    # Qt Application functions -----------------------------------------------------------------------------------------
    def __init__(self, gui_obj: type(MainWindow), matrix_obj: type(MatrixBase)):
        sys.excepthook = self.core_except_hook
        super(Core, self).__init__(sys.argv)

        self.GUI = gui_obj()
        self.MATRIX = matrix_obj()
        self.TCP = AsyncSocketServer(handler=self.tcp_receive)
        self.UART = UARTDrive()

        # signals
        self.GUI.signal_close.connect(self.close)
        self.GUI.signal_switch.connect(self.auto_switch)
        self.TCP.signal_info.connect(self.GUI.show_message)
        
        self.load_configuration()
        self.load_matrix()
        self.TCP.start()

    def core_except_hook(self, exc_type, exc_obj, exc_tb):
        msg = ''.join(traceback.format_exception(exc_type, exc_obj, exc_tb))
        if isinstance(exc_obj, MatrixError):
            logger.error(msg)
            self.ERRORS.append(exc_obj)
            self.OPERATION_COMPLETE = True
            self.GUI.signal_show_message.emit(str(exc_obj), True, False)
        elif isinstance(exc_obj, KeyboardInterrupt):
            logger.error(msg)
        else:
            logger.fatal(msg)
            self.GUI.signal_show_message.emit(f"FATAL Error\n"
                                              f"Please have a look at the log file for details:\n"
                                              f"{self._log_path}", True, True)
            self.close()

    def close(self):
        self.TCP.stop()
        self.save_configuration(True, True, True)
        self.closeAllWindows()
        self.quit()

    # ------------------------------------------------------------------------------------------------------------------
    def tcp_receive(self, receive: str):
        try:
            result = [self.cmd_parse(cmd.upper().strip()) for cmd in receive.split(';')]
            return ';'.join(map(str, filter(bool, result)))
        except MatrixError as e:
            logger.error(traceback.format_exc())
            self.ERRORS.append(e)
            self.OPERATION_COMPLETE = True
            self.GUI.signal_show_message.emit(str(e), True, False)
        except Exception as e:
            logger.fatal(e)
            self.GUI.signal_show_message.emit(f"FATAL Error\n"
                                              f"Please have a look at the log file for details:\n"
                                              f"{self._log_path}", True, True)

    def cmd_parse(self, cmd: str):
        try:
            if cmd == '*IDN?':
                return self.idn_command()
            elif cmd == '*RST':
                self.rst_matrix()
            elif cmd == '*OPC?':
                return self.operation_complete()
            elif cmd == 'SYSTEM:ERROR?':
                return self.error_status()
            elif cmd.startswith('STATE:SWITCH:MANUAL'):
                return self.manual_switch_parse(cmd.lstrip('STATE:SWITCH:MANUAL').split(','))
            elif cmd.startswith('STATE:SWITCH'):
                return self.auto_switch_parse(cmd.lstrip('STATE:SWITCH').split(','))
            # elif cmd.startswith('SYSTEM:CONFIG:IPADDRESS'):
            #     self.system_ipaddr_config(cmd.lstrip('SYSTEM:CONFIG:IPADDRESS'))
            # elif cmd.startswith('SYSTEM:CONFIG:IPMASK'):
            #     self.system_ipmask_config(cmd.lstrip('SYSTEM:CONFIG:IPMASK'))
            # elif cmd.startswith('SYSTEM:CONFIG:IPDEFGATEWAY'):
            #     self.system_ipgateway_config(cmd.lstrip('SYSTEM:CONFIG:IPDEFGATEWAY'))
            elif cmd.startswith('SYSTEM:IPADDRESS'):
                return self.system_ipaddr_config(cmd.lstrip('SYSTEM:IPADDRESS'))
            elif cmd.startswith('SYSTEM:IPMASK'):
                return self.system_ipmask_config(cmd.lstrip('SYSTEM:IPMASK'))
            elif cmd.startswith('SYSTEM:IPDEFGATEWAY'):
                return self.system_ipgateway_config(cmd.lstrip('SYSTEM:IPDEFGATEWAY'))
            elif cmd.startswith('SYSTEM:TCPPORT'):
                return self.system_tcpport_config(cmd.lstrip('SYSTEM:TCPPORT'))
            elif cmd.startswith('SYSTEM:CONFIG:IDN'):
                return self.system_config(cmd.lstrip('SYSTEM:CONFIG:IDN'))
            else:
                raise WrongParameter()
        except ValueError:
            raise WrongParameter()
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def _manual_switch(self, board, switch, ch):
        try:
            self.UART.send(board, switch, ch)
        except (IndexError, TimeoutError, ConnectionError):
            raise NoSwitchStatus()
        except ValueError:
            raise ErrorTransferData()

    def manual_switch(self, board, switch, ch):
        if not self.MATRIX.check_switch(board, switch, ch):
            self.OPERATION_COMPLETE = False
            self._manual_switch(board, switch, ch)
            logger.debug(f"Manual: [{board}, {switch}, {ch}]")
            self.MATRIX.save_switch(board, switch, ch)
            self.OPERATION_COMPLETE = True

    def auto_switch(self, input_, output_):
        if not self.MATRIX.check_commutation(input_, output_):
            for board, switch, ch in self.MATRIX.auto_to_manual(input_, output_):
                self.manual_switch(board, switch, ch)
            logger.info(f"Auto: {input_} to {output_}")
            self.MATRIX.save_commutation(input_, output_)
            self.save_configuration(commutation=True)
        self.GUI.switch_result(input_, output_)

    def rst_matrix(self):
        try:
            for board, switch, ch in self.MATRIX.reset():
                self.manual_switch(board, switch, ch)
            for input_, output_ in self.MATRIX.COMMUTATION.items():
                self.auto_switch(input_, self.MATRIX.OUTPUTS[0])
        except MatrixError:
            pass
        os.remove(self._save_path)
        self.ERRORS = []

    def load_matrix(self):
        try:
            for board, switch, ch in self.MATRIX.load():
                self.manual_switch(board, switch, ch)
        except MatrixError:
            for input_, output_ in self.MATRIX.COMMUTATION.items():
                self.MATRIX.save_commutation(input_, self.MATRIX.OUTPUTS[0])
            logger.error("Load Save - failed!")

        for input_, output_ in self.MATRIX.COMMUTATION.items():
            logger.debug(f"{input_} to {output_}")
            self.GUI.switch_result(input_, output_)

    # ------------------------------------------------------------------------------------------------------------------
    def idn_command(self):
        return f"{self.MATRIX.MODEL},{self.MATRIX.SERIAL_NUMBER}," \
               f"{self.MATRIX.MANUFACTURE},{self.MATRIX.FIRMWARE_VERSION}"

    def operation_complete(self):
        return str(int(self.OPERATION_COMPLETE))

    def error_status(self):
        if self.ERRORS:
            return repr(self.ERRORS.pop())
        else:
            return repr(NoError())

    def auto_switch_parse(self, cmd):
        if len(cmd) == 2:
            input_, output_ = map(int, cmd)
            self.MATRIX.check_auto_values(input_, output_)
            self.auto_switch(input_, output_)
        elif len(cmd) == 1 and cmd[0].endswith("?"):
            input_, _ = int(cmd[0][:-1]), self.MATRIX.OUTPUTS[0]
            self.MATRIX.check_auto_values(input_, _)
            return self.MATRIX.COMMUTATION[input_]
        else:
            raise WrongParameter()

    def manual_switch_parse(self, cmd):
        if len(cmd) == 3:
            pcb, switch, output = map(int, cmd)
            self.MATRIX.check_manual_values(pcb, switch, output)
            self.manual_switch(pcb, switch, output)
        elif len(cmd) == 2 and cmd[1].endswith("?"):
            pcb, switch, _ = int(cmd[0]), int(cmd[1][:-1]), self.MATRIX.CHANNELS[0]
            self.MATRIX.check_manual_values(pcb, switch, _)
            return self.MATRIX.SWITCH_STATUS[pcb][switch]
        else:
            raise WrongParameter()

    def system_ipaddr_config(self, cmd):
        if cmd == '' or cmd == '?':
            return self.TCP.IP
        else:
            ip = ipaddress.ip_address(cmd)
            self.TCP.set_ip_mask_gateway(ip=str(ip))
            self.save_configuration(tcp=True)

    def system_ipmask_config(self, cmd):
        if cmd == '' or cmd == '?':
            return self.TCP.MASK
        else:
            ip = ipaddress.ip_address(cmd)
            self.TCP.set_ip_mask_gateway(mask=str(ip))
            self.save_configuration(tcp=True)

    def system_ipgateway_config(self, cmd):
        if cmd == '' or cmd == '?':
            return self.TCP.GATEWAY
        else:
            ip = ipaddress.ip_address(cmd)
            self.TCP.set_ip_mask_gateway(gateway=str(ip))
            self.save_configuration(tcp=True)

    def system_tcpport_config(self, cmd):
        if cmd == '' or cmd == '?':
            return self.TCP.PORT
        else:
            cmd = int(cmd)
            if cmd != self.TCP.PORT and cmd in range(2**16):
                self.TCP.set_port(cmd)
                self.save_configuration(tcp=True)
            else:
                raise WrongParameter()

    def system_config(self, cmd):
        cmd = cmd.strip()
        if cmd == '' or cmd == '?':
            return self.idn_command()
        elif len(cmd.split(',')) == 4:
            data = cmd.split(',')
            self.MATRIX.MODEL = data[0]
            self.MATRIX.SERIAL_NUMBER = data[1]
            self.MATRIX.MANUFACTURE = data[2]
            self.MATRIX.FIRMWARE_VERSION = data[3]
            self.save_configuration(matrix=True)
        else:
            raise WrongParameter()

    # ------------------------------------------------------------------------------------------------------------------
    _s_model = 'MODEL'
    _s_serial_num = 'SERIAL_NUMBER'
    _s_manufacture = 'MANUFACTURE'
    _s_fv = 'FIRMWARE_VERSION'
    _s_cmt = 'COMMUTATION'

    _s_port = 'TCP_PORT'
    _s_ip = 'IP'
    _s_ip_mask = 'MASK'
    _s_gateway = 'GATEWAY'

    def save_configuration(self, matrix=False, tcp=False, commutation=False):
        if matrix or tcp or commutation:
            settings = QSettings(self._save_path, QSettings.IniFormat)
            if matrix:
                settings.beginGroup("MATRIX")
                settings.setValue(self._s_model, self.MATRIX.MODEL)
                settings.setValue(self._s_serial_num, self.MATRIX.SERIAL_NUMBER)
                settings.setValue(self._s_manufacture, self.MATRIX.MANUFACTURE)
                settings.setValue(self._s_fv, self.MATRIX.FIRMWARE_VERSION)
                settings.endGroup()
            
            if tcp:
                settings.beginGroup("TCP")
                settings.setValue(self._s_port, self.TCP.PORT)
                settings.setValue(self._s_ip, self.TCP.IP)
                settings.setValue(self._s_ip_mask, self.TCP.MASK)
                settings.setValue(self._s_gateway, self.TCP.GATEWAY)
                settings.endGroup()
            
            if commutation:
                settings.beginGroup("MATRIX_COMMUTATION")
                settings.setValue(self._s_cmt, self.MATRIX.COMMUTATION)
                settings.endGroup()
                
            settings.sync()

    def load_configuration(self):
        settings = QSettings(self._save_path, QSettings.IniFormat)
        settings.beginGroup("MATRIX")
        self.MATRIX.MODEL = settings.value(
            self._s_model, defaultValue=self.MATRIX.MODEL, type=str)
        self.MATRIX.SERIAL_NUMBER = settings.value(
            self._s_serial_num, defaultValue=self.MATRIX.SERIAL_NUMBER, type=str)
        self.MATRIX.MANUFACTURE = settings.value(
            self._s_manufacture, defaultValue=self.MATRIX.MANUFACTURE, type=str)
        self.MATRIX.FIRMWARE_VERSION = settings.value(
            self._s_fv, defaultValue=self.MATRIX.FIRMWARE_VERSION, type=str)
        settings.endGroup()

        settings.beginGroup("TCP")
        self.TCP.PORT = settings.value(self._s_port, defaultValue=self.TCP.PORT, type=str)
        self.TCP.IP = settings.value(self._s_ip, defaultValue=self.TCP.IP, type=str)
        self.TCP.MASK = settings.value(self._s_ip_mask, defaultValue=self.TCP.MASK, type=str)
        self.TCP.GATEWAY = settings.value(self._s_gateway, defaultValue=self.TCP.GATEWAY, type=str)
        settings.endGroup()

        settings.beginGroup("MATRIX_COMMUTATION")
        self.MATRIX.COMMUTATION = settings.value(
            self._s_cmt, defaultValue=self.MATRIX.COMMUTATION, type=dict)
        settings.endGroup()

    # ------------------------------------------------------------------------------------------------------------------
