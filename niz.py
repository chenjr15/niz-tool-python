import struct
import hid
# Key name for 84EC(S)BLe
HWID2NAME = [
    '',  # unmapped value
    # first row
    'ESC', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'DEL',
    '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Back Sppace', 'Home',
    'TAB', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\', 'PgUP',
    'Caps Lock', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'Enter', 'PGDn',
    'L-Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'R-Shift', 'UP Arrow', 'End',
    'L-CTRL', 'L-FN', 'Left-Win', 'L-Alt', 'Space', 'R-FN', 'R-Alt', 'ContextMenu', 'R-Ctrl', 'Left Arrow', 'Down Arrow', 'Right Arrow',
]
# reference: https://github.com/cho45/niz-tools-ruby/blob/master/niz.rb
COMMAND_READ_SERIAL = 0x10
COMMAND_CALIB = 0xda
COMMAND_INITIAL_CALIB = 0xdb
COMMAND_PRESS_CALIB = 0xdd
# 0xd9 0x00 lock / 0xd9 0x01 unlock
COMMAND_KEYLOCK = 0xd9
COMMAND_PRESS_CALIB_DONE = 0xde
# TODO maybe macro
COMMAND_XXX_DATA = 0xe0
# TODO maybe macro
COMMAND_READ_XXX = 0xe2
COMMAND_READ_COUNTER = 0xe3
COMMAND_XXX_END = 0xe6
COMMAND_KEY_DATA = 0xf0
COMMAND_WRITE_ALL = 0xf1
COMMAND_READ_ALL = 0xf2
COMMAND_DATA_END = 0xf6
COMMAND_VERSION = 0xf9

VID = 0x0483
PID_NIZ_84EC_S_BLE = 0x5129

counter_example = [
    # CMD
    0, 227,
    # 不知道干什么的
    60,
    #    1-15个按键
    226, 0, 0, 0,
    12, 0, 0, 0,
    14, 0, 0, 0,
    18, 0, 0, 0,
    3, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    2, 0, 0, 0,
    9, 0, 0, 0,
    4, 0, 0, 0,
    2, 0, 0, 0,
    6, 0, 0, 0,
    21, 0, 0, 0,
    10, 1, 0, 0,
    16, 0, 0, 0,
    #    无用
    0]


class HidDevice(dict):

    @property
    def interface_number(self) -> int:
        ''' 2'''
        return self.get('interface_number')

    @property
    def manufacturer_string(self) -> str:
        ''' CATEX TECH.'''
        return self.get('manufacturer_string')

    @property
    def path(self) -> str:
        ''' path to open'''
        return self.get('path')

    @property
    def product_id(self) -> int:
        ''' 20777'''
        return self.get('product_id')

    @property
    def product_string(self) -> str:
        ''' Program '''
        return self.get('product_string')

    @property
    def release_number(self) -> int:
        ''' 0'''
        return self.get('release_number')

    @property
    def serial_number(self) -> str:
        ''' '''
        return self.get('serial_number')

    @property
    def usage(self) -> int:
        ''' 2'''
        return self.get('usage')

    @property
    def usage_page(self) -> int:
        ''' 1'''
        return self.get('usage_page')

    @property
    def vendor_id(self) -> int:
        ''' 1155'''
        return self.get('vendor_id')

    def __str__(self) -> str:
        return f"[0x{self.vendor_id:04X}:0x{self.product_id:x}] {self.interface_number} {self.manufacturer_string} SN:{self.serial_number} ({self.product_string})"


def choice_device(vid=0, pid=0, filters=[]) -> HidDevice:

    hids = [HidDevice(devdict) for devdict in hid.enumerate(vid, pid)]
    if filters:
        import re

        def match(dev: HidDevice) -> bool:
            return all(re.match(pattern, dev.get(key)) for key, pattern in filters)
        hids = [d for d in hids if match(d)]

    dev = None
    if len(hids) == 1:
        dev = hids[0]
    elif len(hids) > 1:
        for i, dev in enumerate(hids):
            print(i, dev)
        n = input("input number:")
        n = int(n)
        if n > -1 and n < len(hids):
            dev = hids[n]
    else:
        print("No device found(after filtered)!")

    print("selected:", dev)
    return dev


class Niz:
    def __init__(self, hiddev: HidDevice) -> None:
        self.device = hid.device()
        self.hiddev = hiddev
        self.device.open_path(hiddev.path)
        self.device.set_nonblocking(1)

    def version(self) -> str:
        self.send(COMMAND_VERSION)
        data = self.read(64)
        ver_str = None
        if data:
            # 2 byte command, 62 bytes version string
            _, ver = struct.unpack('H62s', bytes(data))
            ver_str = ver.decode()
        return ver_str

    def read_counter(self):
        self.send(COMMAND_READ_COUNTER)
        counters = [0]
        while True:
            data = self.read(64)
            if not data or data[1] != COMMAND_READ_COUNTER:
                break
            # 2 byte command, 15*4 byte counter(uint32 LE), 1 byte unused
            _cmd, _,  *cnt, _ = struct.unpack('<Hb15Ib', bytes(data))
            counters.extend(cnt)
        return counters

    def send(self, cmd, data="") -> int:
        '''
        send cmd to keyboard,format: 1 byte 0, two byte command, 62 byte data
        `!bH62s`
        '''
        data = data.encode()
        # 1 byte 0, two byte command, 62 byte data
        buf = struct.pack('!bH62s', 0, cmd, data)
        written = self.device.write(buf)
        return written

    def read(self, num=64, timeout=100) -> bytes:
        '''read data from hid device
        format: 2 bytes command, 62 bytes data'''
        data = None
        try:
            data = self.device.read(num, timeout)
        except IOError as e:
            print(e)
        return data

    def close(self):
        self.device.close()
