import os
import math
from PIL import Image, ImageDraw

def create_weapon_image():
    return Image.new("RGBA", (128, 128), (0, 0, 0, 0))

def draw_thick_outlined_poly(draw, points, fill_color, outline_color=(20, 20, 20, 255), outline_width=3):
    # Draw outline around polygon
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx*dx + dy*dy <= outline_width * outline_width:
                shifted = [(x + dx, y + dy) for x, y in points]
                draw.polygon(shifted, fill=outline_color)
    draw.polygon(points, fill=fill_color)

def draw_thick_outlined_line(draw, points, fill_color, width, outline_color=(20, 20, 20, 255), outline_pad=3):
    total_w = width + (outline_pad * 2)
    for dx in range(-outline_pad, outline_pad + 1):
        for dy in range(-outline_pad, outline_pad + 1):
            if dx*dx + dy*dy <= outline_pad * outline_pad:
                shifted = [(x + dx, y + dy) for x, y in points]
                draw.line(shifted, fill=outline_color, width=total_w, joint="curve")
    draw.line(points, fill=fill_color, width=width, joint="curve")

def generate_halberd(path):
    img = create_weapon_image()
    draw = ImageDraw.Draw(img)

    # Grayscale palette for stuff tinting
    c_black = (20, 20, 20, 255)
    c_wood_light = (220, 220, 220, 255)
    c_wood_dark = (160, 160, 160, 255)
    c_metal_light = (250, 250, 250, 255)
    c_metal_mid = (200, 200, 200, 255)
    c_metal_dark = (140, 140, 140, 255)

    # Shaft: from bottom-left (18, 110) to top-right (98, 30)
    shaft_pts = [(18, 110), (98, 30)]
    draw_thick_outlined_line(draw, shaft_pts, c_wood_light, width=6, outline_pad=3)
    draw.line([(19, 111), (99, 31)], fill=c_wood_dark, width=2)

    # Metal Socket / Langets
    langet_pts = [(82, 46), (92, 36), (95, 39), (85, 49)]
    draw_thick_outlined_poly(draw, langet_pts, c_metal_mid, outline_width=2)

    # Spear head at tip: top-right
    spear_pts = [
        (92, 36),
        (116, 12),
        (120, 8),
        (112, 16),
        (88, 40)
    ]
    draw_thick_outlined_poly(draw, spear_pts, c_metal_light, outline_width=3)
    draw.polygon([(92, 36), (116, 12), (108, 20), (88, 40)], fill=c_metal_dark)

    # Axe Blade on top-left of the head
    axe_pts = [
        (86, 42),
        (72, 28),
        (64, 18),
        (76, 14),
        (94, 24),
        (96, 32)
    ]
    draw_thick_outlined_poly(draw, axe_pts, c_metal_light, outline_width=3)
    draw.polygon([(86, 42), (72, 28), (80, 28), (96, 32)], fill=c_metal_mid)

    # Rear Spike/Beak on bottom-right of head
    beak_pts = [
        (92, 48),
        (106, 52),
        (112, 54),
        (102, 44),
        (96, 40)
    ]
    draw_thick_outlined_poly(draw, beak_pts, c_metal_mid, outline_width=2)

    img.save(path, "PNG")
    print(f"Generated {path}")

def generate_morningstar(path):
    img = create_weapon_image()
    draw = ImageDraw.Draw(img)

    c_black = (20, 20, 20, 255)
    c_wood = (200, 200, 200, 255)
    c_metal_light = (250, 250, 250, 255)
    c_metal_mid = (195, 195, 195, 255)
    c_metal_dark = (130, 130, 130, 255)

    # Handle: bottom-left (25, 103) to (80, 48)
    handle_pts = [(25, 103), (80, 48)]
    draw_thick_outlined_line(draw, handle_pts, c_wood, width=7, outline_pad=3)

    # Handle grip wraps
    draw.line([(28, 100), (45, 83)], fill=c_metal_dark, width=5)
    draw.ellipse([20, 98, 30, 108], fill=c_metal_mid, outline=c_black, width=2)

    # Spiked Ball Center at (88, 40)
    cx, cy = 88, 40
    r = 16

    # Draw spikes radiating out
    spikes = [
        [(cx + 10, cy - 10), (cx + 26, cy - 26), (cx + 16, cy - 4)], # top-right
        [(cx - 2, cy - 14), (cx, cy - 30), (cx + 12, cy - 12)],      # top
        [(cx + 14, cy - 2), (cx + 30, cy), (cx + 12, cy + 12)],      # right
        [(cx - 12, cy - 12), (cx - 24, cy - 24), (cx - 4, cy - 16)], # top-left
        [(cx + 12, cy + 12), (cx + 24, cy + 24), (cx + 4, cy + 16)], # bottom-right
        [(cx - 14, cy + 2), (cx - 28, cy + 4), (cx - 10, cy - 8)]    # left
    ]
    for sp in spikes:
        draw_thick_outlined_poly(draw, sp, c_metal_light, outline_width=3)

    # Central Sphere outline & body
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx*dx + dy*dy <= 9:
                draw.ellipse([cx - r + dx, cy - r + dy, cx + r + dx, cy + r + dy], fill=c_black)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c_metal_mid)
    # Shading on sphere
    draw.ellipse([cx - r + 3, cy - r + 2, cx + r - 5, cy + r - 6], fill=c_metal_light)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=c_metal_dark)

    img.save(path, "PNG")
    print(f"Generated {path}")

