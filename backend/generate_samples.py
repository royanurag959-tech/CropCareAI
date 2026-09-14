import os
from PIL import Image, ImageDraw, ImageFilter

def generate_sample_images():
    output_dirs = [
        os.path.abspath("C:/Users/royan/.gemini/antigravity/scratch/cropcare-ai/frontend/public/sample_leaves"),
        os.path.abspath("C:/Users/royan/.gemini/antigravity/scratch/cropcare-ai/backend/sample_leaves")
    ]
    for d in output_dirs:
        os.makedirs(d, exist_ok=True)

    samples = [
        ("sample_tomato_blight.jpg", (34, 139, 34), [(120, 150, 40, (139, 69, 19)), (240, 280, 55, (105, 45, 12)), (180, 320, 35, (160, 82, 45))], "Tomato Leaf Blight"),
        ("sample_potato_blight.jpg", (46, 125, 50), [(150, 180, 50, (78, 52, 46)), (220, 260, 45, (62, 39, 35))], "Potato Early Blight"),
        ("sample_rice_blast.jpg", (56, 142, 60), [(200, 150, 60, (93, 64, 55)), (180, 310, 45, (120, 80, 60))], "Rice Blast"),
        ("sample_apple_scab.jpg", (43, 114, 51), [(160, 160, 45, (46, 52, 34)), (250, 230, 40, (55, 60, 40))], "Apple Scab"),
        ("sample_corn_spot.jpg", (67, 160, 71), [(170, 140, 65, (141, 110, 99)), (210, 300, 55, (109, 76, 65))], "Corn Leaf Spot"),
        ("sample_tomato_healthy.jpg", (46, 160, 67), [], "Healthy Tomato Leaf"),
        ("sample_unclear_leaf.jpg", (120, 140, 120), [], "Blurry / Unclear Leaf")
    ]

    for filename, base_color, spots, label in samples:
        img = Image.new("RGB", (400, 400), color=(240, 243, 238))
        draw = ImageDraw.Draw(img)

        # Draw leaf outline / shape
        if "unclear" in filename:
            # Low contrast / blurry shape
            draw.ellipse([80, 80, 320, 320], fill=(130, 150, 130))
            img = img.filter(ImageFilter.GaussianBlur(radius=8))
        else:
            # Elegant pointed leaf shape
            draw.chord([60, 50, 340, 350], start=30, end=330, fill=base_color, outline=(20, 90, 20), width=3)
            # Main central vein
            draw.line([(200, 70), (200, 340)], fill=(76, 175, 80), width=4)
            # Lateral veins
            for y in range(110, 320, 35):
                draw.line([(200, y), (120, y - 25)], fill=(76, 175, 80), width=2)
                draw.line([(200, y), (280, y - 25)], fill=(76, 175, 80), width=2)

            # Disease necrotic spots
            for sx, sy, radius, spot_color in spots:
                # Concentric target circles
                draw.ellipse([sx - radius, sy - radius, sx + radius, sy + radius], fill=(218, 165, 32), outline=(139, 69, 19))
                draw.ellipse([sx - radius + 8, sy - radius + 8, sx + radius - 8, sy + radius - 8], fill=spot_color)
                draw.ellipse([sx - radius + 16, sy - radius + 16, sx + radius - 16, sy + radius - 16], fill=(50, 25, 10))

        # Save to both target locations
        for d in output_dirs:
            target_file = os.path.join(d, filename)
            img.save(target_file, "JPEG", quality=90)
            print(f"Generated sample image: {target_file}")

if __name__ == "__main__":
    generate_sample_images()
