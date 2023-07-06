import socket
import subprocess
import logging

from odoo.addons.hw_drivers.interface import Interface

_logger = logging.getLogger(__name__)


class PrinterSocketInterface(Interface):
    _loop_delay = 10
    connection_type = 'printer'
    printer_socket_devices = {}

    def get_devices(self):
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sk.connect(('8.8.8.8', 1))
        local_ip_address = sk.getsockname()[0]
        ip_list = local_ip_address.split('.')
        ip_list.pop()
        r_ip = '.'
        self.range_ip = r_ip.join(ip_list)
        sk.close()
        port = 9100
        for i in range(1, 256):
            ip = self.range_ip + '.' + str(i)
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.2)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    sock.close()
                    res = subprocess.run(["sudo", "python3", "/home/pi/odoo/addons/viin_hw_drivers/tools/get_mac_add.py", ip], capture_output=True, text=True)
                    identifier = res.stdout.strip()
                    self.printer_socket_devices[identifier] = {'device-class': 'network',
                                                               'device-make-and-model': 'printsocket' + ip,
                                                               'identifier': identifier,
                                                               'device-id': '',
                                                               'ip_socket': ip
                                                               }
                    continue
                sock.close()  
            except:
                _logger.error(('Scan IP %s Error') % (ip))
        return self.printer_socket_devices
