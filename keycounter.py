

from niz import *


if __name__ == '__main__':

    hiddev = choice_device(VID, PID_NIZ_84EC_S_BLE, [
                           ('product_string', 'Program')])
    if hiddev == None:
        exit(-1)
    niz = Niz(hiddev)
    ver = niz.version()
    print('Version:', ver)
    counters = niz.read_counter()
    key_counter = list(zip(range(len(HWID2NAME)), HWID2NAME, counters))
    key_counter.sort(key=lambda e: e[2])
    print('idx', 'id', 'name', 'cnt')
    print('-'*10)
    for idx, (key_id, key_name, cnt) in enumerate(reversed(key_counter), 1):
        print(idx, key_id, key_name, cnt)

    niz.close()
