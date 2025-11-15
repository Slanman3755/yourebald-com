# generate_images_parabolic_band_realistic_full_head_taller_top.py
from PIL import Image, ImageDraw
import random
import os
import math

# --- Configuration ---
BASE_IMAGE_PATH = 'Rays_Bald.png' 
OUTPUT_DIR = 'generated_images' 
NUM_OUTPUT_IMAGES = 100
HAIRS_PER_STEP = 50   # Used from your last input: Increased for denser hair
MAX_TOTAL_HAIRS = NUM_OUTPUT_IMAGES * HAIRS_PER_STEP 

# --- Hair Styling Parameters ---
# Subtle blonde highlights re-added to a light brown dominant palette
HAIR_COLOR_PALETTE = [
    (139, 105, 78, 200),  # Light Brown (more frequent)
    (150, 105, 68, 200),  # Warm Light Brown (more frequent)
    (178, 134, 98, 200),  # Light Chestnut Brown (more frequent)
    (200, 170, 120, 200), # Dark Blonde/Dirty Blonde (subtle highlight)
    (210, 180, 140, 200), # Tan/Ash Blonde (subtle highlight)
    (225, 205, 155, 200), # Soft Golden Blonde (new addition for subtle highlight)
    (100, 70, 40, 200),   # Medium Brown for depth
    (78, 43, 22, 200),    # Darker Brown for stronger depth
    (0, 0, 0, 150)        # Very sparse, slightly transparent dark strands for shadow/root effect
]
HAIR_WIDTH = 1
HAIR_LENGTH_MIN = 20  # Longer hair
HAIR_LENGTH_MAX = 40  # Longer hair
HAIR_SWAY_X_RANGE = (-0.5, 0.5)  # Less extreme horizontal sway for more structured growth
HAIR_GROW_Y_RANGE = (-0.5, 1.5)  # Allow more growth downwards/outwards for better head coverage

# --- Define the Head Drawing Area (The Parabolic Band) ---
# Used previous values and ADJUSTED BAND_WIDTH to make the top taller
HEAD_CENTER_X_RATIO = 0.47 
HEAD_LOWEST_Y_RATIO = 0.26   
HEAD_BAND_WIDTH_Y_RATIO = 0.15
HEAD_RADIUS_X_RATIO = 0.25   
HEAD_HEIGHT_Y_RATIO = 0.12

# Global list to store ALL hair data generated so far
ALL_HAIR_STRANDS_DATA = []

def generate_new_hair_position(img_width, img_height, current_hair_index):
    """
    Generates a single hair position within the parabolic band area.
    """
    center_x = int(img_width * HEAD_CENTER_X_RATIO)
    lowest_y = int(img_height * HEAD_LOWEST_Y_RATIO) 
    width_x = int(img_width * HEAD_RADIUS_X_RATIO)
    height_y = int(img_height * HEAD_HEIGHT_Y_RATIO)
    band_width_y = int(img_height * HEAD_BAND_WIDTH_Y_RATIO) 

    a_coefficient = height_y / (width_x ** 2)
    
    start_x = random.randint(center_x - width_x, center_x + width_x)
    
    x_relative = start_x - center_x
    
    y_lower_parabola = lowest_y + (a_coefficient * (x_relative ** 2))
    
    y_upper_parabola = y_lower_parabola - band_width_y
    
    start_y = random.randint(int(min(y_upper_parabola, y_lower_parabola)), 
                             int(max(y_upper_parabola, y_lower_parabola)))
    
    noise_range = int(height_y // 15)
    start_y += random.randint(-noise_range, noise_range)
    
    length = random.randint(HAIR_LENGTH_MIN, HAIR_LENGTH_MAX)
    end_x = int(start_x + length * random.uniform(*HAIR_SWAY_X_RANGE)) 
    end_y = int(start_y + length * random.uniform(*HAIR_GROW_Y_RANGE)) 
    
    return (start_x, start_y, end_x, end_y)


def generate_and_save_image(base_img_path, output_file_path, target_hairs, img_width, img_height):
    """
    Generates and draws new hair positions dynamically up to the target_hairs count.
    """
    global ALL_HAIR_STRANDS_DATA 
    
    try:
        img = Image.open(base_img_path).convert("RGBA")
    except FileNotFoundError:
        print(f"Error: Base image not found at '{base_img_path}'.")
        return False

    draw = ImageDraw.Draw(img)
    
    hairs_to_generate = target_hairs - len(ALL_HAIR_STRANDS_DATA)
    
    for i in range(hairs_to_generate):
        new_hair_data = generate_new_hair_position(
            img_width, img_height, len(ALL_HAIR_STRANDS_DATA) + 1
        )
        ALL_HAIR_STRANDS_DATA.append(new_hair_data)

    for start_x, start_y, end_x, end_y in ALL_HAIR_STRANDS_DATA:
        random_hair_color = random.choice(HAIR_COLOR_PALETTE) 
        draw.line([(start_x, start_y), (end_x, end_y)], fill=random_hair_color, width=HAIR_WIDTH)
            
    img.save(output_file_path, 'PNG')
    print(f"Generated: {output_file_path} (Contains {len(ALL_HAIR_STRANDS_DATA)} hairs)")
    return True

# --- Main Execution Block ---
if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: '{OUTPUT_DIR}'")

    try:
        temp_img = Image.open(BASE_IMAGE_PATH)
        img_width, img_height = temp_img.size
        temp_img.close()
    except FileNotFoundError:
        print(f"Critical Error: Base image '{BASE_IMAGE_PATH}' not found. Check file name and location.")
        exit(1)

    print(f"\nStarting to generate {NUM_OUTPUT_IMAGES} images (each step adding {HAIRS_PER_STEP} hairs) dynamically into a parabolic band...")
    
    final_image_count = 0
    for i in range(1, NUM_OUTPUT_IMAGES + 1): 
        filename = f'image_{i:03d}.png' 
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        target_hairs = i * HAIRS_PER_STEP
        
        if not generate_and_save_image(BASE_IMAGE_PATH, output_path, target_hairs, img_width, img_height):
            print("Image generation stopped due to an error.")
            break 
        final_image_count = i

    print(f"\nFinished generating {len(ALL_HAIR_STRANDS_DATA)} total hair positions across {final_image_count} images in '{OUTPUT_DIR}'.")