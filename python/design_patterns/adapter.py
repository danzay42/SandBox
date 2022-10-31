class UsbPort:
    def __init__(self) -> None:
        self.port_available = True    
    def plug(self, usb):
        if self.port_available:
            usb.plug_usb()
            self.port_available = False

class UsbCabel:
    def __init__(self) -> None:
        self.is_plugged = False
    def plug_usb(self):
        self.is_plugged = True

class MicroUsbCabel:
    def __init__(self) -> None:
        self.is_plugged = False
    def plug_micro_usb(self):
        self.is_plugged = True

class Adapter(UsbCabel):
    def __init__(self, micro_usb) -> None:
        self.micro_usb_cable = micro_usb
        self.micro_usb_cable.plug_micro_usb()

UsbPort().plug(UsbCabel())
UsbPort().plug(Adapter(MicroUsbCabel()))