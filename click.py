import pygame
import numpy as np

SCREEN_SIZE = (800, 800)

center_x = 150
center_y = 100
edge_length = 80

# Define some colors
BLUE = (0, 0, 255)

BROWN = (165, 42, 42)  # brick -- 3
GREEN = (0, 255, 0)  # pasture -- 4
GRAY = (128, 128, 128)  # ore -- 3
GOLD = (255, 215, 0)  # field -- 4
DARK_GREEN = (0, 128, 0)  # trees -- 4
DESSERT = (204, 173, 96)  # dessert -- 1

OLIVE = (128, 128, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
TEAL = (0, 128, 128)
LIGHT_YELLOW = (255, 255, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SILVER = (192, 192, 192)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
NAVY = (0, 0, 128)
INDIGO = (75, 0, 130)
VIOLET = (138, 43, 226)
FUCHSIA = (255, 0, 255)
LIME = (0, 255, 0)
AQUA = (0, 255, 255)


def offset_hex_coordinates_diamond(
    center_x, center_y, edge_length, max_row_width=5, min_row_width=3
):
    tiles = []
    for row in range(max_row_width * 2 - min_row_width * 2 + 1):
        if row <= max_row_width - min_row_width:
            num_tiles = min_row_width + row
        else:
            num_tiles = 2 * max_row_width - row - min_row_width

        for col in range(num_tiles):
            tiles.append(
                [
                    center_x + edge_length * 1.5 * row,
                    center_y
                    + edge_length
                    * np.sqrt(3)
                    * (col + (max_row_width - num_tiles) * 0.5),
                ]
            )
    return tiles


def lighter_color(color, percent):
    r, g, b = color
    new_r = int(min(255, r * percent))
    new_g = int(min(255, g * percent))
    new_b = int(min(255, b * percent))
    return (new_r, new_g, new_b)


def hexagon_coordinates(center_x, center_y, edge_length):
    angle = np.pi * 2 / 6  # Angle between each vertex (360 degrees / 6 sides)
    coordinates = []
    for i in range(6):
        x = center_x + edge_length * np.cos(i * angle)
        y = center_y + edge_length * np.sin(i * angle)
        coordinates.append((x, y))
    return coordinates


def intersects(p, p1, p2):
    return (
        p1[0] < p[0] < p2[0]
        and (p2[0] - p[0]) * p1[1] + (p[0] - p1[0]) * p2[1] > (p2[0] - p1[0]) * p[1]
    )


def is_point_inside_polygon(point, poly):
    intersections = 0
    for i in range(len(poly)):
        p1, p2 = poly[i], poly[(i + 1) % len(poly)]
        if intersects(point, p1, p2):
            intersections += 1
        elif intersects(point, p2, p1):
            intersections += 1
    return intersections % 2 == 1


def draw_button(poly, screen, is_hovered, color):
    # Change button color based on hover state
    button_color = color if is_hovered else lighter_color(color, 0.8)

    # Draw the button polygon
    pygame.draw.polygon(screen, button_color, poly)
    pygame.draw.polygon(screen, (0, 0, 0), poly, width=3)

    # Add some text if needed (optional)
    font = pygame.font.Font(None, 22)
    text_surface = font.render("Click me!", True, BLACK)
    text_rect = text_surface.get_rect(
        center=[np.mean([x[0] for x in poly]), np.mean([x[1] for x in poly])]
    )
    screen.blit(text_surface, text_rect)


hex_tiles = offset_hex_coordinates_diamond(center_x, center_y, edge_length)
tile_types = (
    [BROWN] * 3
    + [GREEN] * 4
    + [GRAY] * 3
    + [GOLD] * 4
    + [DARK_GREEN] * 4
    + [DESSERT] * 1
)
np.random.shuffle(tile_types)

button_points = [
    hexagon_coordinates(center_x=center_x, center_y=center_y, edge_length=edge_length)
    for center_x, center_y in hex_tiles
]


pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill(WHITE)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        mouse_pos = pygame.mouse.get_pos()

        for i, poly in enumerate(button_points):
            color = tile_types[i]
            is_hovered = is_point_inside_polygon(mouse_pos, poly)
            draw_button(poly, screen, is_hovered, color)

            if event.type == pygame.MOUSEBUTTONDOWN and is_hovered:
                print(f"Button {i} clicked!")

    pygame.display.flip()

pygame.quit()
