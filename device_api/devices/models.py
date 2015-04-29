# Not based on Django ORM, but live data from the one-wire system
from pyownet import protocol
import logging
import os

log = logging.getLogger(__name__)


class Device(object):
    def __init__(self, server, ow_device):
        log.info("XXX Instrumenting ow_device")
        self.id = ow_device
        self.type = server.read(ow_device + '/type').decode()
        self.family = server.read(ow_device + '/family').decode()
        # TODO - figure out how to do sub-devices for different readings
        try:
            temp = float(server.read(ow_device + '/temperature'))
        except:
            temp = 0.0
        self.temp = temp


def get_all_devices(server_name=os.environ['OW_SERVER'], server_port=4304):
    try:
        log.error("Connecting to %s:%d", server_name, server_port)
        server = protocol.proxy(server_name, server_port)
    except Exception as err:
        log.exception("Failed to retrieve devices: %r", err)
        raise
    return [Device(server, x) for x in server.dir(slash=False, bus=False)]
