#!/usr/bin/env python3
"""
Basic usage examples for marearts-xcolor package
"""

from marearts_xcolor import ColorExtractor
import json
from pathlib import Path

def basic_color_extraction():
    """Basic color extraction example"""
    print("=== Basic Color Extraction ===")
    
    # Create extractor with default settings
    extractor = ColorExtractor()
    
    # Extract colors from image
    image_path = "../sample_images/sample_image.jpg"
    colors = extractor.extract_colors(image_path, num_colors=5)
    
    # Display results
    print(f"\nExtracted {len(colors)} dominant colors:")
    for i, color in enumerate(colors, 1):
        print(f"\nColor {i}:")
        print(f"  RGB: {color['rgb']}")
        print(f"  HEX: {color['hex']}")
        print(f"  Percentage: {color['percentage']:.2f}%")

def extraction_with_preprocessing():
    """Color extraction with and without preprocessing"""
    print("\n=== Preprocessing Comparison ===")
    
    image_path = "../sample_images/product_example.jpg"
    
    # Without preprocessing
    extractor_no_prep = ColorExtractor(preprocessing=False)
    colors_no_prep = extractor_no_prep.extract_colors(image_path, num_colors=5)
    
    # With preprocessing (default)
    extractor_prep = ColorExtractor(preprocessing=True)
    colors_prep = extractor_prep.extract_colors(image_path, num_colors=5)
    
    print("\nWithout preprocessing:")
    for color in colors_no_prep[:3]:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")
    
    print("\nWith preprocessing (better for varied lighting):")
    for color in colors_prep[:3]:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")

def different_clustering_methods():
    """Compare K-means and DBSCAN clustering"""
    print("\n=== Clustering Methods Comparison ===")
    
    image_path = "../sample_images/color_test_image.jpg"
    
    # K-means clustering
    kmeans_extractor = ColorExtractor(algorithm='kmeans')
    kmeans_colors = kmeans_extractor.extract_colors(image_path, num_colors=5)
    
    # DBSCAN clustering
    dbscan_extractor = ColorExtractor(algorithm='dbscan')
    dbscan_colors = dbscan_extractor.extract_colors(image_path, num_colors=5)
    
    print("\nK-means results (good for uniform distribution):")
    for color in kmeans_colors:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")
    
    print("\nDBSCAN results (good for distinct color regions):")
    for color in dbscan_colors:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")

def color_space_comparison():
    """Compare RGB vs LAB color space extraction"""
    print("\n=== Color Space Comparison ===")
    
    image_path = "../sample_images/sample_image.jpg"
    
    # RGB color space
    rgb_extractor = ColorExtractor(lab_space=False)
    rgb_colors = rgb_extractor.extract_colors(image_path, num_colors=5)
    
    # LAB color space (perceptually uniform)
    lab_extractor = ColorExtractor(lab_space=True)
    lab_colors = lab_extractor.extract_colors(image_path, num_colors=5)
    
    print("\nRGB color space:")
    for color in rgb_colors[:3]:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")
    
    print("\nLAB color space (more perceptually accurate):")
    for color in lab_colors[:3]:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")

def extraction_with_mask():
    """Extract colors from specific regions using mask"""
    print("\n=== Masked Color Extraction ===")
    
    extractor = ColorExtractor()
    
    # Extract colors from masked region
    image_path = "../sample_images/product_example.jpg"
    mask_path = "../sample_images/sample_mask.jpg"
    
    colors = extractor.extract_colors(
        image_path=image_path,
        mask_path=mask_path,
        num_colors=5
    )
    
    print(f"\nColors from masked region only:")
    for color in colors:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")

def batch_processing():
    """Process multiple images efficiently"""
    print("\n=== Batch Processing ===")
    
    extractor = ColorExtractor()
    results = {}
    
    # Process all images in directory
    image_dir = Path("../sample_images")
    for image_file in image_dir.glob("*.jpg"):
        if "mask" not in image_file.name:  # Skip mask files
            colors = extractor.extract_colors(str(image_file), num_colors=3)
            results[image_file.name] = colors
            
            print(f"\n{image_file.name}:")
            for color in colors:
                print(f"  {color['hex']} - {color['percentage']:.1f}%")
    
    # Save results to JSON
    with open("batch_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to batch_results.json")

def save_color_palette():
    """Save extracted colors as palette image"""
    print("\n=== Save Color Palette ===")
    
    extractor = ColorExtractor()
    
    # Extract colors
    image_path = "../sample_images/sample_image.jpg"
    colors = extractor.extract_colors(image_path, num_colors=6)
    
    # Save palette image
    output_path = "extracted_palette.png"
    extractor.save_palette(colors, output_path, width=600, height=100)
    print(f"\nColor palette saved to: {output_path}")
    
    # Also save as JSON
    with open("extracted_colors.json", "w") as f:
        json.dump(colors, f, indent=2)
    print(f"Color data saved to: extracted_colors.json")

def quality_settings():
    """Demonstrate different quality settings"""
    print("\n=== Quality Settings ===")
    
    image_path = "../sample_images/product_example.jpg"
    
    # Low quality - fast
    low_extractor = ColorExtractor()
    low_colors = low_extractor.extract_colors(image_path, quality='low', num_colors=5)
    
    # High quality - accurate
    high_extractor = ColorExtractor()
    high_colors = high_extractor.extract_colors(image_path, quality='high', num_colors=5)
    
    print("\nLow quality (fast):")
    for color in low_colors[:3]:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")
    
    print("\nHigh quality (more accurate):")
    for color in high_colors[:3]:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")

if __name__ == "__main__":
    # Run all examples
    examples = [
        basic_color_extraction,
        extraction_with_preprocessing,
        different_clustering_methods,
        color_space_comparison,
        extraction_with_mask,
        batch_processing,
        save_color_palette,
        quality_settings
    ]
    
    for example in examples:
        example()
        print("-" * 50)
    
    print("\n✅ All examples completed!")