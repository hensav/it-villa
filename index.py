# mbw_pm.py - using pymodbus in serial mode to read and write modbus command.
# both for Windows and Linux environment. ITvilla 2014
# parameters for reading: mba regadd count port
# parameters for writing (1 or 2 consecutive registers): mba regadd hexdata port
''' Test program to communicate with a modbus slave using ModbusRTU protocol over serial or obver TCP '''

import sys
import traceback
# import pymodbus
from pymodbus import *
from pymodbus.transaction import *
from pymodbus.register_read_message import *

cmd = 0

argnum = len(sys.argv)
if argnum < 4:
    print('use arguments: mba regadd count_or_datahex host:port_or_port')
    exit()

mba = int(sys.argv[1])  # mb aadress
regaddr = int(sys.argv[2])  # address to read or hex data to write
port = sys.argv[4]
print('port', port)  # debug

if ":" in port:
    host = port.split(':')[0]
    port = int(port.split(':')[1])
    from pymodbus.client.sync import ModbusTcpClient as ModbusClient

    if (port < 10000 or port > 10003):  # tcp
        client = ModbusClient(host=host, port=port)
    else:  # xport or barionet
        client = ModbusClient(host=host, port=port, framer=ModbusRtuFramer)
else:
    from pymodbus.client.sync import ModbusSerialClient as ModbusClient  # using serial modbusRTU

    client = ModbusClient(method='rtu', stopbits=1, bytesize=8, parity='E', baudrate=19200, timeout=1, port=port)

if len(sys.argv[3]) == 4:  # write 1 register
    regcount = int(sys.argv[3], 16)  # data, hex kujul
    print('writing single register data', regcount)
    cmd = 6
elif len(sys.argv[3]) == 8:  # write 2 registers
    regcount = str(sys.argv[3])
    lodata = int(regcount[4:], 16)
    hidata = int(regcount[0:4], 16)
    print(hidata, hidata)
    cmd = 10
else:
    if len(sys.argv[3]) < 3:
        regcount = int(sys.argv[3])
        if argnum == 6:
            if sys.argv[5] == 'i':  # input register
                # print('reading',regcount,'input registers starting from',regaddr)
                cmd = 4
            elif sys.argv[5] == 'h':  # holding register
                # print('reading',regcount,'holding registers starting from',regaddr)
                cmd = 3
            elif sys.argv[5] == 'c':  # coils
                # print('reading',regcount,'coils starting from',regaddr)
                cmd = 1
            else:
                print('unknown parameter', sys.argv[5])
        else:
            # print('reading',regcount,'holding registers starting from',regaddr)
            cmd = 3
    else:
        print('invalid length ' + str(len(sys.argv[3])) + ' for parameter 3!')

output = ''

if cmd == 3:  # read holding registers
    result = client.read_holding_registers(address=regaddr, count=regcount, unit=mba)  # response=''  # pymodbus
    print(mba, regaddr, regcount, 'result', str(result.registers))

elif cmd == 4:  # lugemine, n registrit jarjest
    result = client.read_input_registers(address=regaddr, count=regcount, unit=mba)  # response=''  # pymodbus
    print(mba, regaddr, regcount, 'result', str(result.registers))

elif cmd == 1:  # lugemine, n coils jarjest
    print('mba', mba, 'regaddr', regaddr, 'regcount', regcount, 'cmd', cmd)  # debug

elif cmd == 6:  # kirjutamine, 1 register
    print('mba', mba, 'regaddr', regaddr, 'data', regcount, 'cmd', cmd)  # debug
    client.write_register(address=regaddr, value=regcount, unit=mba)  # only one regiter to write here
    print('ok')

elif cmd == 10:  # kirjutamine, 2 registrit
    print('mba', mba, 'regaddr', regaddr, 'data', regcount, 'cmd', cmd)  # debug
    client.write_registers(address=regaddr, values=[hidata, lodata], unit=mba)  # 2 registers to write here
    print('ok')
else:
    print('failure, unknown function code', cmd)
