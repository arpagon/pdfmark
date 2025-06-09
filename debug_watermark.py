#!/usr/bin/env python3

import sys
from watermark import create_watermark_image
from PIL import Image

def debug_watermark():
    """Debug the watermark generation process."""
    
    # Test with small dimensions first
    width, height = 400, 300
    wave_frequency = 4
    opacity = 0.8  # High opacity for debugging
    text = "CONFIDENCIAL"
    
    print(f"Creating watermark with:")
    print(f"  Size: {width}x{height}")
    print(f"  Frequency: {wave_frequency}")
    print(f"  Opacity: {opacity}")
    print(f"  Text: '{text}'")
    
    # Generate watermark
    watermark = create_watermark_image(width, height, wave_frequency, opacity, text)
    
    # Save for inspection
    watermark.save('output/debug_watermark.png')
    print(f"Debug watermark saved to: output/debug_watermark.png")
    
    # Analyze the image
    pixels_with_alpha = 0
    total_pixels = width * height
    
    for y in range(height):
        for x in range(width):
            pixel = watermark.getpixel((x, y))
            if len(pixel) == 4 and pixel[3] > 0:  # Has alpha > 0
                pixels_with_alpha += 1
    
    print(f"Analysis:")
    print(f"  Total pixels: {total_pixels}")
    print(f"  Pixels with alpha > 0: {pixels_with_alpha}")
    print(f"  Coverage: {(pixels_with_alpha/total_pixels)*100:.2f}%")
    
    if pixels_with_alpha == 0:
        print("ERROR: No visible pixels found in watermark!")
        
        # Debug the mask generation separately
        from watermark import create_wave_text_lines
        mask = create_wave_text_lines(width, height, wave_frequency, text)
        mask.save('output/debug_mask.png')
        print("Debug mask saved to: output/debug_mask.png")
        
        # Analyze mask
        mask_pixels = 0
        for y in range(height):
            for x in range(width):
                if mask.getpixel((x, y)) > 0:
                    mask_pixels += 1
        
        print(f"Mask analysis:")
        print(f"  Mask pixels > 0: {mask_pixels}")
        print(f"  Mask coverage: {(mask_pixels/total_pixels)*100:.2f}%")
    
    return pixels_with_alpha > 0

if __name__ == "__main__":
    debug_watermark()