def generate_war_pick(path):
    img = create_weapon_image()
    draw = ImageDraw.Draw(img)

    c_black = (20, 20, 20, 255)
    c_wood = (205, 205, 205, 255)
    c_metal_light = (255, 255, 255, 255)
    c_metal_mid = (195, 195, 195, 255)
    c_metal_dark = (130, 130, 130, 255)

    # Shaft from (24, 104) to (84, 44)
    shaft = [(24, 104), (84, 44)]
    draw_thick_outlined_line(draw, shaft, c_wood, width=6, outline_pad=3)
    draw.ellipse([20, 100, 28, 108], fill=c_metal_mid, outline=c_black, width=2)

    # Head block at (84, 44)
    hx, hy = 84, 44
    head_block = [(hx - 6, hy - 2), (hx + 2, hy - 10), (hx + 10, hy - 2), (hx + 2, hy + 6)]
    draw_thick_outlined_poly(draw, head_block, c_metal_dark, outline_width=2)

    # Beak / Pick point extending left/upwards (punching curve)
    beak_pts = [
        (hx - 2, hy - 6),
        (56, 32),
        (46, 26),
        (48, 22),
        (66, 32),
        (hx + 2, hy - 8)
    ]
    draw_thick_outlined_poly(draw, beak_pts, c_metal_light, outline_width=3)
    draw.polygon([(hx-2, hy-6), (56, 32), (62, 30), (hx+2, hy-8)], fill=c_metal_mid)

    # Hammer back / fluke extending right/downwards
    hammer_pts = [
        (hx + 6, hy + 2),
        (98, 56),
        (104, 52),
        (100, 44),
        (hx + 8, hy - 4)
    ]
    draw_thick_outlined_poly(draw, hammer_pts, c_metal_mid, outline_width=3)

    # Top Spike
    top_spike = [
        (hx - 2, hy - 8),
        (hx + 8, hy - 18),
        (hx + 12, hy - 22),
        (hx + 10, hy - 10),
        (hx + 4, hy - 6)
    ]
    draw_thick_outlined_poly(draw, top_spike, c_metal_light, outline_width=2)

    img.save(path, "PNG")
    print(f"Generated {path}")

def generate_scimitar(path):
    img = create_weapon_image()
    draw = ImageDraw.Draw(img)

    c_black = (20, 20, 20, 255)
    c_metal_light = (255, 255, 255, 255)
    c_metal_mid = (200, 200, 200, 255)
    c_metal_dark = (130, 130, 130, 255)
    c_gold_mid = (175, 175, 175, 255)

    # Scimitar: hilt at bottom-left (28, 100), guard at (40, 88), blade sweeping in dynamic curve up to (108, 20)
    # Pommel
    draw.ellipse([20, 96, 32, 108], fill=c_gold_mid, outline=c_black, width=2)

    # Grip
    draw_thick_outlined_line(draw, [(26, 98), (40, 84)], c_metal_dark, width=6, outline_pad=2)

    # Guard / Quillon (perpendicular to blade)
    guard_pts = [(32, 78), (48, 94), (52, 90), (36, 74)]
    draw_thick_outlined_poly(draw, guard_pts, c_gold_mid, outline_width=2)

    # Curved Blade points
    blade_pts = [
        (40, 84),
        (52, 72),
        (68, 56),
        (86, 38),
        (104, 20),
        (112, 14), # sharp tip
        (102, 26),
        (82, 48),
        (62, 68),
        (46, 80)
    ]
    draw_thick_outlined_poly(draw, blade_pts, c_metal_light, outline_width=3)

    # Blade spine shading / fuller
    spine_pts = [
        (42, 82),
        (54, 70),
        (70, 54),
        (88, 36),
        (104, 20),
        (96, 26),
        (78, 46),
        (58, 66),
        (44, 80)
    ]
    draw.polygon(spine_pts, fill=c_metal_mid)
    draw.line([(42, 82), (54, 70), (70, 54), (88, 36), (104, 20)], fill=c_metal_dark, width=1)

    img.save(path, "PNG")
    print(f"Generated {path}")

