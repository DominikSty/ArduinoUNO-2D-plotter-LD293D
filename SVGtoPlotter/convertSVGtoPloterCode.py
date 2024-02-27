import xml.etree.ElementTree as ET
import re

# Path to the SVG file
svg_file_path = "my.svg"
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

print(instructions)

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
        print("penDOWN;")
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
                    print(f'M({y1},{x1});')
                    lines.append(f'M({y1},{x1});')
                    break  # End the loop when you reach your destination point
                elif x1 == x2 or y1 == y2:
                    matrix[y1][x1] = '#'
                    print(f'M({y1},{x1});')
                    lines.append(f'M({y1},{x1});')
                else:
                    matrix[y1][x1] = '#'
                    print(f'M({y1},{x1});')
                    lines.append(f'M({y1},{x1});')
                    matrix[y1 + sy][x1] = '#'
                    print(f'M({y1 + sy},{x1});')
                    lines.append(f'M({y1 + sy},{x1});')
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        print("penUP;")
        lines.append("penUP;")
    
    # Save the current instruction and coordinates as previous ones
    prev_instruction = instr
    prev_x = x
    prev_y = y

# Matrix display
for row in matrix:
    print(' '.join(row))

lines.append("M(0,0);") # MoveTo(0,0) - start position



print(lines)
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
# Displaying the result
# print(wynik)


write_to_file(filename, lines)


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




