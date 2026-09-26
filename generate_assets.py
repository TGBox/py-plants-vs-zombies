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

    # Athletic Jersey zombie
    ox, oy = 8, 0
    # Legs in white shorts
    draw.polygon([(40 + ox, 78 + oy), (46 + ox, 78 + oy), (44 + ox, 114 + oy), (38 + ox, 114 + oy)],
                 fill=(220, 220, 225, 255), outline=(120, 120, 135, 255), width=2)
    draw.polygon([(48 + ox, 78 + oy), (54 + ox, 78 + oy), (60 + ox, 114 + oy), (54 + ox, 114 + oy)],
                 fill=(220, 220, 225, 255), outline=(120, 120, 135, 255), width=2)
    # Red athletic singlet
    draw.polygon([(34 + ox, 44 + oy), (62 + ox, 44 + oy), (60 + ox, 80 + oy), (36 + ox, 80 + oy)],
                 fill=(210, 40, 45, 255), outline=(120, 20, 25, 255), width=2)
    # Green head
    hx, hy = 48 + ox, 32 + oy
    draw.ellipse((hx - 16, hy - 18, hx + 16, hy + 18), fill=(155, 185, 140, 255), outline=(75, 105, 65, 255), width=2)
    draw.ellipse((hx - 1, hy - 11, hx + 13, hy + 3), fill=(255, 255, 240, 255), outline=(50, 70, 45, 255), width=2)
    draw.ellipse((hx + 3, hy - 7, hx + 9, hy - 1), fill=(20, 20, 20, 255))
    draw.arc((hx - 10, hy + 4, hx + 10, hy + 14), start=0, end=180, fill=(45, 25, 25, 255), width=3)

    # Long yellow vaulting pole
    draw.line([(75, 20), (5, 110)], fill=(245, 205, 45, 255), width=5)
    draw.line([(75, 20), (5, 110)], fill=(175, 140, 25, 255), width=1)

    img.save("assets/zombies/zombie_polevaulter.png")


