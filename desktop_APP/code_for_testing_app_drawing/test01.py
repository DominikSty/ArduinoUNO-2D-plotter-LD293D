import pygame
import os
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienie rozmiaru okna
WIDTH, HEIGHT = 55, 55
BG_COLOR = (255, 255, 255)  # Białe tło

# Stworzenie okna
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rysowanie linii")

# Zmienne pomocnicze
drawing = False
start_pos = None
end_pos = None
lines = []

# Główna pętla gry
running = True
while running:
    screen.fill(BG_COLOR)  # Wypełnienie ekranu białym kolorem

    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Lewy przycisk myszy
                start_pos = event.pos
                drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Lewy przycisk myszy
                end_pos = event.pos
                drawing = False
                if start_pos and end_pos:
                    lines.append((start_pos, end_pos))
                    start_pos = None
                    end_pos = None
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                end_pos = event.pos

    # Rysowanie linii
    for line in lines:
        pygame.draw.line(screen, (0, 0, 0), line[0], line[1], 2)

    # Rysowanie aktualnie rysowanej linii
    if start_pos and end_pos:
        pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)

    pygame.display.flip()

# Zapisywanie linii do pliku SVG
svg_content = '<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(WIDTH, HEIGHT)
for line in lines:
    # <path d="M x1,y1 L x2,y2" fill="none" stroke="black" />
    svg_content += '<path d="M {},{} L {},{}" fill="none" stroke="black" />\n'.format(line[0][0], line[0][1], line[1][0], line[1][1])
svg_content += '</svg>'

filename = 'picture.svg'
with open(filename, 'w') as f:
    f.write(svg_content)

print("Linie zostały zapisane w pliku:", filename)

pygame.quit()
sys.exit()
