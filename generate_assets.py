"""
Plants vs. Zombies - High-Quality Asset Generator.
Creates complete, crisp, cartoon-style PNG sprites, backgrounds,
and UI graphics for all game entities and modes.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def draw_gradient_rect(
    draw: ImageDraw.ImageDraw,
    rect: tuple[int, int, int, int],
    c_top: tuple[int, int, int],
    c_bottom: tuple[int, int, int],
):
    x0, y0, x1, y1 = rect
    height = max(1, y1 - y0)
    for y in range(y0, y1):
        ratio = (y - y0) / height
        r = int(c_top[0] * (1 - ratio) + c_bottom[0] * ratio)
        g = int(c_top[1] * (1 - ratio) + c_bottom[1] * ratio)
        b = int(c_top[2] * (1 - ratio) + c_bottom[2] * ratio)
        draw.line([(x0, y), (x1, y)], fill=(r, g, b, 255))


def draw_smooth_circle(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float, float, float],
    fill: tuple,
    outline: tuple | None = None,
    width: int = 1,
):
    draw.ellipse(xy, fill=fill, outline=outline, width=width)


# -------------------------------------------------------------
# BACKGROUNDS
# -------------------------------------------------------------
def generate_lawn_day():
    img = Image.new("RGBA", (1280, 720), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # Sky / upper background
    draw_gradient_rect(draw, (0, 0, 1280, 140), (95, 175, 235), (170, 218, 255))

    # Sun in the distance
    draw.ellipse((1080, 30, 1180, 130), fill=(255, 235, 120, 255))
    draw.ellipse((1090, 40, 1170, 120), fill=(255, 245, 170, 255))

    # Distant clouds
    for cx, cy, rad in [(200, 50, 40), (240, 45, 55), (280, 55, 45), (650, 70, 35), (690, 60, 48)]:
        draw.ellipse((cx - rad, cy - rad // 2, cx + rad, cy + rad // 2), fill=(255, 255, 255, 210))

    # Garden Fence
    fence_y = 120
    for fx in range(0, 1280, 32):
        draw.polygon([(fx, fence_y + 20), (fx + 14, fence_y), (fx + 28, fence_y + 20), (fx + 28, fence_y + 50), (fx, fence_y + 50)],
                     fill=(235, 230, 215, 255), outline=(160, 150, 130, 255))
    draw.rectangle((0, fence_y + 25, 1280, fence_y + 35), fill=(210, 200, 180, 255), outline=(140, 130, 110, 255))

    # House / Porch area on the left (x: 0 .. 220)
    draw_gradient_rect(draw, (0, 140, 220, 720), (145, 115, 80), (105, 80, 55))
    # Wooden floor planks
    for py in range(140, 720, 24):
        draw.line([(0, py), (220, py)], fill=(75, 55, 35, 255), width=2)
    for px in [70, 145]:
        draw.line([(px, 140), (px, 720)], fill=(90, 68, 45, 255), width=1)
    # Porch stone step edge
    draw.rectangle((216, 140, 224, 720), fill=(185, 180, 170, 255), outline=(120, 115, 110, 255))

    # Right side pavement / street edge (x: 1160 .. 1280)
    draw_gradient_rect(draw, (1160, 140, 1280, 720), (160, 160, 160), (120, 120, 120))
    for sy in range(140, 720, 60):
        draw.line([(1160, sy), (1280, sy)], fill=(90, 90, 90, 255), width=2)

    # 5 rows x 9 columns lawn grid
    # Grid x: 224 to 1160 (width 936, 104 px per col)
    # Grid y: 150 to 710 (height 560, 112 px per row)
    row_h = 112
    col_w = 104
    start_x = 224
    start_y = 150

    grass_light = (112, 192, 54)
    grass_dark = (92, 168, 42)

    for r in range(5):
        for c in range(9):
            x0 = start_x + c * col_w
            y0 = start_y + r * row_h
            x1 = x0 + col_w
            y1 = y0 + row_h
            color = grass_light if (r + c) % 2 == 0 else grass_dark
            draw.rectangle((x0, y0, x1, y1), fill=color)
            # subtle border highlight
            draw.rectangle((x0, y0, x1, y1), outline=(color[0] - 15, color[1] - 15, color[2] - 15, 160), width=1)

            # Tiny grass blade tufts
            for gx, gy in [(x0 + 15, y0 + 20), (x0 + 75, y0 + 60), (x0 + 45, y0 + 90)]:
                draw.line([(gx, gy), (gx - 2, gy - 6)], fill=(140, 220, 80, 180), width=2)
                draw.line([(gx, gy), (gx + 3, gy - 7)], fill=(155, 235, 95, 180), width=2)

    # Top & bottom border bars
    draw.rectangle((0, 712, 1280, 720), fill=(55, 100, 30, 255))
    img.save("assets/backgrounds/lawn_day.png")


def generate_lawn_night():
    img = Image.new("RGBA", (1280, 720), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # Night sky
    draw_gradient_rect(draw, (0, 0, 1280, 140), (15, 20, 45), (35, 45, 80))

    # Crescent Moon
    draw.ellipse((1080, 30, 1170, 120), fill=(245, 245, 220, 255))
    draw.ellipse((1105, 25, 1185, 115), fill=(25, 35, 65, 255))

    # Stars
    star_coords = [(120, 30), (250, 70), (410, 40), (580, 80), (740, 35), (890, 60), (980, 25)]
    for sx, sy in star_coords:
        draw.ellipse((sx - 2, sy - 2, sx + 2, sy + 2), fill=(255, 255, 230, 230))

    # Spooky silhouettes of fence
    fence_y = 120
    for fx in range(0, 1280, 32):
        draw.polygon([(fx, fence_y + 20), (fx + 14, fence_y), (fx + 28, fence_y + 20), (fx + 28, fence_y + 50), (fx, fence_y + 50)],
                     fill=(45, 50, 65, 255), outline=(25, 30, 40, 255))

    # Left porch
    draw_gradient_rect(draw, (0, 140, 220, 720), (45, 40, 50), (30, 25, 35))
    for py in range(140, 720, 24):
        draw.line([(0, py), (220, py)], fill=(20, 18, 25, 255), width=2)
    draw.rectangle((216, 140, 224, 720), fill=(65, 65, 75, 255))

    # Right pavement
    draw_gradient_rect(draw, (1160, 140, 1280, 720), (50, 55, 65), (35, 40, 50))

    # 5x9 Lawn at night (cool blueish-green)
    start_x, start_y = 224, 150
    row_h, col_w = 112, 104
    grass_light = (38, 75, 58)
    grass_dark = (28, 60, 48)

    for r in range(5):
        for c in range(9):
            x0 = start_x + c * col_w
            y0 = start_y + r * row_h
            x1 = x0 + col_w
            y1 = y0 + row_h
            color = grass_light if (r + c) % 2 == 0 else grass_dark
            draw.rectangle((x0, y0, x1, y1), fill=color)
            draw.rectangle((x0, y0, x1, y1), outline=(color[0] - 10, color[1] - 10, color[2] - 10, 160), width=1)

    # Fireflies glowing dots
    for fx, fy in [(300, 220), (550, 380), (820, 280), (700, 590), (440, 490), (950, 440)]:
        draw.ellipse((fx - 5, fy - 5, fx + 5, fy + 5), fill=(160, 255, 120, 80))
        draw.ellipse((fx - 2, fy - 2, fx + 2, fy + 2), fill=(230, 255, 160, 255))

    img.save("assets/backgrounds/lawn_night.png")


def generate_lawn_bowling():
    # Day lawn base with bowling red foul line
    generate_lawn_day()
    img = Image.open("assets/backgrounds/lawn_day.png")
    draw = ImageDraw.Draw(img)

    # Bowling red line at column 3 (x = 224 + 3 * 104 = 536)
    rx = 536
    draw.line([(rx, 150), (rx, 710)], fill=(230, 40, 40, 255), width=6)
    # Warning dashed pattern
    for y in range(150, 710, 20):
        draw.line([(rx - 3, y), (rx + 3, y + 10)], fill=(255, 255, 255, 230), width=3)

    # Top conveyor belt header placeholder
    draw.rectangle((0, 0, 1280, 140), fill=(40, 40, 45, 230), outline=(20, 20, 25, 255), width=2)
    # Rollers on conveyor belt
    for cx in range(40, 1240, 36):
        draw.line([(cx, 20), (cx, 120)], fill=(80, 85, 95, 255), width=3)
        draw.ellipse((cx - 3, 65, cx + 3, 75), fill=(130, 140, 155, 255))

    img.save("assets/backgrounds/lawn_bowling.png")


def generate_menu_bg():
    img = Image.new("RGBA", (1280, 720), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # Majestic twilight / evening gradient sky
    draw_gradient_rect(draw, (0, 0, 1280, 450), (45, 80, 140), (160, 120, 170))

    # Distant rolling hills
    draw.pieslice((-200, 220, 800, 750), 180, 360, fill=(35, 85, 45, 255))
    draw.pieslice((500, 260, 1500, 800), 180, 360, fill=(45, 110, 55, 255))
    draw.pieslice((150, 350, 1250, 950), 180, 360, fill=(65, 145, 50, 255))

    # Fore lawn
    draw_gradient_rect(draw, (0, 520, 1280, 720), (75, 155, 45), (45, 95, 25))

    # Giant gravestone on the right
    gx, gy = 960, 280
    draw.polygon([(gx, gy + 340), (gx, gy + 100), (gx + 60, gy), (gx + 180, gy), (gx + 240, gy + 100), (gx + 240, gy + 340)],
                 fill=(135, 135, 145, 255), outline=(75, 75, 85, 255), width=4)
    # Crack in stone
    draw.line([(gx + 120, gy + 40), (gx + 100, gy + 90), (gx + 130, gy + 140), (gx + 110, gy + 200)], fill=(60, 60, 70, 255), width=3)

    img.save("assets/backgrounds/menu_bg.png")


# -------------------------------------------------------------
# PLANTS SPRITES (Transparent RGBA 96x96)
# -------------------------------------------------------------
def generate_peashooter():
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Base stem & ground leaves
    draw.ellipse((28, 74, 52, 88), fill=(40, 140, 35, 255), outline=(20, 80, 15, 255), width=2)
    draw.ellipse((44, 74, 68, 88), fill=(50, 160, 40, 255), outline=(20, 80, 15, 255), width=2)
    # Stem
    draw.line([(48, 55), (46, 78)], fill=(45, 150, 35, 255), width=9)
    draw.line([(48, 55), (46, 78)], fill=(30, 110, 25, 255), width=2)

    # Leaf on stem
    draw.polygon([(46, 65), (32, 60), (44, 72)], fill=(55, 175, 45, 255), outline=(25, 95, 20, 255))

    # Round Head
    hx, hy, hr = 46, 42, 24
    draw.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=(105, 210, 45, 255), outline=(30, 110, 25, 255), width=3)
    # Head highlight
    draw.ellipse((hx - hr + 7, hy - hr + 6, hx - 4, hy - 4), fill=(160, 245, 90, 255))

    # Snout / Cannon tube (facing right)
    draw.polygon([(hx + 12, hy - 11), (hx + 38, hy - 16), (hx + 42, hy + 12), (hx + 14, hy + 11)],
                 fill=(95, 195, 40, 255), outline=(30, 110, 25, 255), width=3)
    # Snout hole
    draw.ellipse((hx + 35, hy - 16, hx + 44, hy + 12), fill=(25, 75, 20, 255), outline=(15, 55, 15, 255), width=2)

    # Big Expressive Eyes
    # Right eye
    draw.ellipse((hx + 2, hy - 14, hx + 18, hy + 4), fill=(255, 255, 255, 255), outline=(20, 80, 20, 255), width=2)
    draw.ellipse((hx + 8, hy - 10, hx + 16, hy), fill=(20, 20, 20, 255))
    draw.ellipse((hx + 12, hy - 8, hx + 15, hy - 4), fill=(255, 255, 255, 255))

    # Left eye (partly behind)
    draw.ellipse((hx - 14, hy - 14, hx, hy + 3), fill=(255, 255, 255, 255), outline=(20, 80, 20, 255), width=2)
    draw.ellipse((hx - 8, hy - 10, hx - 1, hy), fill=(20, 20, 20, 255))
    draw.ellipse((hx - 4, hy - 8, hx - 1, hy - 4), fill=(255, 255, 255, 255))

    img.save("assets/plants/peashooter.png")


def generate_snow_pea():
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Base stem & frost leaves
    draw.ellipse((28, 74, 52, 88), fill=(40, 120, 150, 255), outline=(15, 60, 90, 255), width=2)
    draw.ellipse((44, 74, 68, 88), fill=(55, 145, 180, 255), outline=(15, 60, 90, 255), width=2)
    # Stem
    draw.line([(48, 55), (46, 78)], fill=(45, 130, 160, 255), width=9)

    # Icy spikes at back of head
    for sp_x, sp_y in [(24, 28), (18, 40), (22, 52)]:
        draw.polygon([(sp_x + 14, sp_y), (sp_x - 6, sp_y - 4), (sp_x + 4, sp_y + 10)],
                     fill=(180, 240, 255, 255), outline=(60, 150, 210, 255), width=2)

    # Round Frost Head
    hx, hy, hr = 46, 42, 24
    draw.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=(80, 195, 235, 255), outline=(25, 100, 160, 255), width=3)
    # Head highlight
    draw.ellipse((hx - hr + 7, hy - hr + 6, hx - 4, hy - 4), fill=(200, 250, 255, 255))

    # Snout
    draw.polygon([(hx + 12, hy - 11), (hx + 38, hy - 16), (hx + 42, hy + 12), (hx + 14, hy + 11)],
                 fill=(70, 175, 220, 255), outline=(25, 100, 160, 255), width=3)
    draw.ellipse((hx + 35, hy - 16, hx + 44, hy + 12), fill=(20, 60, 110, 255), outline=(10, 35, 70, 255), width=2)

    # Big Eyes
    draw.ellipse((hx + 2, hy - 14, hx + 18, hy + 4), fill=(255, 255, 255, 255), outline=(20, 70, 120, 255), width=2)
    draw.ellipse((hx + 8, hy - 10, hx + 16, hy), fill=(10, 30, 60, 255))
    draw.ellipse((hx + 12, hy - 8, hx + 15, hy - 4), fill=(255, 255, 255, 255))

    draw.ellipse((hx - 14, hy - 14, hx, hy + 3), fill=(255, 255, 255, 255), outline=(20, 70, 120, 255), width=2)
    draw.ellipse((hx - 8, hy - 10, hx - 1, hy), fill=(10, 30, 60, 255))
    draw.ellipse((hx - 4, hy - 8, hx - 1, hy - 4), fill=(255, 255, 255, 255))

    img.save("assets/plants/snow_pea.png")


def generate_sunflower():
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Base stem & leaves
    draw.ellipse((24, 76, 50, 88), fill=(40, 150, 35, 255), outline=(20, 80, 15, 255), width=2)
    draw.ellipse((46, 76, 72, 88), fill=(50, 165, 45, 255), outline=(20, 80, 15, 255), width=2)
    draw.line([(48, 52), (48, 80)], fill=(45, 155, 35, 255), width=9)

    cx, cy = 48, 42
    # 12 bright yellow petals
    num_petals = 12
    for i in range(num_petals):
        angle = i * (2 * math.pi / num_petals)
        px = cx + math.cos(angle) * 29
        py = cy + math.sin(angle) * 29
        # Draw petal teardrop/ellipse
        draw.ellipse((px - 9, py - 9, px + 9, py + 9), fill=(255, 215, 20, 255), outline=(215, 140, 10, 255), width=2)

    # Inner warm brown smiling face
    draw.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), fill=(145, 95, 35, 255), outline=(95, 55, 15, 255), width=3)
    draw.ellipse((cx - 21, cy - 21, cx + 21, cy + 21), fill=(175, 115, 45, 255))

    # Cheerful Eyes
    draw.ellipse((cx - 16, cy - 12, cx - 4, cy + 4), fill=(20, 20, 20, 255))
    draw.ellipse((cx - 12, cy - 10, cx - 7, cy - 4), fill=(255, 255, 255, 255))
    draw.ellipse((cx + 4, cy - 12, cx + 16, cy + 4), fill=(20, 20, 20, 255))
    draw.ellipse((cx + 8, cy - 10, cx + 13, cy - 4), fill=(255, 255, 255, 255))

    # Rosy Cheeks
    draw.ellipse((cx - 18, cy + 4, cx - 8, cy + 12), fill=(235, 130, 100, 160))
    draw.ellipse((cx + 8, cy + 4, cx + 18, cy + 12), fill=(235, 130, 100, 160))

    # Happy Smile
    draw.arc((cx - 12, cy - 2, cx + 12, cy + 16), start=20, end=160, fill=(45, 20, 5, 255), width=3)

    img.save("assets/plants/sunflower.png")


def generate_wallnut_stages():
    # Stage 0: Healthy Wall-nut
    img0 = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    draw0 = ImageDraw.Draw(img0)

    # Nut body (oval brown)
    nx0, ny0, nx1, ny1 = 20, 14, 76, 86
    draw0.ellipse((nx0, ny0, nx1, ny1), fill=(190, 145, 80, 255), outline=(100, 65, 30, 255), width=3)
    # Shading gradient / 3D highlight
    draw0.ellipse((nx0 + 6, ny0 + 6, nx1 - 10, ny1 - 25), fill=(225, 180, 110, 255))

    # Big Curious Eyes looking right
    # Left eye
    draw0.ellipse((32, 28, 48, 52), fill=(255, 255, 255, 255), outline=(80, 50, 20, 255), width=2)
    draw0.ellipse((38, 34, 47, 47), fill=(20, 20, 20, 255))
    draw0.ellipse((42, 36, 46, 42), fill=(255, 255, 255, 255))
    # Right eye
    draw0.ellipse((52, 28, 68, 52), fill=(255, 255, 255, 255), outline=(80, 50, 20, 255), width=2)
    draw0.ellipse((58, 34, 67, 47), fill=(20, 20, 20, 255))
    draw0.ellipse((62, 36, 66, 42), fill=(255, 255, 255, 255))

    # Calm / goofy smile
    draw0.arc((42, 58, 58, 70), start=10, end=170, fill=(70, 40, 15, 255), width=3)
    img0.save("assets/plants/wallnut.png")

    # Stage 1: Cracked Wall-nut (Damaged)
    img1 = img0.copy()
    draw1 = ImageDraw.Draw(img1)
    # Cracks on the forehead and side
    draw1.line([(35, 18), (38, 25), (32, 30)], fill=(75, 40, 15, 255), width=3)
    draw1.line([(68, 48), (62, 54), (66, 62)], fill=(75, 40, 15, 255), width=3)
    # Nervous mouth (straight squiggly line)
    draw1.rectangle((42, 60, 58, 68), fill=(225, 180, 110, 255))  # erase calm smile
    draw1.line([(42, 64), (46, 62), (50, 65), (56, 63)], fill=(70, 40, 15, 255), width=3)
    img1.save("assets/plants/wallnut_cracked1.png")

    # Stage 2: Heavily Cracked Wall-nut (Critical)
    img2 = img1.copy()
    draw2 = ImageDraw.Draw(img2)
    # Massive cracks with chunks missing
    draw2.polygon([(22, 35), (28, 42), (20, 48)], fill=(100, 65, 30, 255))
    draw2.line([(45, 16), (50, 26), (44, 34), (48, 44)], fill=(60, 30, 10, 255), width=3)
    draw2.line([(64, 58), (56, 66), (62, 76)], fill=(60, 30, 10, 255), width=3)
    # Desperate mouth
    draw2.arc((42, 62, 58, 74), start=190, end=350, fill=(70, 40, 15, 255), width=3)
    # Tear drop
    draw2.ellipse((30, 50, 36, 60), fill=(120, 200, 255, 220))
    img2.save("assets/plants/wallnut_cracked2.png")


def generate_cherry_bomb():
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Green stem connecting twin cherries
    draw.line([(32, 52), (48, 22), (64, 52)], fill=(50, 160, 40, 255), width=6)
    draw.polygon([(48, 22), (58, 12), (54, 26)], fill=(60, 185, 45, 255))
    # Sparking lit fuse at the top
    draw.line([(48, 22), (48, 10)], fill=(120, 80, 40, 255), width=3)
    draw.ellipse((44, 4, 52, 12), fill=(255, 210, 40, 255))
    draw.ellipse((46, 6, 50, 10), fill=(255, 255, 220, 255))

    # Left Cherry
    c1x, c1y = 32, 58
    draw.ellipse((c1x - 20, c1y - 20, c1x + 20, c1y + 20), fill=(225, 25, 35, 255), outline=(130, 10, 20, 255), width=3)
    draw.ellipse((c1x - 14, c1y - 14, c1x - 2, c1y - 2), fill=(255, 110, 120, 255))  # shine
    # Angry eyes
    draw.line([(c1x - 12, c1y - 8), (c1x - 2, c1y - 3)], fill=(20, 10, 10, 255), width=3)
    draw.ellipse((c1x - 10, c1y - 4, c1x - 2, c1y + 4), fill=(255, 255, 255, 255))
    draw.ellipse((c1x - 6, c1y - 2, c1x - 2, c1y + 3), fill=(10, 10, 10, 255))

    draw.line([(c1x + 12, c1y - 8), (c1x + 2, c1y - 3)], fill=(20, 10, 10, 255), width=3)
    draw.ellipse((c1x + 2, c1y - 4, c1x + 10, c1y + 4), fill=(255, 255, 255, 255))
    draw.ellipse((c1x + 2, c1y - 2, c1x + 6, c1y + 3), fill=(10, 10, 10, 255))
    # Grimace
    draw.line([(c1x - 8, c1y + 9), (c1x + 8, c1y + 9)], fill=(40, 10, 10, 255), width=3)

    # Right Cherry
    c2x, c2y = 64, 58
    draw.ellipse((c2x - 20, c2y - 20, c2x + 20, c2y + 20), fill=(225, 25, 35, 255), outline=(130, 10, 20, 255), width=3)
    draw.ellipse((c2x - 14, c2y - 14, c2x - 2, c2y - 2), fill=(255, 110, 120, 255))
    # Angry eyes
    draw.line([(c2x - 12, c2y - 8), (c2x - 2, c2y - 3)], fill=(20, 10, 10, 255), width=3)
    draw.ellipse((c2x - 10, c2y - 4, c2x - 2, c2y + 4), fill=(255, 255, 255, 255))
    draw.ellipse((c2x - 6, c2y - 2, c2x - 2, c2y + 3), fill=(10, 10, 10, 255))

    draw.line([(c2x + 12, c2y - 8), (c2x + 2, c2y - 3)], fill=(20, 10, 10, 255), width=3)
    draw.ellipse((c2x + 2, c2y - 4, c2x + 10, c2y + 4), fill=(255, 255, 255, 255))
    draw.ellipse((c2x + 2, c2y - 2, c2x + 6, c2y + 3), fill=(10, 10, 10, 255))
    # Grimace
    draw.line([(c2x - 8, c2y + 9), (c2x + 8, c2y + 9)], fill=(40, 10, 10, 255), width=3)

    img.save("assets/plants/cherry_bomb.png")


def generate_potato_mine_stages():
    # Unarmed stage (under dirt)
    img_u = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    draw_u = ImageDraw.Draw(img_u)
    # Dirt mound
    draw_u.ellipse((18, 58, 78, 88), fill=(130, 85, 45, 255), outline=(75, 45, 20, 255), width=2)
    # Potato top poking out
    draw_u.ellipse((34, 46, 62, 68), fill=(185, 140, 80, 255), outline=(95, 65, 30, 255), width=2)
    # Blinking red antenna bulb (grey/off or faint red)
    draw_u.line([(48, 46), (48, 36)], fill=(80, 80, 80, 255), width=3)
    draw_u.ellipse((44, 30, 52, 38), fill=(220, 60, 60, 255), outline=(130, 20, 20, 255), width=1)
    img_u.save("assets/plants/potato_mine_unarmed.png")

    # Armed stage (popped up, ready to explode!)
    img_a = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    draw_a = ImageDraw.Draw(img_a)
    # Dirt base
    draw_a.ellipse((18, 68, 78, 90), fill=(130, 85, 45, 255), outline=(75, 45, 20, 255), width=2)
    # Potato body popped up
    draw_a.ellipse((26, 32, 70, 78), fill=(205, 160, 95, 255), outline=(110, 75, 35, 255), width=3)
    # Bright glowing red antenna
    draw_a.line([(48, 32), (48, 16)], fill=(120, 40, 40, 255), width=4)
    draw_a.ellipse((40, 8, 56, 24), fill=(255, 30, 30, 255), outline=(160, 10, 10, 255), width=2)
    draw_a.ellipse((45, 12, 51, 18), fill=(255, 200, 200, 255))  # glow spot

    # Cute Derpy Face
    # Big eyes looking up
    draw_a.ellipse((34, 40, 46, 54), fill=(255, 255, 255, 255), outline=(80, 50, 20, 255), width=2)
    draw_a.ellipse((38, 42, 44, 48), fill=(20, 20, 20, 255))
    draw_a.ellipse((50, 40, 62, 54), fill=(255, 255, 255, 255), outline=(80, 50, 20, 255), width=2)
    draw_a.ellipse((54, 42, 60, 48), fill=(20, 20, 20, 255))
    # Smile
    draw_a.arc((42, 58, 54, 68), start=10, end=170, fill=(70, 40, 15, 255), width=3)
    img_a.save("assets/plants/potato_mine_armed.png")
    # Save standard canonical potato_mine.png so sprite lookups succeed
    img_a.save("assets/plants/potato_mine.png")


def generate_repeater():
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Base stem & leaves
    draw.ellipse((28, 74, 52, 88), fill=(35, 120, 30, 255), outline=(15, 70, 12, 255), width=2)
    draw.ellipse((44, 74, 68, 88), fill=(45, 140, 35, 255), outline=(15, 70, 12, 255), width=2)
    draw.line([(48, 55), (46, 78)], fill=(40, 130, 30, 255), width=9)

    # Twin leaves on back of head (repeater signature)
    for lx, ly in [(20, 30), (14, 44)]:
        draw.polygon([(lx + 14, ly), (lx - 8, ly - 4), (lx + 2, ly + 10)],
                     fill=(50, 170, 35, 255), outline=(20, 85, 15, 255), width=2)

    # Darker Green Head with eyebrow ridge
    hx, hy, hr = 46, 42, 24
    draw.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=(80, 185, 35, 255), outline=(25, 95, 20, 255), width=3)
    # Head highlight
    draw.ellipse((hx - hr + 7, hy - hr + 6, hx - 4, hy - 4), fill=(140, 235, 80, 255))

    # Dark green headband
    draw.arc((hx - hr + 4, hy - hr + 10, hx + hr - 4, hy + 2), start=170, end=350, fill=(30, 90, 20, 255), width=4)

    # Snout / Cannon tube (facing right)
    draw.polygon([(hx + 12, hy - 11), (hx + 38, hy - 16), (hx + 42, hy + 12), (hx + 14, hy + 11)],
                 fill=(70, 175, 30, 255), outline=(25, 95, 20, 255), width=3)
    draw.ellipse((hx + 35, hy - 16, hx + 44, hy + 12), fill=(20, 65, 15, 255), outline=(10, 45, 10, 255), width=2)

    # Fierce Eyes
    draw.line([(hx, hy - 16), (hx + 18, hy - 12)], fill=(20, 70, 15, 255), width=3)
    draw.ellipse((hx + 2, hy - 14, hx + 18, hy + 4), fill=(255, 255, 255, 255), outline=(20, 80, 20, 255), width=2)
    draw.ellipse((hx + 8, hy - 10, hx + 16, hy), fill=(20, 20, 20, 255))
    draw.ellipse((hx + 12, hy - 8, hx + 15, hy - 4), fill=(255, 255, 255, 255))

    draw.ellipse((hx - 14, hy - 14, hx, hy + 3), fill=(255, 255, 255, 255), outline=(20, 80, 20, 255), width=2)
    draw.ellipse((hx - 8, hy - 10, hx - 1, hy), fill=(20, 20, 20, 255))

    img.save("assets/plants/repeater.png")


def generate_chomper():
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Stem and spiky leafy base
    draw.line([(48, 55), (46, 82)], fill=(45, 140, 35, 255), width=10)
    draw.polygon([(46, 80), (22, 88), (40, 72)], fill=(40, 150, 30, 255), outline=(20, 80, 15, 255), width=2)
    draw.polygon([(48, 80), (74, 88), (56, 72)], fill=(40, 150, 30, 255), outline=(20, 80, 15, 255), width=2)

    # Big purple carnivorous head (upper and lower jaws open)
    # Upper jaw
    draw.chord((26, 16, 86, 60), start=180, end=360, fill=(150, 45, 175, 255), outline=(75, 15, 95, 255), width=3)
    # Lower jaw
    draw.chord((26, 44, 86, 76), start=0, end=180, fill=(130, 35, 155, 255), outline=(75, 15, 95, 255), width=3)

    # Deep dark mouth cavity
    draw.ellipse((32, 34, 80, 56), fill=(45, 10, 55, 255))

    # Sharp white teeth!
    # Top teeth
    for tx in [38, 48, 58, 68]:
        draw.polygon([(tx, 36), (tx + 5, 46), (tx + 9, 36)], fill=(255, 255, 240, 255), outline=(90, 80, 80, 255), width=1)
    # Bottom teeth
    for tx in [42, 52, 62]:
        draw.polygon([(tx, 54), (tx + 5, 44), (tx + 9, 54)], fill=(255, 255, 240, 255), outline=(90, 80, 80, 255), width=1)

    # Derpy little pink eyes on top
    draw.ellipse((42, 14, 52, 26), fill=(255, 255, 255, 255), outline=(75, 15, 95, 255), width=2)
    draw.ellipse((46, 18, 50, 23), fill=(20, 20, 20, 255))
    draw.ellipse((58, 14, 68, 26), fill=(255, 255, 255, 255), outline=(75, 15, 95, 255), width=2)
    draw.ellipse((62, 18, 66, 23), fill=(20, 20, 20, 255))

    img.save("assets/plants/chomper.png")


def generate_jalapeno():
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fiery flame hair at top
    draw.polygon([(48, 4), (40, 22), (48, 16), (56, 22)], fill=(255, 140, 20, 255), outline=(220, 60, 10, 255), width=2)
    draw.polygon([(48, 10), (44, 20), (52, 20)], fill=(255, 240, 80, 255))

    # Bright Red Pepper Body (curved tapering chili)
    draw.polygon([
        (40, 20), (56, 20), (62, 40), (58, 68), (52, 84), (48, 88), (44, 84), (36, 68), (34, 40)
    ], fill=(235, 25, 25, 255), outline=(130, 10, 10, 255), width=3)
    # Highlight
    draw.line([(40, 26), (40, 64)], fill=(255, 110, 110, 255), width=3)

    # Furious Angry Face
    # Unibrow angled downwards
    draw.line([(36, 32), (48, 40), (60, 32)], fill=(20, 5, 5, 255), width=4)
    # Yellow furious eyes
    draw.ellipse((38, 36, 46, 46), fill=(255, 240, 40, 255), outline=(30, 10, 10, 255), width=2)
    draw.ellipse((42, 39, 45, 43), fill=(20, 5, 5, 255))
    draw.ellipse((50, 36, 58, 46), fill=(255, 240, 40, 255), outline=(30, 10, 10, 255), width=2)
    draw.ellipse((51, 39, 54, 43), fill=(20, 5, 5, 255))
    # Teeth gritting grimace
    draw.rectangle((40, 52, 56, 60), fill=(245, 245, 240, 255), outline=(30, 5, 5, 255), width=2)
    draw.line([(48, 52), (48, 60)], fill=(30, 5, 5, 255), width=2)

    img.save("assets/plants/jalapeno.png")


def generate_squash():
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Little brown stem on head
    draw.polygon([(46, 12), (48, 4), (54, 6), (50, 14)], fill=(120, 80, 40, 255), outline=(60, 40, 20, 255), width=2)

    # Pear/bell shaped Squash body (green with ridges)
    draw.ellipse((30, 14, 66, 52), fill=(120, 195, 60, 255), outline=(40, 95, 20, 255), width=3)
    draw.ellipse((22, 38, 74, 86), fill=(110, 185, 55, 255), outline=(40, 95, 20, 255), width=3)

    # Shading ridges
    draw.arc((32, 20, 64, 82), start=80, end=280, fill=(75, 140, 35, 255), width=3)
    draw.arc((32, 20, 64, 82), start=260, end=460, fill=(75, 140, 35, 255), width=3)

    # Grumpy intense gaze
    # Heavy brow
    draw.line([(32, 36), (48, 44), (64, 36)], fill=(30, 65, 15, 255), width=5)
    # Eyes looking down at zombie
    draw.ellipse((34, 42, 46, 54), fill=(255, 255, 255, 255), outline=(30, 65, 15, 255), width=2)
    draw.ellipse((40, 47, 45, 52), fill=(20, 20, 20, 255))
    draw.ellipse((50, 42, 62, 54), fill=(255, 255, 255, 255), outline=(30, 65, 15, 255), width=2)
    draw.ellipse((51, 47, 56, 52), fill=(20, 20, 20, 255))

    # Frown
    draw.arc((38, 62, 58, 76), start=200, end=340, fill=(35, 75, 15, 255), width=4)

    img.save("assets/plants/squash.png")


def generate_puff_shroom():
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Small night mushroom
    # Stem
    draw.polygon([(42, 60), (54, 60), (56, 84), (40, 84)], fill=(190, 160, 215, 255), outline=(90, 60, 120, 255), width=2)

    # Cute rounded cap (purple with violet spots)
    draw.ellipse((24, 28, 72, 66), fill=(160, 65, 195, 255), outline=(85, 25, 115, 255), width=3)
    # Spots on cap
    draw.ellipse((34, 34, 44, 44), fill=(215, 140, 240, 255))
    draw.ellipse((52, 32, 64, 44), fill=(215, 140, 240, 255))
    draw.ellipse((44, 48, 54, 58), fill=(215, 140, 240, 255))

    # Cute sleepy face on stem
    draw.ellipse((43, 66, 47, 72), fill=(30, 15, 45, 255))
    draw.ellipse((49, 66, 53, 72), fill=(30, 15, 45, 255))
    # Snout blowing spores
    draw.ellipse((52, 68, 62, 76), fill=(145, 55, 175, 255), outline=(75, 20, 100, 255), width=2)

    img.save("assets/plants/puff_shroom.png")


def generate_fume_shroom():
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Large purple trumpet-mushroom
    # Sturdy stem
    draw.polygon([(36, 54), (58, 54), (62, 84), (32, 84)], fill=(165, 135, 195, 255), outline=(80, 50, 110, 255), width=3)

    # Wide cap
    draw.ellipse((20, 22, 76, 58), fill=(140, 50, 175, 255), outline=(70, 20, 100, 255), width=3)
    # Bright glowing violet spots
    draw.ellipse((28, 28, 40, 40), fill=(225, 120, 255, 255))
    draw.ellipse((56, 26, 68, 38), fill=(225, 120, 255, 255))

    # Big trumpet snout (facing right to shoot fumes)
    draw.polygon([(52, 42), (76, 36), (82, 66), (54, 60)], fill=(120, 40, 155, 255), outline=(60, 15, 85, 255), width=3)
    draw.ellipse((74, 36, 84, 66), fill=(40, 10, 55, 255), outline=(20, 5, 30, 255), width=2)

    # Eyes
    draw.ellipse((38, 44, 46, 54), fill=(255, 255, 255, 255), outline=(60, 20, 85, 255), width=2)
    draw.ellipse((42, 47, 45, 52), fill=(20, 20, 20, 255))

    img.save("assets/plants/fume_shroom.png")



# -------------------------------------------------------------
# ZOMBIES SPRITES (Transparent RGBA 96x128 for height)
# -------------------------------------------------------------
def generate_base_zombie_body(draw: ImageDraw.ImageDraw, ox=0, oy=0):
    # Zombie body anchor: centered around x=48+ox, ground at y=120+oy

    # Legs (Blue tattered pants)
    # Left leg
    draw.polygon([(40 + ox, 78 + oy), (46 + ox, 78 + oy), (44 + ox, 114 + oy), (38 + ox, 114 + oy)],
                 fill=(45, 60, 95, 255), outline=(20, 30, 55, 255), width=2)
    # Right leg (stepped forward)
    draw.polygon([(48 + ox, 78 + oy), (54 + ox, 78 + oy), (58 + ox, 114 + oy), (52 + ox, 114 + oy)],
                 fill=(55, 70, 110, 255), outline=(20, 30, 55, 255), width=2)
    # Brown shoes
    draw.ellipse((34 + ox, 112 + oy, 46 + ox, 122 + oy), fill=(75, 50, 30, 255), outline=(40, 25, 15, 255), width=2)
    draw.ellipse((50 + ox, 112 + oy, 64 + ox, 122 + oy), fill=(75, 50, 30, 255), outline=(40, 25, 15, 255), width=2)

    # Torso (Brown ragged jacket, white shirt collar, red tie)
    draw.polygon([(34 + ox, 44 + oy), (62 + ox, 44 + oy), (60 + ox, 80 + oy), (36 + ox, 80 + oy)],
                 fill=(115, 85, 60, 255), outline=(60, 45, 30, 255), width=2)
    # White collar shirt peeking
    draw.polygon([(44 + ox, 44 + oy), (52 + ox, 44 + oy), (48 + ox, 55 + oy)], fill=(225, 225, 220, 255))
    # Red crooked tie
    draw.polygon([(46 + ox, 52 + oy), (50 + ox, 52 + oy), (52 + ox, 72 + oy), (48 + ox, 76 + oy), (44 + ox, 72 + oy)],
                 fill=(195, 40, 40, 255), outline=(110, 20, 20, 255), width=1)

    # Outstretched zombie arms (reaching left towards house)
    draw.polygon([(36 + ox, 48 + oy), (16 + ox, 42 + oy), (14 + ox, 50 + oy), (36 + ox, 56 + oy)],
                 fill=(115, 85, 60, 255), outline=(60, 45, 30, 255), width=2)
    # Green zombie hand
    draw.ellipse((10 + ox, 40 + oy, 20 + ox, 52 + oy), fill=(145, 175, 130, 255), outline=(75, 100, 65, 255), width=2)

    # Pale greenish-gray zombie head
    hx, hy = 48 + ox, 32 + oy
    draw.ellipse((hx - 16, hy - 18, hx + 16, hy + 18), fill=(155, 185, 140, 255), outline=(75, 105, 65, 255), width=2)

    # Mismatched zombie eyes (one big, one small)
    # Left eye (smaller, deadpan)
    draw.ellipse((hx - 12, hy - 8, hx - 2, hy + 2), fill=(240, 240, 230, 255), outline=(50, 70, 45, 255), width=2)
    draw.ellipse((hx - 8, hy - 5, hx - 5, hy - 2), fill=(20, 20, 20, 255))
    # Right eye (large, bulging)
    draw.ellipse((hx - 1, hy - 11, hx + 13, hy + 3), fill=(255, 255, 240, 255), outline=(50, 70, 45, 255), width=2)
    draw.ellipse((hx + 3, hy - 7, hx + 9, hy - 1), fill=(20, 20, 20, 255))

    # Mouth with crooked teeth
    draw.arc((hx - 10, hy + 4, hx + 10, hy + 14), start=0, end=180, fill=(45, 25, 25, 255), width=3)
    # Two yellowed teeth
    draw.rectangle((hx - 6, hy + 6, hx - 2, hy + 11), fill=(240, 235, 180, 255))
    draw.rectangle((hx + 2, hy + 7, hx + 5, hy + 12), fill=(240, 235, 180, 255))


def generate_normal_zombie():
    img = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    generate_base_zombie_body(draw)
    img.save("assets/zombies/zombie_normal.png")


def generate_conehead_zombie():
    img = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    generate_base_zombie_body(draw)

    # Traffic cone on head
    cx, cy = 48, 20
    draw.polygon([(cx - 16, cy + 2), (cx + 16, cy + 2), (cx + 5, cy - 28), (cx - 5, cy - 28)],
                 fill=(255, 130, 20, 255), outline=(180, 70, 10, 255), width=2)
    # White reflective strip
    draw.polygon([(cx - 10, cy - 8), (cx + 10, cy - 8), (cx + 7, cy - 18), (cx - 7, cy - 18)],
                 fill=(245, 245, 245, 255), outline=(180, 70, 10, 255), width=1)
    # Cone base rim
    draw.ellipse((cx - 20, cy, cx + 20, cy + 6), fill=(255, 130, 20, 255), outline=(180, 70, 10, 255), width=2)

    img.save("assets/zombies/zombie_conehead.png")


def generate_buckethead_zombie():
    img = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    generate_base_zombie_body(draw)

    # Metallic iron bucket on head
    bx, by = 48, 22
    draw.polygon([(bx - 17, by + 4), (bx + 17, by + 4), (bx + 19, by - 24), (bx - 19, by - 24)],
                 fill=(170, 175, 185, 255), outline=(90, 95, 105, 255), width=2)
    # Bucket rim & handle
    draw.ellipse((bx - 18, by + 2, bx + 18, by + 7), fill=(195, 200, 210, 255), outline=(90, 95, 105, 255), width=2)
    draw.arc((bx - 20, by - 12, bx + 20, by + 8), start=0, end=180, fill=(120, 125, 135, 255), width=2)

    img.save("assets/zombies/zombie_buckethead.png")


def generate_flag_zombie():
    img = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    generate_base_zombie_body(draw)

    # Red Flag on a pole held by left arm
    draw.line([(22, 115), (22, 12)], fill=(125, 85, 45, 255), width=4)
    # Red fabric
    draw.polygon([(22, 14), (2, 28), (22, 42)], fill=(235, 35, 45, 255), outline=(150, 15, 25, 255), width=2)
    # Zombie Brain skull symbol on flag
    draw.ellipse((8, 22, 16, 32), fill=(245, 180, 200, 255))

    img.save("assets/zombies/zombie_flag.png")


def generate_pole_vaulter():
    img = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    ox, oy = 8, 0
    draw.polygon([(40 + ox, 78 + oy), (46 + ox, 78 + oy), (44 + ox, 114 + oy), (38 + ox, 114 + oy)],
                 fill=(220, 220, 225, 255), outline=(120, 120, 135, 255), width=2)
    draw.polygon([(48 + ox, 78 + oy), (54 + ox, 78 + oy), (60 + ox, 114 + oy), (54 + ox, 114 + oy)],
                 fill=(220, 220, 225, 255), outline=(120, 120, 135, 255), width=2)
    draw.polygon([(34 + ox, 44 + oy), (62 + ox, 44 + oy), (60 + ox, 80 + oy), (36 + ox, 80 + oy)],
                 fill=(210, 40, 45, 255), outline=(120, 20, 25, 255), width=2)
    hx, hy = 48 + ox, 32 + oy
    draw.ellipse((hx - 16, hy - 18, hx + 16, hy + 18), fill=(155, 185, 140, 255), outline=(75, 105, 65, 255), width=2)
    draw.ellipse((hx - 1, hy - 11, hx + 13, hy + 3), fill=(255, 255, 240, 255), outline=(50, 70, 45, 255), width=2)
    draw.ellipse((hx + 3, hy - 7, hx + 9, hy - 1), fill=(20, 20, 20, 255))
    draw.arc((hx - 10, hy + 4, hx + 10, hy + 14), start=0, end=180, fill=(45, 25, 25, 255), width=3)

    draw.line([(75, 20), (5, 110)], fill=(245, 205, 45, 255), width=5)
    draw.line([(75, 20), (5, 110)], fill=(175, 140, 25, 255), width=1)
    img.save("assets/zombies/zombie_polevaulter.png")


def generate_newspaper_zombie():
    img = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    generate_base_zombie_body(draw, ox=6)

    draw.ellipse((42, 24, 52, 34), fill=None, outline=(50, 50, 60, 255), width=2)
    draw.ellipse((53, 24, 63, 34), fill=None, outline=(50, 50, 60, 255), width=2)
    draw.line([(52, 29), (53, 29)], fill=(50, 50, 60, 255), width=2)

    draw.rectangle((12, 46, 42, 92), fill=(235, 230, 220, 255), outline=(80, 80, 80, 255), width=2)
    draw.rectangle((16, 50, 38, 56), fill=(40, 40, 40, 255))
    for ty in range(62, 88, 5):
        draw.line([(16, ty), (38, ty)], fill=(100, 100, 100, 255), width=2)
    img.save("assets/zombies/zombie_newspaper.png")

    img_a = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    draw_a = ImageDraw.Draw(img_a)
    generate_base_zombie_body(draw_a, ox=2)
    draw_a.ellipse((40, 23, 49, 32), fill=(255, 30, 30, 255), outline=(120, 10, 10, 255), width=2)
    draw_a.ellipse((52, 23, 61, 32), fill=(255, 30, 30, 255), outline=(120, 10, 10, 255), width=2)
    draw_a.polygon([(14, 55), (28, 50), (22, 70), (12, 65)], fill=(225, 220, 210, 255), outline=(80, 80, 80, 255), width=1)
    img_a.save("assets/zombies/zombie_newspaper_angry.png")


def generate_football_zombie():
    img = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    ox, oy = 0, 0
    # Athletic White Football Pants
    draw.polygon([(40 + ox, 76 + oy), (46 + ox, 76 + oy), (44 + ox, 114 + oy), (38 + ox, 114 + oy)],
                 fill=(235, 235, 235, 255), outline=(120, 120, 120, 255), width=2)
    draw.polygon([(48 + ox, 76 + oy), (54 + ox, 76 + oy), (60 + ox, 114 + oy), (54 + ox, 114 + oy)],
                 fill=(235, 235, 235, 255), outline=(120, 120, 120, 255), width=2)
    # Cleats
    draw.ellipse((34 + ox, 112 + oy, 46 + ox, 122 + oy), fill=(40, 40, 40, 255), outline=(15, 15, 15, 255), width=2)
    draw.ellipse((50 + ox, 112 + oy, 64 + ox, 122 + oy), fill=(40, 40, 40, 255), outline=(15, 15, 15, 255), width=2)

    # Big Brown Padded Football Jersey with #7
    draw.polygon([(30 + ox, 40 + oy), (66 + ox, 40 + oy), (62 + ox, 80 + oy), (34 + ox, 80 + oy)],
                 fill=(160, 40, 35, 255), outline=(90, 15, 15, 255), width=3)
    # Jersey stripes & number
    draw.line([(34 + ox, 46 + oy), (62 + ox, 46 + oy)], fill=(245, 245, 245, 255), width=2)
    draw.rectangle((44 + ox, 54 + oy, 52 + ox, 68 + oy), fill=(255, 255, 255, 255))

    # Padded Football Helmet (leather/red with white central stripe)
    hx, hy = 48 + ox, 28 + oy
    draw.ellipse((hx - 18, hy - 20, hx + 18, hy + 18), fill=(185, 30, 30, 255), outline=(100, 10, 10, 255), width=3)
    draw.line([(hx, hy - 20), (hx, hy + 18)], fill=(255, 255, 255, 255), width=3)
    # Metal face cage grill
    for gy in [-6, 2, 10]:
        draw.line([(hx - 14, hy + gy), (hx + 14, hy + gy)], fill=(180, 185, 195, 255), width=3)
    draw.line([(hx - 4, hy - 10), (hx - 4, hy + 14)], fill=(180, 185, 195, 255), width=2)
    draw.line([(hx + 4, hy - 10), (hx + 4, hy + 14)], fill=(180, 185, 195, 255), width=2)

    # Red sprint eyes peeking through cage
    draw.ellipse((hx - 10, hy - 6, hx - 4, hy), fill=(255, 230, 40, 255))
    draw.ellipse((hx + 4, hy - 6, hx + 10, hy), fill=(255, 230, 40, 255))

    img.save("assets/zombies/zombie_football.png")


def generate_screendoor_zombie():
    img = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    generate_base_zombie_body(draw, ox=12)

    # Large Metal Screen Door shield held in front
    sx0, sy0, sx1, sy1 = 10, 25, 46, 115
    # Aluminum door frame
    draw.rounded_rectangle((sx0, sy0, sx1, sy1), radius=4, fill=(190, 195, 205, 255), outline=(100, 105, 115, 255), width=3)
    # Dark mesh screen interior
    draw.rectangle((sx0 + 4, sy0 + 6, sx1 - 4, sy1 - 6), fill=(70, 75, 85, 220), outline=(50, 55, 60, 255), width=1)
    # Mesh cross grid
    for mx in range(sx0 + 8, sx1 - 4, 6):
        draw.line([(mx, sy0 + 6), (mx, sy1 - 6)], fill=(120, 125, 135, 180), width=1)
    for my in range(sy0 + 10, sy1 - 6, 8):
        draw.line([(sx0 + 4, my), (sx1 - 4, my)], fill=(120, 125, 135, 180), width=1)
    # Door handle
    draw.rectangle((sx1 - 8, sy0 + 45, sx1 - 2, sy0 + 55), fill=(40, 40, 45, 255))

    img.save("assets/zombies/zombie_screendoor.png")


def generate_disco_zombie():
    img = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    ox, oy = 0, 0
    # Flared 70s white bell-bottom trousers
    draw.polygon([(36 + ox, 76 + oy), (46 + ox, 76 + oy), (48 + ox, 114 + oy), (30 + ox, 114 + oy)],
                 fill=(245, 245, 250, 255), outline=(150, 150, 165, 255), width=2)
    draw.polygon([(48 + ox, 76 + oy), (58 + ox, 76 + oy), (66 + ox, 114 + oy), (48 + ox, 114 + oy)],
                 fill=(245, 245, 250, 255), outline=(150, 150, 165, 255), width=2)
    # Platform shoes
    draw.rectangle((28 + ox, 114 + oy, 48 + ox, 124 + oy), fill=(210, 40, 120, 255), outline=(110, 10, 60, 255), width=2)
    draw.rectangle((48 + ox, 114 + oy, 68 + ox, 124 + oy), fill=(210, 40, 120, 255), outline=(110, 10, 60, 255), width=2)

    # Open collar Disco Shirt & sparkly white blazer
    draw.polygon([(32 + ox, 42 + oy), (64 + ox, 42 + oy), (60 + ox, 78 + oy), (36 + ox, 78 + oy)],
                 fill=(250, 250, 255, 255), outline=(160, 160, 180, 255), width=2)
    # Deep V-neck showing bare zombie chest
    draw.polygon([(42 + ox, 42 + oy), (54 + ox, 42 + oy), (48 + ox, 62 + oy)], fill=(145, 175, 130, 255))
    # Shiny gold chain and disco medallion
    draw.arc((42 + ox, 46 + oy, 54 + ox, 66 + oy), start=0, end=180, fill=(255, 215, 30, 255), width=2)
    draw.ellipse((45 + ox, 64 + oy, 51 + ox, 70 + oy), fill=(255, 220, 40, 255))

    # Giant brown Afro haircut!
    hx, hy = 48 + ox, 32 + oy
    draw.ellipse((hx - 24, hy - 32, hx + 24, hy + 6), fill=(65, 40, 25, 255), outline=(35, 20, 10, 255), width=3)

    # Zombie face inside afro
    draw.ellipse((hx - 14, hy - 14, hx + 14, hy + 16), fill=(155, 185, 140, 255), outline=(75, 105, 65, 255), width=2)

    # Cool Star / Disco Sunglasses
    draw.polygon([(hx - 13, hy - 6), (hx - 3, hy - 6), (hx - 4, hy + 4), (hx - 12, hy + 4)], fill=(20, 20, 20, 255))
    draw.polygon([(hx + 3, hy - 6), (hx + 13, hy - 6), (hx + 12, hy + 4), (hx + 4, hy + 4)], fill=(20, 20, 20, 255))
    draw.line([(hx - 3, hy - 3), (hx + 3, hy - 3)], fill=(255, 215, 30, 255), width=2)

    # Smug grin
    draw.arc((hx - 8, hy + 6, hx + 8, hy + 14), start=0, end=180, fill=(40, 20, 20, 255), width=2)

    img.save("assets/zombies/zombie_disco.png")


def generate_backup_zombie():
    img = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    ox, oy = 0, 0
    # Purple flared trousers
    draw.polygon([(36 + ox, 76 + oy), (46 + ox, 76 + oy), (46 + ox, 114 + oy), (32 + ox, 114 + oy)],
                 fill=(140, 50, 160, 255), outline=(70, 15, 80, 255), width=2)
    draw.polygon([(48 + ox, 76 + oy), (58 + ox, 76 + oy), (64 + ox, 114 + oy), (48 + ox, 114 + oy)],
                 fill=(140, 50, 160, 255), outline=(70, 15, 80, 255), width=2)

    # Silver glitter shirt
    draw.polygon([(34 + ox, 42 + oy), (62 + ox, 42 + oy), (58 + ox, 78 + oy), (36 + ox, 78 + oy)],
                 fill=(200, 205, 220, 255), outline=(110, 115, 130, 255), width=2)

    # Head and smaller afro
    hx, hy = 48 + ox, 32 + oy
    draw.ellipse((hx - 18, hy - 24, hx + 18, hy + 4), fill=(55, 35, 20, 255), outline=(30, 15, 10, 255), width=2)
    draw.ellipse((hx - 13, hy - 12, hx + 13, hy + 14), fill=(155, 185, 140, 255), outline=(75, 105, 65, 255), width=2)
    # Sunglasses
    draw.rectangle((hx - 11, hy - 4, hx - 2, hy + 3), fill=(30, 30, 35, 255))
    draw.rectangle((hx + 2, hy - 4, hx + 11, hy + 3), fill=(30, 30, 35, 255))

    img.save("assets/zombies/zombie_backup.png")


def generate_gargantuar():
    # Massive Brute (112x144)
    img = Image.new("RGBA", (112, 144), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    ox, oy = 8, 8
    # Massive tree-trunk legs
    draw.polygon([(36 + ox, 85 + oy), (48 + ox, 85 + oy), (46 + ox, 128 + oy), (32 + ox, 128 + oy)],
                 fill=(70, 50, 85, 255), outline=(35, 20, 45, 255), width=3)
    draw.polygon([(54 + ox, 85 + oy), (66 + ox, 85 + oy), (70 + ox, 128 + oy), (56 + ox, 128 + oy)],
                 fill=(70, 50, 85, 255), outline=(35, 20, 45, 255), width=3)

    # Giant muscular greenish-gray torso
    draw.polygon([(26 + ox, 38 + oy), (76 + ox, 38 + oy), (70 + ox, 88 + oy), (32 + ox, 88 + oy)],
                 fill=(135, 165, 120, 255), outline=(65, 90, 55, 255), width=3)
    # Heavy leather apron
    draw.polygon([(34 + ox, 44 + oy), (68 + ox, 44 + oy), (64 + ox, 86 + oy), (36 + ox, 86 + oy)],
                 fill=(115, 80, 50, 255), outline=(60, 40, 20, 255), width=2)

    # Huge Head with metal bolts
    hx, hy = 50 + ox, 24 + oy
    draw.ellipse((hx - 20, hy - 20, hx + 20, hy + 20), fill=(145, 175, 130, 255), outline=(65, 90, 55, 255), width=3)
    # Glowing red tiny furious eyes
    draw.ellipse((hx - 12, hy - 6, hx - 5, hy + 1), fill=(255, 30, 30, 255), outline=(100, 10, 10, 255), width=2)
    draw.ellipse((hx + 5, hy - 6, hx + 12, hy + 1), fill=(255, 30, 30, 255), outline=(100, 10, 10, 255), width=2)
    # Heavy jaw with tusks/teeth
    draw.rectangle((hx - 10, hy + 6, hx + 10, hy + 14), fill=(40, 25, 20, 255))
    draw.polygon([(hx - 8, hy + 14), (hx - 5, hy + 8), (hx - 2, hy + 14)], fill=(245, 245, 230, 255))
    draw.polygon([(hx + 2, hy + 14), (hx + 5, hy + 8), (hx + 8, hy + 14)], fill=(245, 245, 230, 255))

    # Massive Telephone Pole weapon resting in hands
    draw.line([(88 + ox, 6 + oy), (12 + ox, 136 + oy)], fill=(130, 90, 50, 255), width=10)
    draw.line([(88 + ox, 6 + oy), (12 + ox, 136 + oy)], fill=(75, 50, 25, 255), width=2)
    # Pole crossbar with insulators
    draw.line([(78 + ox, 18 + oy), (96 + ox, 32 + oy)], fill=(120, 80, 40, 255), width=6)
    draw.ellipse((76 + ox, 16 + oy, 84 + ox, 24 + oy), fill=(225, 230, 240, 255))
    draw.ellipse((92 + ox, 28 + oy, 100 + ox, 36 + oy), fill=(225, 230, 240, 255))

    img.save("assets/zombies/zombie_gargantuar.png")


# -------------------------------------------------------------
# PROJECTILES & SPECIAL OBJECTS
# -------------------------------------------------------------
def generate_projectiles():
    # Green Pea (32x32)
    img_p = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw_p = ImageDraw.Draw(img_p)
    draw_p.ellipse((4, 4, 28, 28), fill=(110, 215, 45, 255), outline=(35, 115, 25, 255), width=2)
    draw_p.ellipse((8, 8, 16, 16), fill=(185, 250, 115, 255))  # shine
    img_p.save("assets/projectiles/pea.png")

    # Frozen Snow Pea (32x32)
    img_sp = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw_sp = ImageDraw.Draw(img_sp)
    draw_sp.ellipse((4, 4, 28, 28), fill=(95, 205, 245, 255), outline=(30, 110, 175, 255), width=2)
    draw_sp.ellipse((8, 8, 16, 16), fill=(215, 250, 255, 255))
    # Snowflake accent
    draw_sp.line([(16, 10), (16, 22)], fill=(255, 255, 255, 220), width=2)
    draw_sp.line([(10, 16), (22, 16)], fill=(255, 255, 255, 220), width=2)
    img_sp.save("assets/projectiles/snow_pea_proj.png")

    # Fume Spore Cloud (48x48)
    img_fume = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    draw_fume = ImageDraw.Draw(img_fume)
    draw_fume.ellipse((6, 8, 42, 40), fill=(210, 90, 235, 170))
    draw_fume.ellipse((14, 12, 34, 34), fill=(240, 140, 255, 220))
    draw_fume.ellipse((20, 16, 28, 26), fill=(255, 255, 255, 240))
    img_fume.save("assets/projectiles/fume_spore.png")

    # Jalapeno Fire Wall (Row incinerator segment 104x96)
    img_fire = Image.new("RGBA", (104, 96), (0, 0, 0, 0))
    draw_fire = ImageDraw.Draw(img_fire)
    for fx in range(6, 98, 14):
        # Spikes of blazing flame
        draw_fire.polygon([(fx, 94), (fx + 7, 10), (fx + 14, 94)], fill=(255, 60, 20, 240))
        draw_fire.polygon([(fx + 3, 94), (fx + 7, 30), (fx + 11, 94)], fill=(255, 215, 30, 255))
    img_fire.save("assets/projectiles/jalapeno_fire.png")

    # Sun entity (72x72)
    img_sun = Image.new("RGBA", (72, 72), (0, 0, 0, 0))
    draw_sun = ImageDraw.Draw(img_sun)
    scx, scy = 36, 36
    # 14 golden rays
    for i in range(14):
        ang = i * (2 * math.pi / 14)
        rx = scx + math.cos(ang) * 23
        ry = scy + math.sin(ang) * 23
        draw_sun.ellipse((rx - 7, ry - 7, rx + 7, ry + 7), fill=(255, 200, 30, 240))
    # Inner orb
    draw_sun.ellipse((scx - 20, scy - 20, scx + 20, scy + 20), fill=(255, 235, 60, 255), outline=(225, 140, 15, 255), width=3)
    draw_sun.ellipse((scx - 14, scy - 14, scx - 2, scy - 2), fill=(255, 255, 210, 255))  # highlight
    # Cute smiling face
    draw_sun.ellipse((scx - 9, scy - 7, scx - 4, scy - 1), fill=(180, 80, 10, 255))
    draw_sun.ellipse((scx + 4, scy - 7, scx + 9, scy - 1), fill=(180, 80, 10, 255))
    draw_sun.arc((scx - 8, scy - 2, scx + 8, scy + 11), start=20, end=160, fill=(180, 80, 10, 255), width=2)
    img_sun.save("assets/projectiles/sun.png")

    # Lawn Mower (80x64)
    img_lm = Image.new("RGBA", (80, 64), (0, 0, 0, 0))
    draw_lm = ImageDraw.Draw(img_lm)
    draw_lm.rounded_rectangle((14, 22, 62, 54), radius=8, fill=(225, 35, 45, 255), outline=(135, 15, 25, 255), width=3)
    draw_lm.rectangle((26, 12, 50, 22), fill=(185, 190, 200, 255), outline=(100, 105, 115, 255), width=2)
    draw_lm.ellipse((8, 40, 24, 58), fill=(40, 40, 45, 255), outline=(15, 15, 20, 255), width=3)
    draw_lm.ellipse((13, 45, 19, 53), fill=(190, 190, 200, 255))
    draw_lm.ellipse((52, 40, 68, 58), fill=(40, 40, 45, 255), outline=(15, 15, 20, 255), width=3)
    draw_lm.ellipse((57, 45, 63, 53), fill=(190, 190, 200, 255))
    draw_lm.line([(20, 26), (4, 4)], fill=(150, 155, 165, 255), width=4)
    draw_lm.line([(2, 4), (8, 4)], fill=(30, 30, 30, 255), width=4)
    img_lm.save("assets/projectiles/lawn_mower.png")

    # Shovel (64x64)
    img_sh = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw_sh = ImageDraw.Draw(img_sh)
    draw_sh.line([(12, 12), (40, 40)], fill=(160, 105, 55, 255), width=5)
    draw_sh.arc((6, 6, 18, 18), start=45, end=315, fill=(100, 60, 25, 255), width=3)
    draw_sh.polygon([(36, 36), (56, 44), (44, 56)], fill=(175, 185, 195, 255), outline=(90, 100, 110, 255), width=2)
    img_sh.save("assets/ui/shovel.png")

    # Cherry Bomb Explosion Burst (160x160)
    img_exp = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    draw_exp = ImageDraw.Draw(img_exp)
    ecx, ecy = 80, 80
    num_spikes = 16
    poly_pts = []
    for i in range(num_spikes * 2):
        rad = 75 if i % 2 == 0 else 42
        ang = i * (math.pi / num_spikes)
        poly_pts.append((ecx + math.cos(ang) * rad, ecy + math.sin(ang) * rad))
    draw_exp.polygon(poly_pts, fill=(255, 60, 20, 240), outline=(255, 220, 40, 255), width=4)

    poly_pts2 = []
    for i in range(num_spikes * 2):
        rad = 45 if i % 2 == 0 else 24
        ang = i * (math.pi / num_spikes) + 0.15
        poly_pts2.append((ecx + math.cos(ang) * rad, ecy + math.sin(ang) * rad))
    draw_exp.polygon(poly_pts2, fill=(255, 230, 50, 255))
    img_exp.save("assets/projectiles/cherry_explosion.png")

    # Bowling Nut - Normal (Rolling ball 80x80)
    img_bn = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
    draw_bn = ImageDraw.Draw(img_bn)
    draw_bn.ellipse((6, 6, 74, 74), fill=(195, 145, 80, 255), outline=(100, 65, 30, 255), width=4)
    draw_bn.ellipse((14, 14, 60, 60), fill=(225, 180, 110, 255))
    draw_bn.arc((18, 18, 62, 62), start=40, end=200, fill=(120, 80, 35, 255), width=4)
    draw_bn.arc((26, 26, 54, 54), start=220, end=380, fill=(120, 80, 35, 255), width=4)
    img_bn.save("assets/projectiles/bowling_nut.png")

    # Bowling Giant Nut - Riesen-Wallnuss (100x100)
    img_gn = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    draw_gn = ImageDraw.Draw(img_gn)
    draw_gn.ellipse((4, 4, 96, 96), fill=(160, 110, 55, 255), outline=(75, 45, 20, 255), width=5)
    draw_gn.ellipse((12, 12, 88, 88), fill=(205, 155, 90, 255))
    # Heavy stone/steel bands
    draw_gn.arc((20, 20, 80, 80), start=30, end=210, fill=(90, 55, 25, 255), width=6)
    draw_gn.arc((20, 20, 80, 80), start=220, end=390, fill=(90, 55, 25, 255), width=6)
    img_gn.save("assets/projectiles/bowling_giant_nut.png")

    # Bowling Ice Nut - Schnee-Nuss (80x80)
    img_in = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
    draw_in = ImageDraw.Draw(img_in)
    draw_in.ellipse((6, 6, 74, 74), fill=(120, 210, 245, 255), outline=(40, 120, 180, 255), width=4)
    draw_in.ellipse((14, 14, 60, 60), fill=(185, 240, 255, 255))
    # Snowflake crystal pattern
    draw_in.line([(40, 18), (40, 62)], fill=(255, 255, 255, 255), width=4)
    draw_in.line([(18, 40), (62, 40)], fill=(255, 255, 255, 255), width=4)
    draw_in.line([(24, 24), (56, 56)], fill=(255, 255, 255, 255), width=3)
    draw_in.line([(24, 56), (56, 24)], fill=(255, 255, 255, 255), width=3)
    img_in.save("assets/projectiles/bowling_ice_nut.png")


# -------------------------------------------------------------
# UI ASSETS (Seed packets, frames, buttons)
# -------------------------------------------------------------
def generate_ui_assets():
    # Seed packet background frame (80x100)
    img_sp = Image.new("RGBA", (80, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_sp)
    draw.rounded_rectangle((2, 2, 78, 98), radius=6, fill=(230, 215, 175, 255), outline=(125, 95, 55, 255), width=3)
    draw.rectangle((8, 8, 72, 68), fill=(245, 235, 205, 255), outline=(160, 130, 90, 255), width=2)
    draw.rounded_rectangle((6, 72, 74, 94), radius=4, fill=(255, 255, 255, 255), outline=(140, 110, 70, 255), width=2)
    img_sp.save("assets/ui/seed_packet_base.png")

    # Sun counter wood board (140x54)
    img_sc = Image.new("RGBA", (140, 54), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_sc)
    draw.rounded_rectangle((2, 2, 138, 52), radius=10, fill=(155, 110, 65, 255), outline=(85, 55, 30, 255), width=3)
    draw.rounded_rectangle((48, 8, 132, 46), radius=6, fill=(245, 240, 220, 255), outline=(115, 80, 45, 255), width=2)
    img_sc.save("assets/ui/sun_counter_bg.png")

    # Progress bar frame (280x32)
    img_pb = Image.new("RGBA", (280, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_pb)
    draw.rounded_rectangle((2, 2, 278, 30), radius=8, fill=(60, 60, 65, 255), outline=(120, 125, 135, 255), width=3)
    img_pb.save("assets/ui/progress_bar_frame.png")

    # Standard Button Normal (220x60)
    img_btn_n = Image.new("RGBA", (220, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_btn_n)
    draw.rounded_rectangle((2, 2, 218, 58), radius=12, fill=(65, 160, 45, 255), outline=(25, 90, 20, 255), width=4)
    draw.rounded_rectangle((6, 6, 214, 30), radius=8, fill=(110, 205, 85, 255))
    img_btn_n.save("assets/ui/button_normal.png")

    # Standard Button Hover (220x60)
    img_btn_h = Image.new("RGBA", (220, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_btn_h)
    draw.rounded_rectangle((2, 2, 218, 58), radius=12, fill=(85, 195, 60, 255), outline=(35, 120, 30, 255), width=4)
    draw.rounded_rectangle((6, 6, 214, 30), radius=8, fill=(145, 235, 115, 255))
    img_btn_h.save("assets/ui/button_hover.png")


def main():
    print("Generating Plants vs. Zombies game assets...")
    ensure_dir("assets/backgrounds")
    ensure_dir("assets/plants")
    ensure_dir("assets/zombies")
    ensure_dir("assets/projectiles")
    ensure_dir("assets/ui")

    generate_lawn_day()
    generate_lawn_night()
    generate_lawn_bowling()
    generate_menu_bg()

    # Original plants + new plants
    generate_peashooter()
    generate_snow_pea()
    generate_sunflower()
    generate_wallnut_stages()
    generate_cherry_bomb()
    generate_potato_mine_stages()
    generate_repeater()
    generate_chomper()
    generate_jalapeno()
    generate_squash()
    generate_puff_shroom()
    generate_fume_shroom()

    # Original zombies + new zombies
    generate_normal_zombie()
    generate_conehead_zombie()
    generate_buckethead_zombie()
    generate_flag_zombie()
    generate_pole_vaulter()
    generate_newspaper_zombie()
    generate_football_zombie()
    generate_screendoor_zombie()
    generate_disco_zombie()
    generate_backup_zombie()
    generate_gargantuar()

    generate_projectiles()
    generate_ui_assets()

    print("All assets successfully generated!")



if __name__ == "__main__":
    main()
