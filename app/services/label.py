
import os, datetime
from typing import Tuple
import qrcode
from PIL import Image, ImageDraw, ImageFont
from ..settings import get_settings

settings = get_settings()

def ensure_output_dir():
    os.makedirs(settings.LABEL_OUTPUT_DIR, exist_ok=True)

def build_payload(rem_id, material, thickness_mm, width_mm, height_mm, location_code):
    return f"{rem_id} | {material} | {thickness_mm}mm | {int(width_mm)}x{int(height_mm)} | {location_code}"

def render_label_png(rem_id, material, thickness_mm, width_mm, height_mm, location_code)->str:
    ensure_output_dir()
    payload = build_payload(rem_id, material, thickness_mm, width_mm, height_mm, location_code)
    # QR
    qr = qrcode.QRCode(box_size=4, border=1)
    qr.add_data(payload)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Canvas ~ 500x300 px (approx 50x30mm at ~254 dpi). Keep simple.
    W, H = 500, 300
    canvas = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(canvas)
    # Paste QR
    qr_size = 250
    qr_img = qr_img.resize((qr_size, qr_size))
    canvas.paste(qr_img, (20, (H-qr_size)//2))

    # Text block
    lines = [
        f"ID: {rem_id}",
        f"{material} / {thickness_mm} mm",
        f"Size: {int(width_mm)} x {int(height_mm)} mm",
        f"Loc: {location_code}",
        datetime.date.today().isoformat(),
    ]
    x = 300; y = 20; line_h = 48
    for i, line in enumerate(lines):
        draw.text((x, y + i*line_h), line, fill="black")

    out_path = os.path.join(settings.LABEL_OUTPUT_DIR, f"{rem_id}.png")
    canvas.save(out_path)
    return out_path
