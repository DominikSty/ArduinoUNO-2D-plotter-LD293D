import serial
import time

# Set SerialPort
port = '/dev/ttyACM2' 
baudrate = 9600

# Init connection
arduino = serial.Serial(port, baudrate, timeout=1)

# Wait for stabilization
time.sleep(2)

try:
    with open('commands.txt', 'r') as file:
        for line in file:
            komenda = line.strip()
            status = ''
            try:
                arduino.write(komenda.encode())
                print("Sent: ", komenda)
                
                while status != 'OK':
                    data = arduino.readline()
                    if data:
                        status = data.decode().rstrip()
                        print("Received: ", status)
                
                print("Command executed successfully.")
                print("--------------------")
            
            except Exception as e:
                print("An error occurred:", str(e))
                break  # Stop execution if there's an error

except KeyboardInterrupt:
    print("\nInterrupted by the user.")

finally:
    # Close the connection
    arduino.close()
