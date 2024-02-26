import xml.etree.ElementTree as ET
import re

# Ścieżka do pliku SVG
svg_file_path = "my.svg"

# Parsowanie pliku SVG
tree = ET.parse(svg_file_path)
root = tree.getroot()

count = 0

instructions = []

# Przeszukiwanie elementów "path"
for path in root.iter('path'):
    # Pobieranie atrybutu "d" i wypisywanie
    d_value = path.attrib.get('d')
    count += 1
    
    # Znajdowanie wszystkich ciągów znaków z instrukcjami rysowania
    d_values_find = re.findall(r'[ML]\s*[\d.]+,\s*[\d.]+', d_value)
    
    # Iteracja po znalezionych dopasowaniach i ich wypisanie
    for d_value_find in d_values_find:
        # Zastąpienie spacji przecinkiem
        d_value_find = d_value_find.replace(' ', ',')
        
        # Ustawienie przecinka zaraz po literze 'M' lub 'L'
        d_value_find = re.sub(r'([ML])\s*', r'\1,', d_value_find)
        d_value_find = d_value_find.replace(',,', ',')
            
        # Podział ciągu na poszczególne elementy
        d_value_find_elements = d_value_find.split(',')
        instruction = d_value_find_elements[0].strip()
        x_coordinate = d_value_find_elements[1].strip()
        y_coordinate = d_value_find_elements[2].strip()
        instructions.append([instruction, x_coordinate, y_coordinate])

print(instructions)

matrix = [[' ' for _ in range(56)] for _ in range(56)]  # Inicjalizacja pustej macierzy
prev_instruction = None
prev_x = None
prev_y = None
    
# Przetwarzanie danych symboli i umieszczanie ich na macierzy
for symbol in instructions:
    instr = symbol[0]  # Litera instrukcji
    x = int(float(symbol[1]))  # Współrzędna x
    y = int(float(symbol[2]))  # Współrzędna y
    
    # Mapowanie współrzędnych na indeksy w macierzy
    row = y
    col = x
    
    # Umieszczanie symbolu na macierzy
    matrix[row][col] = instr
    
    # Jeśli instrukcja nie zaczyna się od "M" i istnieje poprzednia instrukcja, łączymy punkty
    if instr != "M" and prev_instruction is not None:
        print("penDOWN();")
        # Łączymy punkty symbolem '#'
        x1 = prev_x
        y1 = prev_y
        x2 = x
        y2 = y
        
        # Zaktualizowana część algorytmu Bresenhama
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = -1 if x1 > x2 else 1
        sy = -1 if y1 > y2 else 1
        err = dx - dy
        while True:  # Pętla będzie wykonywać się do momentu osiągnięcia punktu docelowego
            if 0 <= x1 < 56 and 0 <= y1 < 56:
                if x1 == x2 and y1 == y2:
                    matrix[y1][x1] = '#'  # Rysuj punkt docelowy
                    print(f"MoveTo({x1},{y1});")
                    break  # Zakończ pętlę po osiągnięciu punktu docelowego
                elif x1 == x2 or y1 == y2:
                    matrix[y1][x1] = '#'
                    print(f"MoveTo({x1},{y1});")
                else:
                    matrix[y1][x1] = '#'
                    print(f"MoveTo({x1},{y1});")
                    matrix[y1 + sy][x1] = '#'
                    print(f"MoveTo({x1},{y1 + sy});")
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        print("penUP();")    
    
    # Zapisujemy aktualną instrukcję i współrzędne jako poprzednie
    prev_instruction = instr
    prev_x = x
    prev_y = y

# Wyświetlanie macierzy
for row in matrix:
    print(' '.join(row))

