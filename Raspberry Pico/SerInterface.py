# Modul für die serielle Kommunikation mit der Desktopanwendung
import time
import usb_cdc


class SerialInterface:
    def __init__(self):
        self.connection = usb_cdc.console
        self.connection.flush()

    def read(self):
        data = None
        if self.connection.in_waiting > 0:
            data = self.connection.read(self.connection.in_waiting).decode("utf-8")

        return data
    
    def send(self, data):
        self.connection.write(bytes(data, "utf-8"))