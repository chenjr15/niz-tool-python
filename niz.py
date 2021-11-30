import struct
import logging
from typing import List
import hid
logger = logging.getLogger(__name__)

# reference: https://github.com/cho45/niz-tools-ruby/blob/master/niz.rb
HWCODE = {
    0: '',
    1: 'ESC',
    2: 'F1',
    3: 'F2',
    4: 'F3',
    5: 'F4',
    6: 'F5',
    7: 'F6',
    8: 'F7',
    9: 'F8',
    10: 'F9',
    11: 'F10',
    12: 'F11',
    13: 'F12',
    14: '`',
    15: '1',
    16: '2',
    17: '3',
    18: '4',
    19: '5',
    20: '6',
    21: '7',
    22: '8',
    23: '9',
    24: '0',
    25: '-',
    26: '=',
    27: 'BS',
    28: 'TAB',
    29: 'Q',
    30: 'W',
    31: 'E',
    32: 'R',
    33: 'T',
    34: 'Y',
    35: 'U',
    36: 'I',
    37: 'O',
    38: 'P',
    39: '[',
    40: ']',
    41: '\\',
    42: 'Caps Lock',
    43: 'A',
    44: 'S',
    45: 'D',
    46: 'F',
    47: 'G',
    48: 'H',
    49: 'J',
    50: 'K',
    51: 'L',
    52: ';',
    53: '\'',
    54: 'RET',
    55: 'L-Shift',
    56: 'Z',
    57: 'X',
    58: 'C',
    59: 'V',
    60: 'B',
    61: 'N',
    62: 'M',
    63: ',',
    64: '.',
    65: '/',
    66: 'R-Shift',
    67: 'L-CTRL',
    68: 'Left-Super',
    69: 'L-Alt',
    70: 'Space',
    71: 'R-Alt',
    72: 'Right-Super',
    73: 'ContextMenu',
    74: 'R-Ctrl',
    75: 'Wakeup',
    76: 'Sleep',
    77: 'Power',
    78: 'PriSc',
    79: 'SclLk',
    80: 'Pause',
    81: 'Ins',
    82: 'Home',
    83: 'PageUp',
    84: 'Del',
    85: 'End',
    86: 'PageDown',
    87: 'Up Arrow',
    88: 'Left Arrow',
    89: 'Down Arrow',
    90: 'Right Arrow',
    91:  'Num Lock',
    92: '(/)',
    93: '(*)',
    94: '(7)',
    95: '(8)',
    96: '(9)',
    97: '(4)',
    98: '(5)',
    99: '(6)',
    100: '(1)',
    101: '(2)',
    102: '(3)',
    103: '(0)',
    104: '(.)',
    105: '(-)',
    106: '(+)',
    107: '(Enter)',
    108: 'Media Next Track',
    109: 'Media Previous Track',
    110: 'Media Stop',
    111: 'Media Play/Pause',
    112: 'Media Mute',
    113: 'Media VolumeUp',
    114: 'Media VolumeDn',
    115: 'Media Select',
    116: 'WWW Email',
    117: 'Media Calculator',
    118: 'Media My Computer',
    119: 'WWW Search',
    120: 'WWW Home',
    121: 'WWW Back',
    122: 'WWW Forward',
    123: 'WWW Stop',
    124: 'WWW Refresh',
    125: 'WWW Favorites',
    126: 'Mouse Left',
    127: 'Mouse Right',
    128: 'Mouse Up',
    129: 'Mouse Down',
    130: 'Mouse Key Left',
    131: 'Mouse Key Right',
    132: 'Mouse Key Middle',
    133: 'Mouse Wheel Up',
    134: 'Mouse Wheel Dn',
    135: 'Backlight Switch',
    136: 'Backlight Macro',
    137: 'Demonstrate',
    138: 'Star shower',
    139: 'Riffle',
    140: 'Demo Stop',
    141: 'Breathe',
    142: 'Breathe Sequence-',
    143: 'Breathe Sequence+',
    144: 'Backlight Lightness-',
    145: 'Backlight Lightness+',
    146: 'Sunset or Relax/Aurora',
    147: 'Color Breathe',
    148: 'Back Color Exchange',
    149: 'Adjust Trigger Point',
    150: 'Keyboard Lock',
    151: 'Shift&Up',
    152: 'Ctrl&Caps Exchange',
    153: 'WinLock',
    154: 'MouseLock',
    155: 'Win/Mac Exchange',
    156: 'R-Fn',
    157: 'Mouse Unit Pixel',
    158: 'Mouse Unit Time',
    159: 'Programmable keyboard',
    160: 'Backlight Record1',
    161: 'Backlight Record2',
    162: 'Backlight Record3',
    163: 'Backlight Record4',
    164: 'Backlight Record5',
    165: 'Backlight Record6',
    166: 'L-Fn',
    167: 'Wire/Wireless exchange',
    168: 'BTD1',
    169: 'BTD2',
    170: 'BTD3',
    171: 'Game',
    172: 'ECO',
    173: 'Mouse First Delay',
    174: 'Key Repeat Rate',
    175: 'Key Response Delay',
    176: 'USB Report Rate',
    177: 'Key Scan Period',
    178: 'App Lock',
    179: 'unknown',
    180: 'unknown',
    181: 'unknown',
    182: 'unknown',
    183: 'unknown',
    184: 'unknown',
    185: 'unknown',
    186: 'unknown',
    187: 'unknown',
    188: 'unknown',
    189: 'unknown',
    190: 'unknown',
    191: 'unknown',
    192: 'unknown',
    193: 'unknown',
    194: 'unknown',
    195: 'unknown',
    196: 'unknown',
    197: 'unknown',
    198: 'unknown',
    199: 'Mouse Left Double Click',
    200: 'unknown',
    201: 'unknown',
    202: 'unknown',
    203: 'unknown',
    204: '<>|',
    205: 'unknown',
    206: 'unknown',
    207: 'unknown',
    208: 'unknown',
    209: 'unknown',
    210: 'unknown',
    211: 'unknown',
    212: 'unknown',
    213: 'unknown',
    214: 'unknown',
    215: 'unknown',
    216: 'unknown',
    217: 'unknown',
    218: 'unknown',
    219: 'unknown',
    220: 'unknown',
    221: 'unknown',
    222: 'unknown',
    223: 'unknown',
    224: 'unknown',
    225: 'unknown',
    226: 'unknown',
    227: 'unknown',
    228: 'unknown',
    229: 'unknown',
    230: 'unknown',
    231: 'unknown',
    232: 'unknown',
    233: 'unknown',
    234: 'unknown',
    235: 'unknown',
    236: 'unknown',
    237: 'unknown',
    238: 'unknown',
    239: 'unknown',
    240: 'unknown',
    241: 'unknown',
    242: 'unknown',
    243: 'unknown',
    244: 'unknown',
    245: 'unknown',
    246: 'unknown',
    247: 'unknown',
    248: 'unknown',
    249: 'unknown',
    250: 'unknown',
    251: 'unknown',
    252: 'unknown',
    253: 'unknown',
    254: 'unknown',
    255: 'unknown', }
