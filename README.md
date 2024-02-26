# ArduinoUNO-2D-plotter-LD293D
Arduino 2D plotter on LD293D (two-channel motor controller)

## Arduino UNO connection diagram with controller and motors:
<img src="https://github.com/DominikSty/ArduinoUNO-2D-plotter-LD293D/assets/101213292/ebf4764b-8a7a-4b11-9ce3-aa1c5e19dd20" width="800">

The version of Arduino used to create the project is the UNO board, with an Atmega 382p microcontroller, 32 kB Flash memory, 2 kB RAM, 14 digital inputs/outputs (6 of which have PWM channels) and 6 analog outputs. The motors responsible for the X and Y axis are SM15L stepper motors. The SG90 Servo motor will be responsible for controlling the Z axis. The Servo Motor SG90 can be controlled directly from the Arduino microcontroller, all you need is an appropriate library. However, a control system is needed to run and manage the speeds of the SM15L stepper motors. There are many microcircuits, however, L293D ICs were used for the project.

![animation](https://github.com/DominikSty/ArduinoUNO-2D-plotter-LD293D/assets/101213292/95991c58-9cec-4430-a732-509e0dcb2dbf)

The designed 3D model presented in the figure below shows the general appearance of the CNC plotter consisting of mechanical parts. The total size of the device is 168 x 190 x 183 mm and weighs 1076 grams, including consumables (pen) and complete electronics. The range of movements of the machinable surface is 40 x 32 mm. Communication between the Arduino microcontroller and the SM15L stepper motors is carried out using L293D ICs. It is a controller connected to an H-bridge, which allows for precise stepper control of the motors. It allows for separate bidirectional control of one of the engines. Two modules were used in the project, for the X axis and the Y axis. This system has an operating range of 5-7 V DC, so the power supply from Arduino is completely sufficient to operate these systems. During full operation, the structure reaches a relatively high temperature, bordering on the maximum temperature, which is why the project created a passive-active cooling system. This results in protection against overheating of the systems, which could lead to their degradation. The Servo motor responsible for the Z axis (raising and dropping the tool processing the material) does not need an additional system and is connected directly to Arduino. As the plotter is powered via USB, the current power available is limited. Therefore, more powerful motors could not be used in the project. According to the documentation, their operation is limited to 450 mA, and the cooling system (fan) consumes 15 mA. Thanks to this, Arduino has a large reserve of power for proper functioning.


<img src="https://github.com/DominikSty/ArduinoUNO-2D-plotter-LD293D/assets/101213292/986601e9-51ab-4543-a1d7-ff9edee24094" width="800">

<img src="https://github.com/DominikSty/ArduinoUNO-2D-plotter-LD293D/assets/101213292/b50b48b4-c654-4d60-9602-d216b0aae067" width="800">

<img src="https://github.com/DominikSty/ArduinoUNO-2D-plotter-LD293D/assets/101213292/3f76e6a2-6764-4c43-96f2-bd0ee4a5ef7c" width="800">


# TODO in near future:
- Create app to convert image to g-code
- implement functionality of g-code interpreter 
- curret step is 4*motor step - chagne
- modify function to draw line