def generate_quarterstaff(path):
    img = create_weapon_image()
    draw = ImageDraw.Draw(img)

    c_black = (20, 20, 20, 255)
    c_wood_light = (235, 235, 235, 255)
    c_wood_mid = (190, 190, 190, 255)
    c_wood_dark = (140, 140, 140, 255)
    c_metal_cap = (210, 210, 210, 255)

    # Diagonal staff from (16, 112) to (112, 16)
    staff_pts = [(16, 112), (112, 16)]
    draw_thick_outlined_line(draw, staff_pts, c_wood_mid, width=7, outline_pad=3)

    # Wood grain highlight
    draw.line([(15, 111), (111, 15)], fill=c_wood_light, width=2)
    draw.line([(17, 113), (113, 17)], fill=c_wood_dark, width=2)

    # Metal caps/ferrules at both ends
    # Bottom ferrule
    bot_cap = [(14, 114), (24, 104), (27, 107), (17, 117)]
    draw_thick_outlined_poly(draw, bot_cap, c_metal_cap, outline_width=2)

    # Top ferrule
    top_cap = [(101, 27), (111, 17), (114, 20), (104, 30)]
    draw_thick_outlined_poly(draw, top_cap, c_metal_cap, outline_width=2)

    # Center grip wraps
    draw.line([(58, 70), (70, 58)], fill=c_wood_dark, width=9)
    draw.line([(60, 68), (68, 60)], fill=c_wood_light, width=3)

    img.save(path, "PNG")
    print(f"Generated {path}")

def generate_buckler(path):
    img = create_weapon_image()
    draw = ImageDraw.Draw(img)

    c_black = (20, 20, 20, 255)
    c_metal_light = (255, 255, 255, 255)
    c_metal_mid = (195, 195, 195, 255)
    c_metal_dark = (130, 130, 130, 255)
    c_wood = (215, 215, 215, 255)

    cx, cy = 64, 64
    r = 32

    # Outer circle outline
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx*dx + dy*dy <= 9:
                draw.ellipse([cx - r + dx, cy - r + dy, cx + r + dx, cy + r + dy], fill=c_black)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c_metal_mid)

    # Rim bevel
    draw.ellipse([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4], fill=c_wood)

    # Inner boss
    rboss = 16
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            if dx*dx + dy*dy <= 4:
                draw.ellipse([cx - rboss + dx, cy - rboss + dy, cx + rboss + dx, cy + rboss + dy], fill=c_black)
    draw.ellipse([cx - rboss, cy - rboss, cx + rboss, cy + rboss], fill=c_metal_light)
    draw.ellipse([cx - rboss + 3, cy - rboss + 2, cx + rboss - 5, cy + rboss - 5], fill=(255, 255, 255, 255))
    draw.ellipse([cx + 2, cy + 2, cx + 8, cy + 8], fill=c_metal_dark)

    # Rivets around rim
    for angle_deg in range(0, 360, 45):
        rad = math.radians(angle_deg)
        rx = int(cx + (r - 6) * math.cos(rad))
        ry = int(cy + (r - 6) * math.sin(rad))
        draw.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=c_black)
        draw.point((rx, ry), fill=c_metal_light)

    img.save(path, "PNG")
    print(f"Generated {path}")

def generate_round_shield(path):
    img = create_weapon_image()
    draw = ImageDraw.Draw(img)

    c_black = (20, 20, 20, 255)
    c_metal_light = (255, 255, 255, 255)
    c_metal_mid = (200, 200, 200, 255)
    c_metal_dark = (125, 125, 125, 255)
    c_plank1 = (230, 230, 230, 255)
    c_plank2 = (210, 210, 210, 255)

    cx, cy = 64, 64
    r = 46

    # Base shield circle
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx*dx + dy*dy <= 9:
                draw.ellipse([cx - r + dx, cy - r + dy, cx + r + dx, cy + r + dy], fill=c_black)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c_metal_dark)

    # Planks inside
    draw.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5], fill=c_plank1)
    
    # Wooden plank vertical divider lines
    for px in [38, 52, 64, 76, 90]:
        draw.line([(px, cy - int(math.sqrt(max(0, (r-6)**2 - (px-cx)**2)))),
                   (px, cy + int(math.sqrt(max(0, (r-6)**2 - (px-cx)**2))))],
                  fill=c_metal_dark, width=2)

    # Central Shield Boss
    rboss = 18
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            if dx*dx + dy*dy <= 4:
                draw.ellipse([cx - rboss + dx, cy - rboss + dy, cx + rboss + dx, cy + rboss + dy], fill=c_black)
    draw.ellipse([cx - rboss, cy - rboss, cx + rboss, cy + rboss], fill=c_metal_mid)
    draw.ellipse([cx - rboss + 3, cy - rboss + 2, cx + rboss - 4, cy + rboss - 5], fill=c_metal_light)

    # Rim rivets
    for angle_deg in range(0, 360, 30):
        rad = math.radians(angle_deg)
        rx = int(cx + (r - 4) * math.cos(rad))
        ry = int(cy + (r - 4) * math.sin(rad))
        draw.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=c_black)
        draw.point((rx, ry), fill=c_metal_light)

    img.save(path, "PNG")
    print(f"Generated {path}")

