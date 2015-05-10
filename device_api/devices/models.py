# Not based on Django ORM, but live data from the one-wire system
from pyownet import protocol
import logging
import os
from rest_framework.reverse import reverse_lazy
import re

log = logging.getLogger(__name__)


# Seems a little silly...
protocol._SCK_TIMEOUT = 4


# Might want to move this someplace else...
subdevice_filter = dict(
    DS1420 = [],
    DS18S20 = [r'temperature', r'temphigh', r'templow'],
    DS2408 = [r'PIO.[0-9]'],
    DS2423 = [r'counters.[AB]$'],
    DS2438 = [r'humidity', r'temperature'],
)

class Subdevice(object):
    def __init__(self, server, ow_device, subdevice):
        self.server = "%s:%d" % (server._sockaddr[0], server._sockaddr[1])
        self.device = ow_device
        self.label = subdevice
        try:
            self.reading = str(server.read(ow_device + '/' + subdevice).decode())
            # XXX there's probably a better way...
            if self.label == 'temperature' or \
                    self.label == 'temphigh' or \
                    self.label == 'templow':
                self.reading = float(self.reading) * 9 / 5 + 32
        except Exception as e:
            log.exception("Failed to process reading: %r", e)
            self.reading = None

    def set_reading(self, reading):
        try:
            reading = str(reading)
            device_path = "%s/%s" % (self.device, self.label)
            server = _connect(self.server)
            log.info("Setting %r to %r (%r)", device_path , reading, type(reading))
            server.write(device_path, reading)
        except:
            log.exception("Failed to performing write of %s/%s <- %r",
                          self.device, self.label, reading)
            raise


class Device(object):
    def __init__(self, server, ow_device):
        self.server = "%s:%d" % (server._sockaddr[0], server._sockaddr[1])
        self.id = os.path.basename(ow_device)
        self.type = server.read(ow_device + '/type').decode()
        self.family = server.read(ow_device + '/family').decode()
        if self.type in subdevice_filter:
            self.subdevices = []
            for subdevice in server.dir(ow_device, slash=False, bus=False):
                subdevice = os.path.basename(subdevice)
                for pattern in subdevice_filter[self.type]:
                    if re.search(pattern, subdevice):
                        self.subdevices.append(subdevice)
        else:
            self.subdevices = [os.path.basename(x) for x in server.dir(ow_device, slash=False, bus=False)]


# TODO - This is probably leaking sockets...
def _connect(server):
    try:
        if ':' in server:
            server, port = server.split(':')
        else:
            port=4304
        log.info("Connecting to %s:%d", server, int(port))
        return protocol.proxy(server, int(port))
    except Exception as err:
        log.exception("Failed to retrieve devices from %s:%d: %r", server, int(port), err)
        raise


def get_all_devices(server=os.environ['OW_SERVER']):
    devices = []
    for name in server.split(','):
        server = _connect(name)
        devices.extend([Device(server, x) for x in server.dir(slash=False, bus=False)])
    return devices


def get_device(ow_device, server=os.environ['OW_SERVER']):
    for name in server.split(','):
        server = _connect(name)
        try:
            return Device(server, ow_device)
        except:
            pass
    raise Exception("Not Found")  # TODO Something better!


def get_subdevice(ow_device, subdevice, server=os.environ['OW_SERVER']):
    for name in server.split(','):
        server = _connect(name)
        try:
            return Subdevice(server, ow_device, subdevice)
        except:
            pass
    raise Exception("Not Found")  # TODO Something better!
