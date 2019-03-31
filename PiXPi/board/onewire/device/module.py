import time
import struct

from ..utils import *
from ..exceptions import OneWireException, CRCError, DeviceError
from .generic import AddressableDevice


class AddressableModule(AddressableDevice):
    """
    class for sending raw commands
    """

    def __init__(self, bus, rom=None):
        """
        If no ROM code passed we suppose that thare is only one 1-wire device on the line!
        """
        AddressableDevice.__init__(self, bus)

        if rom is None:  # only one 1-wire module connected
            self.single_mode = True
            self.rom_code = self._read_ROM()
        else:
            self.single_mode = False
            self.rom_code = str2rom(rom)
            if not self.is_connected(self.rom_code):
                raise DeviceError('Device with ROM code %s not found' % rom2str(self.rom_code))
            self._reset()

    def _reset(self):
        """
        Send reset pulse, wait for presence and then select the device.
        """
        if self.single_mode:
            self._skip_ROM()  # because it is single device
        else:
            self._match_ROM(self.rom_code)


    def send_command(self, command_code):
        """
        sends single command to driver, waits for reponse and returns its[response] value
        """
        self._reset();

        self.bus.write_byte(command_code);

        #while self.bus.read_bit()!=0:
        #    print self.bus.read_bit()

        response = self.bus.read_byte()

        return response
