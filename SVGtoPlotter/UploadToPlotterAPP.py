import serial.tools.list_ports
import xml.etree.ElementTree as ET
import serial
import time
import re
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf


class ArduinoDeviceList(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Arduino Device List")
        self.set_default_size(550, 480)
        self.set_resizable(False)
        self.svgPath = None
        self.arduinoPort = None

        # Layout
        fixed = Gtk.Fixed()
        self.add(fixed)

        # Label info for comboBox
        self.label01 = Gtk.Label(label="Select the Plotter device")
        fixed.put(self.label01, 5, 5)

        # Label error messane for comboBox
        self.label01 = Gtk.Label(label="No USB/ACM devices available.\nClick Refresh to reload")
        fixed.put(self.label01, 5, 30)

        # Combo Box for Device List
        self.device_combo = Gtk.ComboBoxText()
        self.device_combo.set_size_request(200, 30)
        fixed.put(self.device_combo, 5, 30)

        # Refresh Button
        self.refresh_button = Gtk.Button(label="Refresh")
        self.refresh_button.connect("clicked", self.on_refresh_clicked)
        self.refresh_button.set_size_request(100, 30)
        fixed.put(self.refresh_button, 210, 30)

        # Connect Button
        self.connect_button = Gtk.Button(label="Connect")
        self.connect_button.connect("clicked", self.connect_to_plotter)
        self.connect_button.set_size_request(100, 30)
        fixed.put(self.connect_button, 5, 70)

        # Disconnect Button
        self.disconnect_button = Gtk.Button(label="Disconnect")
        self.disconnect_button.set_sensitive(False)
        self.disconnect_button.connect("clicked", self.disconnect_to_plotter)
        self.disconnect_button.set_size_request(100, 30)
        fixed.put(self.disconnect_button, 110, 70)

        # Load SVG Button
        self.loadSVG_button = Gtk.Button(label="Load SVG")
        self.loadSVG_button.connect("clicked", self.on_choose_file_clicked)
        self.loadSVG_button.set_size_request(100, 30)
        fixed.put(self.loadSVG_button, 5, 140)

        # Drawing SVG area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(280, 280)
        fixed.put(self.drawing_area, 20, 190)
        self.current_pixbuf = None

        # Upload to Plotter Button
        self.uploadSVGtoPlotter_button = Gtk.Button(label="Start PRINT")
        self.uploadSVGtoPlotter_button.connect("clicked", self.uploadSVGtoPlotter)
        self.uploadSVGtoPlotter_button.set_size_request(100, 30)
        fixed.put(self.uploadSVGtoPlotter_button, 110, 140)

        # View Command Area
        self.textview = Gtk.TextView()
        self.textview.set_editable(False)  # Ustawienie textview jako niemożliwego do edycji
        self.scrollable = Gtk.ScrolledWindow()
        self.scrollable.set_min_content_height(470)
        self.scrollable.set_min_content_width(220)
        self.scrollable.add(self.textview)
        fixed.put(self.scrollable, 320, 5)

        # Connect signals "show" with method start_actions()
        self.connect("show", self.start_actions)  
        self.start_actions()

    def start_actions(self, widget=None):
        self.label01.hide()
        self.disconnect_button.set_sensitive(False)
        self.connect_button.set_sensitive(False)
        self.uploadSVGtoPlotter_button.set_sensitive(False)
        self.refresh_device_list()
    

    def uploadSVGtoPlotter(self, button):
        addTextLine = self.textview.get_buffer()
        addTextLine.insert_at_cursor("Converting image...\n")
        #--------------------------------------------------------------#
        #                        CONVERT TIME                          #
        # -------------------------------------------------------------#
        
        # Path to the SVG file
        svg_file_path = self.svgPath
        commands_count = 20 # default 5

        # Parsing an SVG file
        tree = ET.parse(svg_file_path)
        root = tree.getroot()

        count = 0

        instructions = []


        def write_to_file(filename, commands):
            try:
                # Opening a file in save mode (creates a new file or overwrites an existing one)
                with open(filename, 'w') as file:
                    # Saving subsequent lines to the file
                    for command in commands:
                        file.write(command)
            except Exception as e:
                print("An error occurred while writing to the file:", str(e))

        filename = 'commands.txt'
        lines = []

        # Searching for "path" elements
        for path in root.iter('path'):
            # Getting the 'd' attribute and printing it out
            d_value = path.attrib.get('d')
            count += 1
            
            # Find all strings with drawing instructions
            d_values_find = re.findall(r'[ML]\s*[\d.]+,\s*[\d.]+', d_value)
            
            # Iterate through the matches found and write them out
            for d_value_find in d_values_find:
                # Replacing a space with a comma
                d_value_find = d_value_find.replace(' ', ',')
                
                # Setting a comma right after the letter 'M' or 'L'
                d_value_find = re.sub(r'([ML])\s*', r'\1,', d_value_find)
                d_value_find = d_value_find.replace(',,', ',')
                    
                # Division of the sequence into individual elements
                d_value_find_elements = d_value_find.split(',')
                instruction = d_value_find_elements[0].strip()
                x_coordinate = d_value_find_elements[1].strip()
                y_coordinate = d_value_find_elements[2].strip()
                instructions.append([instruction, x_coordinate, y_coordinate])

        print("Instructions:\n", instructions)

        matrix = [[' ' for _ in range(56)] for _ in range(56)]  # Initializing an empty matrix
        prev_instruction = None
        prev_x = None
        prev_y = None

        # Processing symbol data and placing it on a matrix
        for symbol in instructions:
            instr = symbol[0]  # Instruction letter
            x = int(float(symbol[1]))  # x coordinate
            y = int(float(symbol[2]))  # y coordinate
            
            # Mapping coordinates to indexes in a matrix
            row = y
            col = x
            
            # Placing a symbol on a matrix
            matrix[row][col] = instr
            
            # If the statement does not start with "M" and there is a previous statement, we combine the dots
            if instr != "M" and prev_instruction is not None:
                # print("penDOWN;")
                lines.append("penDOWN;")
                # We connect the points with the '#' symbol
                x1 = prev_x
                y1 = prev_y
                x2 = x
                y2 = y
                
                # Updated part of Bresenham's algorithm
                dx = abs(x2 - x1)
                dy = abs(y2 - y1)
                sx = -1 if x1 > x2 else 1
                sy = -1 if y1 > y2 else 1
                err = dx - dy
                while True:  # The loop will continue until the destination point is reached
                    if 0 <= x1 < 56 and 0 <= y1 < 56:
                        if x1 == x2 and y1 == y2:
                            matrix[y1][x1] = '#'  # Draw the target point
                            # print(f'M({y1},{x1});')
                            lines.append(f'M({y1},{x1});')
                            break  # End the loop when you reach your destination point
                        elif x1 == x2 or y1 == y2:
                            matrix[y1][x1] = '#'
                            # print(f'M({y1},{x1});')
                            lines.append(f'M({y1},{x1});')
                        else:
                            matrix[y1][x1] = '#'
                            # print(f'M({y1},{x1});')
                            lines.append(f'M({y1},{x1});')
                            matrix[y1 + sy][x1] = '#'
                            # print(f'M({y1 + sy},{x1});')
                            lines.append(f'M({y1 + sy},{x1});')
                    e2 = 2 * err
                    if e2 > -dy:
                        err -= dy
                        x1 += sx
                    if e2 < dx:
                        err += dx
                        y1 += sy
                # print("penUP;")
                lines.append("penUP;")
            
            # Save the current instruction and coordinates as previous ones
            prev_instruction = instr
            prev_x = x
            prev_y = y

        # Matrix display
        print("\nView picture:\n")
        for row in matrix:
            print(' '.join(row))

        lines.append("M(0,0);") # MoveTo(0,0) - start position


        # Stores the resulting instructions
        change_list = []

        # Iterate through the elements of the list except the last element
        i = 0
        while i < len(lines) - 1:
            # If the current statement is "penDOWN;" and the previous instruction is "penUP;"
            if lines[i] == "penDOWN;":
                # Move "penDOWN;" with the next instruction
                change_list.append(lines[i + 1])
                change_list.append(lines[i])
                i += 2
            else:
                change_list.append(lines[i])
                i += 1

        # Add the last item of the list to the result
        change_list.append(lines[-1])
        lines = change_list

        write_to_file(filename, lines)


        print("Plotter code:\n", lines)

        # Division into lines after X commands

        # Opening a file with saved lines
        with open(filename, 'r') as file:
            data = file.read()

        # Division of data into lines
        lines = data.split(';')

        # Opening a file in save mode
        with open(filename, 'w') as file:
            # Writing consecutive lines to the file, adding a newline after every 20 ';' characters
            for i, line in enumerate(lines):
                file.write(line + ';')
                # Adding a newline after every X ';'
                if (i + 1) % commands_count == 0:
                    file.write('\n')
        
        addTextLine.insert_at_cursor("Converting done.\n")

        #--------------------------------------------------------------#
        #                         UPLOAD TIME                          #
        # -------------------------------------------------------------#

        addTextLine.insert_at_cursor("Start printing...\n")

        # Set SerialPort
        port = self.arduinoPort
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

        #--------------------------------------------------------------#
        #                           END TIME                           #
        # -------------------------------------------------------------#
        addTextLine.insert_at_cursor("Printing done.\n")
        
    def on_choose_file_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Please choose an SVG file", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        filter_svg = Gtk.FileFilter()
        filter_svg.set_name("SVG files")
        filter_svg.add_mime_type("image/svg+xml")
        dialog.add_filter(filter_svg)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            svg_path = dialog.get_filename()
            self.svgPath = svg_path
            self.load_svg(svg_path)
        dialog.destroy()

    def load_svg(self, file_path):
        try:
            # Load SVG file as a pixbuf
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(file_path)
            # Scale the pixbuf 5 times bigger
            scaled_pixbuf = pixbuf.scale_simple(
                pixbuf.get_width() * 5,
                pixbuf.get_height() * 5,
                GdkPixbuf.InterpType.BILINEAR
            )
            # Clear the drawing area
            self.drawing_area.queue_draw()
            # Store the current pixbuf
            self.current_pixbuf = scaled_pixbuf
            self.drawing_area.connect("draw", self.on_draw)
            self.uploadSVGtoPlotter_button.set_sensitive(True)
        except Exception as e:
            print("Error loading SVG:", e)

    def on_draw(self, widget, context):
        if self.current_pixbuf is not None:
            Gdk.cairo_set_source_pixbuf(context, self.current_pixbuf, 0, 0)
            context.paint()

    def refresh_device_list(self):
        self.device_combo.remove_all()
        ports = serial.tools.list_ports.comports()
        usb_devices = [port.device for port in ports if 'USB' in port.description or 'ACM' in port.description]
        if usb_devices:
            for device in usb_devices:
                self.device_combo.append_text(device)
            self.label01.hide()
            self.device_combo.show()
            self.connect_button.set_sensitive(True)
        else:
            self.device_combo.hide()
            self.label01.show()
            self.connect_button.set_sensitive(False)

    def on_refresh_clicked(self, button):
        self.refresh_device_list()

    def connect_to_plotter(self, button):
        selected_value = self.device_combo.get_active_text()
        self.arduinoPort = selected_value
        addTextLine = self.textview.get_buffer()
        if selected_value is not None:
            connectionIsGood = False
            addTextLine.insert_at_cursor("Connecting to Plotter...\n")
            # Sending stest command to check connection
            # Init connection
            arduino = serial.Serial(self.arduinoPort, 9600, timeout=1)
            # Wait for stabilization
            time.sleep(2)
            try:
                command = 'M(0,0);'
                arduino.write(command.encode() + b';')  # Send the command with a line break (;)
                print("Sent: ", command) 
                status = ''
                while status != 'OK':
                    data = arduino.readline()
                    if data:
                        status = data.decode().rstrip()
                        print("Received: ", status) 
                addTextLine.insert_at_cursor("Connecting succesfully.\n")
                connectionIsGood = True

            except Exception as e:
                addTextLine.insert_at_cursor(f'An error occurred:{str(e)}\n')
                print("An error occurred:", str(e))

            finally:
                # Close the connection
                arduino.close()

            if connectionIsGood:
                self.device_combo.set_sensitive(False)
                self.refresh_button.set_sensitive(False)
                self.connect_button.set_sensitive(False)
                self.disconnect_button.set_sensitive(True)
            connectionIsGood = False
        else:
            addTextLine.insert_at_cursor(f'Error: Select the port from list!\n')
        


    def disconnect_to_plotter(self, button):
        self.device_combo.set_sensitive(True)
        self.refresh_button.set_sensitive(True)
        self.connect_button.set_sensitive(True)
        self.disconnect_button.set_sensitive(False)
        addTextLine = self.textview.get_buffer()
        addTextLine.insert_at_cursor("Disconnected from Plotter.\n")


win = ArduinoDeviceList()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