def generate_kite_shield(path):
    img = create_weapon_image()
    draw = ImageDraw.Draw(img)

    c_black = (20, 20, 20, 255)
    c_metal_light = (255, 255, 255, 255)
    c_metal_mid = (200, 200, 200, 255)
    c_metal_dark = (130, 130, 130, 255)
    c_face = (235, 235, 235, 255)

    # Kite shape points (curved top, tapering down to a pointed bottom)
    kite_pts = [
        (34, 22),
        (50, 16),
        (64, 14),
        (78, 16),
        (94, 22),
        (92, 54),
        (82, 82),
        (64, 114), # Bottom tip
        (46, 82),
        (36, 54)
    ]
    draw_thick_outlined_poly(draw, kite_pts, c_metal_dark, outline_width=3)

    # Inner face inset
    inner_pts = [
        (38, 26),
        (50, 20),
        (64, 18),
        (78, 20),
        (90, 26),
        (88, 52),
        (78, 78),
        (64, 106),
        (50, 78),
        (40, 52)
    ]
    draw.polygon(inner_pts, fill=c_face)

    # Central metal cross / heraldic stripe
    draw.line([(64, 18), (64, 106)], fill=c_metal_mid, width=6)
    draw.line([(38, 42), (90, 42)], fill=c_metal_mid, width=6)
    draw.line([(64, 18), (64, 106)], fill=c_metal_light, width=2)
    draw.line([(38, 42), (90, 42)], fill=c_metal_light, width=2)

    # Center boss
    draw.ellipse([58, 36, 70, 48], fill=c_metal_light, outline=c_black, width=2)

    img.save(path, "PNG")
    print(f"Generated {path}")

def generate_tower_shield(path):
    img = create_weapon_image()
    draw = ImageDraw.Draw(img)

    c_black = (20, 20, 20, 255)
    c_metal_light = (255, 255, 255, 255)
    c_metal_mid = (200, 200, 200, 255)
    c_metal_dark = (120, 120, 120, 255)
    c_body = (230, 230, 230, 255)

    # Rectangular curved tower shield
    tower_pts = [
        (32, 18),
        (64, 14),
        (96, 18),
        (96, 110),
        (64, 114),
        (32, 110)
    ]
    draw_thick_outlined_poly(draw, tower_pts, c_metal_dark, outline_width=3)

    # Inner body
    inner_pts = [
        (36, 22),
        (64, 18),
        (92, 22),
        (92, 106),
        (64, 110),
        (36, 106)
    ]
    draw.polygon(inner_pts, fill=c_body)

    # Vertical reinforced spine
    draw.line([(64, 14), (64, 114)], fill=c_metal_dark, width=8)
    draw.line([(64, 14), (64, 114)], fill=c_metal_light, width=3)

    # Corner brackets
    # Top-left, top-right, bottom-left, bottom-right
    for (cx, cy) in [(34, 20), (94, 20), (34, 108), (94, 108)]:
        draw.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=c_metal_mid, outline=c_black, width=1)

    # Heavy rectangular / round central boss
    draw.ellipse([54, 54, 74, 74], fill=c_metal_light, outline=c_black, width=2)
    draw.ellipse([58, 58, 70, 70], fill=c_metal_mid)

    img.save(path, "PNG")
    print(f"Generated {path}")

def main():
    tex_dir = os.path.join(os.path.dirname(__file__), "..", "Textures", "Things", "Item", "Equipment", "WeaponMelee")
    os.makedirs(tex_dir, exist_ok=True)

    generate_halberd(os.path.join(tex_dir, "Halberd.png"))
    generate_morningstar(os.path.join(tex_dir, "Morningstar.png"))
    generate_war_pick(os.path.join(tex_dir, "WarPick.png"))
    generate_scimitar(os.path.join(tex_dir, "Scimitar.png"))
    generate_quarterstaff(os.path.join(tex_dir, "Quarterstaff.png"))

    shield_dir = os.path.join(os.path.dirname(__file__), "..", "Textures", "Things", "Item", "Equipment", "Shield")
    os.makedirs(shield_dir, exist_ok=True)

    generate_buckler(os.path.join(shield_dir, "Buckler.png"))
    generate_round_shield(os.path.join(shield_dir, "RoundShield.png"))
    generate_kite_shield(os.path.join(shield_dir, "KiteShield.png"))
    generate_tower_shield(os.path.join(shield_dir, "TowerShield.png"))

if __name__ == "__main__":
    main()

