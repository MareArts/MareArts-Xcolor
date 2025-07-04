#!/usr/bin/env python3
"""
Basic usage example for marearts-xcolor package
"""

from marearts_xcolor import ColorExtractor
import cv2
import numpy as np
from pathlib import Path

def basic_color_extraction():
    """Basic color extraction example"""
    print("=== Basic Color Extraction ===")
    
    # Create extractor instance
    extractor = ColorExtractor()
    
    # Extract colors from image
    image_path = "../sample_images/sample_image.jpg"
    colors = extractor.extract_colors(image_path, num_colors=5)
    
    # Display results
    print(f"\nExtracted {len(colors)} dominant colors from {image_path}:")
    for i, color in enumerate(colors, 1):
        print(f"\nColor {i}:")
        print(f"  RGB: {color['rgb']}")
        print(f"  HEX: {color['hex']}")
        print(f"  Percentage: {color['percentage']:.2f}%")

def advanced_color_extraction():
    """Advanced color extraction with configuration"""
    print("\n=== Advanced Color Extraction ===")
    
    # Create extractor with custom settings
    extractor = ColorExtractor(
        method='kmeans',
        n_clusters=7,
        preprocessing=True,
        use_lab_space=True
    )
    
    # Extract with mask
    image_path = "../sample_images/product_example.jpg"
    mask_path = "../sample_images/sample_mask.jpg"
    
    colors = extractor.extract_colors(
        image_path,
        mask_path=mask_path,
        num_colors=7,
        quality='high'
    )
    
    print(f"\nExtracted colors with mask from {image_path}:")
    for color in colors:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")

def batch_processing_example():
    """Batch processing multiple images"""
    print("\n=== Batch Processing Example ===")
    
    extractor = ColorExtractor()
    
    # Process all images in directory
    image_dir = Path("../sample_images")
    for image_file in image_dir.glob("*.jpg"):
        print(f"\nProcessing: {image_file.name}")
        colors = extractor.extract_colors(str(image_file), num_colors=3)
        
        # Show top 3 colors
        top_colors = [f"{c['hex']} ({c['percentage']:.1f}%)" for c in colors[:3]]
        print(f"  Top colors: {', '.join(top_colors)}")

def color_similarity_example():
    """Color similarity analysis example"""
    print("\n=== Color Similarity Analysis ===")
    
    extractor = ColorExtractor()
    
    # Define brand colors
    brand_colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
    ]
    
    # Extract colors from image
    image_path = "../sample_images/color_test_image.jpg"
    extracted_colors = extractor.extract_colors(image_path, num_colors=5)
    
    print(f"\nFinding similar brand colors in {image_path}:")
    
    # Find similar colors
    for brand_rgb in brand_colors:
        similar = extractor.find_similar_colors(
            extracted_colors,
            brand_rgb,
            threshold=50.0
        )
        
        if similar:
            print(f"\nBrand color RGB{brand_rgb} found similar colors:")
            for color in similar:
                print(f"  {color['hex']} - Distance: {color['distance']:.2f}")
        else:
            print(f"\nNo similar colors found for RGB{brand_rgb}")

def visualization_example():
    """Create color palette visualization"""
    print("\n=== Color Palette Visualization ===")
    
    extractor = ColorExtractor()
    
    # Extract colors
    image_path = "../sample_images/sample_image.jpg"
    colors = extractor.extract_colors(image_path, num_colors=6)
    
    # Create color palette image
    palette_height = 100
    color_width = 150
    palette_width = color_width * len(colors)
    
    palette = np.zeros((palette_height, palette_width, 3), dtype=np.uint8)
    
    for i, color in enumerate(colors):
        start_x = i * color_width
        end_x = (i + 1) * color_width
        palette[:, start_x:end_x] = color['rgb']
        
        # Add percentage text
        text = f"{color['percentage']:.1f}%"
        cv2.putText(palette, text, (start_x + 10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Save palette
    output_path = "color_palette.png"
    cv2.imwrite(output_path, cv2.cvtColor(palette, cv2.COLOR_RGB2BGR))
    print(f"\nColor palette saved to: {output_path}")

if __name__ == "__main__":
    # Run all examples
    basic_color_extraction()
    advanced_color_extraction()
    batch_processing_example()
    color_similarity_example()
    visualization_example()
    
    print("\n=== All examples completed! ===")