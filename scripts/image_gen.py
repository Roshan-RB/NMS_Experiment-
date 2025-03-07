from PIL import Image, ImageDraw, ImageFont
import random

def generate_image_with_text(output_path=r"C:\Thesis\Dataprep\output\output.png"):
    # Create a blank white image
    img_width, img_height = 800, 600
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)
    
    # Define words and their frequencies
    words = {"mango": 5, "banana": 3, "strawberry": 2, "orange": 1}
    
    # Load a default font (adjust font size as needed)
    try:
        font = ImageFont.truetype("arial.ttf", 24)  # Windows
    except:
        font = ImageFont.load_default()  # Fallback font
    
    # Randomly place words on the image
    placed_positions = []
    for word, count in words.items():
        for _ in range(count):
            while True:
                x = random.randint(20, img_width - 100)
                y = random.randint(20, img_height - 30)
                
                # Check if position overlaps significantly with existing ones
                if not any(abs(px - x) < 50 and abs(py - y) < 20 for px, py in placed_positions):
                    draw.text((x, y), word, fill="black", font=font)
                    placed_positions.append((x, y))
                    break
    
    # Save the image
    img.save(output_path)
    print(f"Image saved as {output_path}")

# Run the function
generate_image_with_text()