LEVEL2NAME = [
    'UNKNOWN',
    'Normal',
    'R - FN',
    'L - FN',
]
UNSET = 0x000
SINGLE_KEY = 0x0001
COMBO_KEY = 0x0002
MACRO_DEF = 0x0201
SIM_HIT = 0x0100
MODE2NAME = {
    UNSET: 'unset',
    SINGLE_KEY: '单键',
    COMBO_KEY: '组合键',
    MACRO_DEF: '宏定义',
    SIM_HIT: '模拟击键',
}
# Key id to name mapping for 84EC(S)BLe
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


class Command:

    READ_SERIAL = 0x10
    CALIB = 0xda
    INITIAL_CALIB = 0xdb
    PRESS_CALIB = 0xdd
    # 0xd9 0x00 lock / 0xd9 0x01 unlock
    KEYLOCK = 0xd9
    PRESS_CALIB_DONE = 0xde
    KEY_DATA = 0xf0
    WRITE_KEY_MAP = 0xf1
    READ_KEY_MAP = 0xf2
    DATA_END = 0xf6
    VERSION = 0xf9
    # -- unknown --
    #  maybe macro
    XXX_DATA = 0xe0
    #  maybe macro
    READ_XXX = 0xe2
    READ_COUNTER = 0xe3
    XXX_END = 0xe6


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
micro_example_niz = [
    0, 0, 0, 24,
    # N down 107 ms
    61, 200, 0, 107,
    # I down 123 ms
    36, 200, 0, 23,
    # N up 83 ms
    61, 200, 0, 83,
    # I up 7 ms
    36, 200, 0, 7,
    # Z down
    56, 200, 0, 113,
    # Z up
    56, 200, 0, 50,
]


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


