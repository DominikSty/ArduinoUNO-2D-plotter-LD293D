import serial
import time

# Set SerialPort
port = '/dev/ttyACM0' 
baudrate = 9600

# Init connection
arduino = serial.Serial(port, baudrate, timeout=1)

# Wait for stabilization
time.sleep(2)

try:
    with open('commands.txt', 'r') as file:
        for line in file:
            command = line.strip()  # Read the next line from the file and remove whitespace from the beginning and end
            arduino.write(command.encode() + b';')  # Send the command with a line break (;)
            print("Sent: ", command)
            
            status = ''
            while status != 'OK':
                data = arduino.readline()
                if data:
                    status = data.decode().rstrip()
                    print("Received: ", status)
        
        print("All commands executed successfully.")
        print("--------------------")

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the connection
    arduino.close()
