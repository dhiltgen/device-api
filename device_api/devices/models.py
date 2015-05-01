# Not based on Django ORM, but live data from the one-wire system
from pyownet import protocol
import logging
import os
from rest_framework.reverse import reverse_lazy

log = logging.getLogger(__name__)


# Seems a little silly...
protocol._SCK_TIMEOUT = 4


class Subdevice(object):
    def __init__(self, server, ow_device, subdevice):
        self.device = ow_device
        self.label = subdevice
        try:
            self.reading = str(server.read(ow_device + '/' + subdevice).decode())
        except:
            self.reading = None


class Device(object):
    def __init__(self, server, ow_device):
        log.info("XXX Instrumenting ow_device")
        #self.id = reverse_lazy('device-detail', kwargs={'device':os.path.basename(ow_device)})
        self.id = os.path.basename(ow_device)
        self.type = server.read(ow_device + '/type').decode()
        self.family = server.read(ow_device + '/family').decode()
        self.subdevices = [os.path.basename(x) for x in server.dir(ow_device, slash=False, bus=False)]


def _connect(server_name, server_port):
    try:
        log.error("Connecting to %s:%d", server_name, server_port)
        return protocol.proxy(server_name, server_port)
    except Exception as err:
        log.exception("Failed to retrieve devices: %r", err)
        raise


def get_all_devices(server_name=os.environ['OW_SERVER'], server_port=4304):
    server = _connect(server_name, server_port)
    return [Device(server, x) for x in server.dir(slash=False, bus=False)]


def get_device(ow_device, server_name=os.environ['OW_SERVER'], server_port=4304):
    server = _connect(server_name, server_port)
    return Device(server, ow_device)


def get_subdevice(ow_device, subdevice, server_name=os.environ['OW_SERVER'], server_port=4304):
    server = _connect(server_name, server_port)
    return Subdevice(server, ow_device, subdevice)