def generate_newspaper_zombie():
    # Normal Newspaper Zombie (carrying shield newspaper)
    img = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    generate_base_zombie_body(draw, ox=6)

    # Grandpa glasses
    draw.ellipse((42, 24, 52, 34), fill=None, outline=(50, 50, 60, 255), width=2)
    draw.ellipse((53, 24, 63, 34), fill=None, outline=(50, 50, 60, 255), width=2)
    draw.line([(52, 29), (53, 29)], fill=(50, 50, 60, 255), width=2)

    # Large Folded Newspaper in hands
    draw.rectangle((12, 46, 42, 92), fill=(235, 230, 220, 255), outline=(80, 80, 80, 255), width=2)
    # Headline and text lines
    draw.rectangle((16, 50, 38, 56), fill=(40, 40, 40, 255))
    for ty in range(62, 88, 5):
        draw.line([(16, ty), (38, ty)], fill=(100, 100, 100, 255), width=2)

    img.save("assets/zombies/zombie_newspaper.png")

    # Angry Newspaper Zombie (after newspaper is shredded)
    img_a = Image.new("RGBA", (96, 128), (0, 0, 0, 0))
    draw_a = ImageDraw.Draw(img_a)
    generate_base_zombie_body(draw_a, ox=2)
    # Red glowing angry eyes
    draw_a.ellipse((40, 23, 49, 32), fill=(255, 30, 30, 255), outline=(120, 10, 10, 255), width=2)
    draw_a.ellipse((52, 23, 61, 32), fill=(255, 30, 30, 255), outline=(120, 10, 10, 255), width=2)
    # Shredded newspaper scrap in hand
    draw_a.polygon([(14, 55), (28, 50), (22, 70), (12, 65)], fill=(225, 220, 210, 255), outline=(80, 80, 80, 255), width=1)
    img_a.save("assets/zombies/zombie_newspaper_angry.png")


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
    # Red engine chassis
    draw_lm.rounded_rectangle((14, 22, 62, 54), radius=8, fill=(225, 35, 45, 255), outline=(135, 15, 25, 255), width=3)
    # Silver motor top
    draw_lm.rectangle((26, 12, 50, 22), fill=(185, 190, 200, 255), outline=(100, 105, 115, 255), width=2)
    # Black wheels
    draw_lm.ellipse((8, 40, 24, 58), fill=(40, 40, 45, 255), outline=(15, 15, 20, 255), width=3)
    draw_lm.ellipse((13, 45, 19, 53), fill=(190, 190, 200, 255))
    draw_lm.ellipse((52, 40, 68, 58), fill=(40, 40, 45, 255), outline=(15, 15, 20, 255), width=3)
    draw_lm.ellipse((57, 45, 63, 53), fill=(190, 190, 200, 255))
    # Handlebar
    draw_lm.line([(20, 26), (4, 4)], fill=(150, 155, 165, 255), width=4)
    draw_lm.line([(2, 4), (8, 4)], fill=(30, 30, 30, 255), width=4)
    img_lm.save("assets/projectiles/lawn_mower.png")

    # Shovel (64x64)
    img_sh = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw_sh = ImageDraw.Draw(img_sh)
    # Wooden handle angled
    draw_sh.line([(12, 12), (40, 40)], fill=(160, 105, 55, 255), width=5)
    # Handle grip D-shape
    draw_sh.arc((6, 6, 18, 18), start=45, end=315, fill=(100, 60, 25, 255), width=3)
    # Steel blade
    draw_sh.polygon([(36, 36), (56, 44), (44, 56)], fill=(175, 185, 195, 255), outline=(90, 100, 110, 255), width=2)
    img_sh.save("assets/ui/shovel.png")

    # Cherry Bomb Explosion Burst (160x160)
    img_exp = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    draw_exp = ImageDraw.Draw(img_exp)
    # Multi-point starburst
    ecx, ecy = 80, 80
    num_spikes = 16
    poly_pts = []
    for i in range(num_spikes * 2):
        rad = 75 if i % 2 == 0 else 42
        ang = i * (math.pi / num_spikes)
        poly_pts.append((ecx + math.cos(ang) * rad, ecy + math.sin(ang) * rad))
    draw_exp.polygon(poly_pts, fill=(255, 60, 20, 240), outline=(255, 220, 40, 255), width=4)

    # Inner bright yellow core
    poly_pts2 = []
    for i in range(num_spikes * 2):
        rad = 45 if i % 2 == 0 else 24
        ang = i * (math.pi / num_spikes) + 0.15
        poly_pts2.append((ecx + math.cos(ang) * rad, ecy + math.sin(ang) * rad))
    draw_exp.polygon(poly_pts2, fill=(255, 230, 50, 255))
    img_exp.save("assets/projectiles/cherry_explosion.png")

    # Bowling Nut (Rolling ball 80x80)
    img_bn = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
    draw_bn = ImageDraw.Draw(img_bn)
    draw_bn.ellipse((6, 6, 74, 74), fill=(195, 145, 80, 255), outline=(100, 65, 30, 255), width=4)
    draw_bn.ellipse((14, 14, 60, 60), fill=(225, 180, 110, 255))
    # Rolling spiral motion lines
    draw_bn.arc((18, 18, 62, 62), start=40, end=200, fill=(120, 80, 35, 255), width=4)
    draw_bn.arc((26, 26, 54, 54), start=220, end=380, fill=(120, 80, 35, 255), width=4)
    img_bn.save("assets/projectiles/bowling_nut.png")


# -------------------------------------------------------------
# UI ASSETS (Seed packets, frames, buttons)
# -------------------------------------------------------------
def generate_ui_assets():
    # Seed packet background frame (80x100)
    img_sp = Image.new("RGBA", (80, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_sp)
    # Card base
    draw.rounded_rectangle((2, 2, 78, 98), radius=6, fill=(230, 215, 175, 255), outline=(125, 95, 55, 255), width=3)
    # Image frame inner slot
    draw.rectangle((8, 8, 72, 68), fill=(245, 235, 205, 255), outline=(160, 130, 90, 255), width=2)
    # Bottom Sun cost tag
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

    generate_peashooter()
    generate_snow_pea()
    generate_sunflower()
    generate_wallnut_stages()
    generate_cherry_bomb()
    generate_potato_mine_stages()

    generate_normal_zombie()
    generate_conehead_zombie()
    generate_buckethead_zombie()
    generate_flag_zombie()
    generate_pole_vaulter()
    generate_newspaper_zombie()

    generate_projectiles()
    generate_ui_assets()

    print("All assets successfully generated!")


if __name__ == "__main__":
    main()