class KeyLayer:
    keyid = 0
    level = 0
    mode = 0
    hwcodes = []

    def __init__(self, data: List[int]) -> None:
        _cmd, level, keyid, mode = struct.unpack('!HBBH', bytes(data[:6]))
        self.level = level
        self.keyid = keyid
        self.mode = mode
        if mode == SINGLE_KEY:
            self.hwcodes = [data[6]]
        elif mode == COMBO_KEY:
            self.hwcodes = [code for code in data[6:] if code]

    def __str__(self) -> str:
        s = f"[{LEVEL2NAME[self.level]}] "
        if self.mode in (MACRO_DEF, SIM_HIT,):
            s += f'{MODE2NAME[self.mode]} '
        if len(self.hwcodes) == 1:
            s += HWCODE[self.hwcodes[0]]
        elif len(self.hwcodes) > 1:
            s += ' + '.join([HWCODE[code] for code in self.hwcodes])
        return s

    def __repr__(self) -> str:
        s = f"[#{self.keyid}:{LEVEL2NAME[self.level]}] "
        if self.mode in (MACRO_DEF, SIM_HIT,):
            s += f'{MODE2NAME[self.mode]} '
        if len(self.hwcodes) == 1:
            s += HWCODE[self.hwcodes[0]]
        elif len(self.hwcodes) > 1:
            s += ' + '.join([HWCODE[code] for code in self.hwcodes])
        return s


class PhysicalKey:
    '''
    Each Physical Key may has more than one key layer.
    Physical Key: 1. Normal
                  2. Right FN
                  3. Left FN
    '''

    def __init__(self, keyid=0, data=None, counter=0) -> None:
        self.keyid = keyid
        self.layers = {}
        self.counter = counter
        if data:
            self.read(data)

    def read(self, data: List[int]):
        keylayer = KeyLayer(data)
        self.keyid = keylayer.keyid
        self.layers[keylayer.level] = keylayer

    def __str__(self) -> str:
        s = f"#{self.keyid} {self.counter}"
        for layer in self.layers.values():
            s += f"\n\t{layer}"
        return s

    def __repr__(self) -> str:
        return f"#{self.keyid}:{self.counter} {self.layers}"


class Niz:
    def __init__(self, hiddev: HidDevice) -> None:
        self.device = hid.device()
        self.hiddev = hiddev
        self.device.open_path(hiddev.path)
        self.device.set_nonblocking(1)
        self.keys = [PhysicalKey(i) for i in range(85)]

    def version(self) -> str:
        '''
        read the version of keyboard
        '''
        self.send(Command.VERSION)
        data = self.read(64)
        ver_str = None
        if data:
            # 2 byte command, 62 bytes version string
            _, ver = struct.unpack('H62s', bytes(data))
            ver_str = ver.decode()
        return ver_str

    def read_keymap(self):
        '''
        mode:
        0 unset
        1 单键 00:01 接一个hwid
        2 组合键 00:02 hwid 列表
        3 宏定义 02:01 1 byte 播放次数,
        4 模拟击键 01:00 1byte delay, 1 byte 按键数量, hwid列表
        5 多媒体 00:01
        6 鼠标 00:01
        7 操控键 00:01
        8 电源键 00:01
        '''
        keymap = self.keys
        # nCCa2CC* -> uint16 BE,uint8,uint8,2 char,uint8,uint8*,
        self.send(Command.READ_KEY_MAP)
        while True:
            data = self.read(64)
            if not data or data[0] != 0:
                break
            key = keymap[data[3]]
            key.read(data)
        return keymap

    def read_counter(self):
        '''
        read press time of each key, key starts with 1 , 0 is not set
        '''
        self.send(Command.READ_COUNTER)
        counters = [0]
        idx = 0
        while True:
            data = self.read(64)
            if not data or data[1] != Command.READ_COUNTER:
                break
            # 2 byte command, 15*4 byte counter(uint32 LE), 1 byte unused
            _cmd, _,  *cnt, _ = struct.unpack('<Hb15Ib', bytes(data))
            counters.extend(cnt)
            for i, c in enumerate(cnt, start=1):
                if (idx*15+i) > 84:
                    break
                self.keys[idx*15+i].counter = c

            idx += 1

        return counters

    def send(self, cmd, data="") -> int:
        '''send cmd to keyboard,format: 1 byte 0, two byte command, 62 byte data
        `!bH62s`
        '''
        logger.debug(f'send:0x{cmd:02X},{data}')
        data = data.encode()
        # 1 byte 0, two byte command, 62 byte data
        buf = struct.pack('!bH62s', 0, cmd, data)
        written = self.device.write(buf)
        logger.debug(f"write({written}): {buf[1:].hex(':')}")

        return written

    def read(self, num=64, timeout=100) -> bytes:
        '''read data from hid device
        format: 2 bytes command, 62 bytes data'''
        data = None
        try:
            data = self.device.read(num, timeout)
            logger.debug(f"read ({len(data)}): {bytes(data).hex(':')}")
        except IOError as e:
            logger.error(e)
        return data

    def close(self):
        self.device.close()


def test():
    for i, name in enumerate(HWID2NAME):
        print(i, name)


if __name__ == '__main__':
    test()
