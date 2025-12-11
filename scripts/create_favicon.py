from PIL import Image, ImageDraw
import os

def create_robot_favicon():
    # Create a 32x32 image for the favicon
    size = (32, 32)
    image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Draw robot body (simplified)
    # Head
    draw.rectangle([10, 8, 22, 18], fill=(68, 93, 72, 255), outline=(44, 62, 80, 255), width=1)

    # Eyes
    draw.ellipse([12, 10, 14, 12], fill=(231, 76, 61, 255))
    draw.ellipse([18, 10, 20, 12], fill=(231, 76, 61, 255))

    # Body
    draw.rectangle([12, 18, 20, 26], fill=(52, 73, 94, 255), outline=(44, 62, 80, 255), width=1)

    # AI symbol
    draw.ellipse([14, 5, 18, 9], outline=(52, 152, 219, 255), width=1)
    # Simple circuit pattern
    draw.line([10, 22, 12, 22], fill=(52, 152, 219, 255), width=1)
    draw.line([20, 22, 22, 22], fill=(52, 152, 219, 255), width=1)

    return image

def create_larger_logo():
    # Create a 192x192 image for larger displays
    size = (192, 192)
    image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Draw a more detailed robot
    # Head
    draw.rounded_rectangle([56, 40, 136, 100], radius=8, fill=(68, 93, 72, 255), outline=(44, 62, 80, 255), width=2)

    # Eyes
    draw.ellipse([72, 56, 88, 72], fill=(231, 76, 61, 255))
    draw.ellipse([104, 56, 120, 72], fill=(231, 76, 61, 255))

    # Mouth
    draw.rounded_rectangle([92, 84, 100, 87], radius=1, fill=(236, 240, 241, 255))

    # Body
    draw.rounded_rectangle([64, 100, 128, 150], radius=4, fill=(52, 73, 94, 255), outline=(44, 62, 80, 255), width=2)

    # Arms
    draw.rounded_rectangle([44, 108, 64, 116], radius=4, fill=(52, 73, 94, 255), outline=(44, 62, 80, 255), width=1)
    draw.rounded_rectangle([128, 108, 148, 116], radius=4, fill=(52, 73, 94, 255), outline=(44, 62, 80, 255), width=1)

    # Legs
    draw.rectangle([76, 150, 86, 175], fill=(44, 62, 80, 255))
    draw.rectangle([106, 150, 116, 175], fill=(44, 62, 80, 255))

    # AI/Brain symbol
    draw.ellipse([88, 28, 104, 44], outline=(52, 152, 219, 255), width=2)
    # Draw a simple neural network pattern
    draw.line([92, 36, 100, 30], fill=(52, 152, 219, 255), width=1)
    draw.line([92, 36, 100, 42], fill=(52, 152, 219, 255), width=1)
    draw.line([100, 30, 100, 42], fill=(52, 152, 219, 255), width=1)

    # Circuit pattern
    draw.arc([52, 120, 68, 136], start=0, end=180, fill=(52, 152, 219, 255), width=1)
    draw.arc([124, 120, 140, 136], start=0, end=180, fill=(52, 152, 219, 255), width=1)

    return image

if __name__ == "__main__":
    # Create favicon
    favicon = create_robot_favicon()
    favicon.save("docs/static/img/favicon.ico")

    # Create larger logo for PWA
    large_logo = create_larger_logo()
    large_logo.save("docs/static/img/logo-192.png")

    print("Favicon and logo created successfully!")