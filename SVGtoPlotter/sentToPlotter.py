import serial
import time

# Set SerialPort
port = '/dev/ttyACM2' 
baudrate = 9600

# Init connection
arduino = serial.Serial(port, baudrate, timeout=1)

# Wait for stabilization
time.sleep(2)

# Variable definitions
status = ''
komenda = 'M(0,0);'
try:
    
    arduino.write(komenda.encode())
    print("send: ,",komenda)
        
    while status != 'OK':
        data = arduino.readline()
        if data:
            status = data.decode().rstrip()
            print("recive: ",status)
    print("recive: ",status)

    status = ''

    print("--------------------")

except KeyboardInterrupt:
    print("\nPrzerwano przez użytkownika.")

finally:
    # Zakończenie połączenia
    arduino.close()
