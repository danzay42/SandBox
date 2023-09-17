import time

from header import *


class Worker(QThread):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.fn(*self.args, **self.kwargs)


class TCPDrive(QObject):
    INTERFACE = 'eth0'
    PORT = '5025'
    IP = '192.168.0.100'
    MASK = '255.255.255.0'
    GATEWAY = '0.0.0.0'

    signal_recv_message = pyqtSignal(object)
    signal_info = pyqtSignal(object)

    _encoding = 'ASCII'
    _timeout = 0.1
    _cycle_timeout = 0.001
    _queue = 100

    _recv_thread: Worker = None
    _listen_thread: Worker = None
    _connect_sock: socket = None
    _listen_sock: socket = None
    _work: bool = True
    
    def __init__(self):
        super(TCPDrive, self).__init__()
        self.INTERFACE = self.get_interface()

        self._recv_thread = Worker(self.receive)
        self._listen_thread = Worker(self.listen)
        self._recv_thread.start()
        self._listen_thread.start()

    def start(self):
        self.set_ip_mask_gateway(self.IP, self.MASK, self.GATEWAY)
        
        self._listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listen_sock.settimeout(self._timeout)
        while True:
            try:
                self._listen_sock.bind(('', int(self.PORT)))
                break
            except socket.error:
                time.sleep(self._timeout)
                logger.error(traceback.format_exc())
                continue
        self._listen_sock.listen(self._queue)
        self._listen_info()
        self._work = True

    def stop(self):
        self._work = False
        self._recv_thread.wait()
        self._listen_thread.wait()

    # ------------------------------------------------------------------------------------------------------------------
    def listen(self):
        while self._work:
            try:
                self._connect_sock, addr = self._listen_sock.accept()
            except (OSError, AttributeError):
                time.sleep(self._cycle_timeout)
            else:
                self._connect_sock.settimeout(self._timeout)
                logger.debug(f'connection established:\n{addr}')
        logger.debug("TCP listen close")

    def receive(self):
        while self._work:
            try:
                data = self._connect_sock.recv(1024)
            except (OSError, AttributeError):
                time.sleep(self._cycle_timeout)
            else:
                if data:
                    logger.debug(f"TCP receive: [{data}]")
                    self.signal_recv_message.emit(data.decode(encoding=self._encoding))
        logger.debug("TCP receive close")

    def send(self, data):
        data = str(data)
        logger.debug(f"TCP send: [{data}]")
        data += '\r\n'
        for i in range(10):
            try:
                self._connect_sock.send(data.encode(encoding=self._encoding))
                break
            except (OSError, AttributeError):
                continue

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_interface():
        interfaces = netifaces.interfaces()
        interface = TCPDrive.INTERFACE if TCPDrive.INTERFACE in interfaces else interfaces[1]
        return interface
    
    @staticmethod
    def get_ip(iface):
        try:
            return netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
        except KeyError:
            return '0.0.0.0'
        
    @staticmethod
    def get_mask(iface):
        try:
            return netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['netmask']
        except KeyError:
            return '0.0.0.0'

    @staticmethod
    def get_gateway(iface):
        try:
            gateway, g_iface = netifaces.gateways()['default'][netifaces.AF_INET]
            if g_iface != iface:
                logger.error(f"Gateway error: iface={iface}, g_iface={g_iface}")
            return gateway
        except KeyError:
            return '0.0.0.0'

    def set_ip_mask_gateway(self, ip=IP, mask=MASK, gateway=GATEWAY):
        res = subprocess.call(f"ifconfig {self.INTERFACE} down".split(' '))

        res += subprocess.call(f"ifconfig {self.INTERFACE} {ip} netmask {mask}".split(' '))
        if (int(ipaddress.ip_address(gateway)) & int(ipaddress.ip_address(mask))) \
                == (int(ipaddress.ip_address(ip)) & int(ipaddress.ip_address(mask))):
            res += subprocess.call(f"ip route add {ip} via {gateway}".split(' '))
            self.GATEWAY = gateway

        res += subprocess.call(f"ifconfig {self.INTERFACE} up".split(' '))
        logger.debug(res)
        self.IP, self.MASK = ip, mask

    def set_dhcp(self):
        subprocess.check_call(f"ifconfig {self.INTERFACE} 0.0.0.0 0.0.0.0 && dhclient".split(' '))
    
    def _listen_info(self):
        ip = self.get_ip(self.INTERFACE)
        logger.debug(f"TCP Listen: [{ip}][{self.PORT}]")
        info = f"IP: {ip}\nPORT: {self.PORT}\n"
        info += f"MASK: {self.get_mask(self.INTERFACE)}\nGATEWAY: {self.get_gateway(self.INTERFACE)}"
        self.signal_info.emit(info)
