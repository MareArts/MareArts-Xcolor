#!/usr/bin/env python3
"""
Advanced usage examples for marearts-xcolor package
"""

from marearts_xcolor import ColorExtractor
import numpy as np
import cv2
import json
from pathlib import Path
import time

def performance_comparison():
    """Compare performance with different settings"""
    print("=== Performance Comparison ===")
    
    image_path = "../sample_images/product_example.jpg"
    
    # Test different quality settings
    for quality in ['low', 'medium', 'high']:
        extractor = ColorExtractor()
        
        start_time = time.time()
        colors = extractor.extract_colors(image_path, num_colors=5, quality=quality)
        elapsed_time = time.time() - start_time
        
        print(f"\nQuality: {quality}")
        print(f"  Time: {elapsed_time:.3f} seconds")
        print(f"  Colors found: {len(colors)}")

def color_distribution_analysis():
    """Analyze color distribution in image"""
    print("\n=== Color Distribution Analysis ===")
    
    extractor = ColorExtractor(lab_space=True)
    
    image_path = "../sample_images/color_test_image.jpg"
    colors = extractor.extract_colors(image_path, num_colors=8)
    
    # Analyze distribution
    total_percentage = sum(color['percentage'] for color in colors)
    
    print(f"\nColor distribution for {image_path}:")
    print(f"Total coverage: {total_percentage:.1f}%")
    
    # Group by dominance
    dominant = [c for c in colors if c['percentage'] > 15]
    secondary = [c for c in colors if 5 <= c['percentage'] <= 15]
    accent = [c for c in colors if c['percentage'] < 5]
    
    print(f"\nDominant colors (>15%):")
    for color in dominant:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")
    
    print(f"\nSecondary colors (5-15%):")
    for color in secondary:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")
    
    print(f"\nAccent colors (<5%):")
    for color in accent:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")

def color_harmony_detection():
    """Detect color harmonies in extracted colors"""
    print("\n=== Color Harmony Detection ===")
    
    extractor = ColorExtractor()
    
    image_path = "../sample_images/sample_image.jpg"
    colors = extractor.extract_colors(image_path, num_colors=6)
    
    # Convert to HSV for harmony analysis
    hsv_colors = []
    for color in colors:
        rgb = np.array(color['rgb']).reshape(1, 1, 3).astype(np.uint8)
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)[0, 0]
        hsv_colors.append({
            'hex': color['hex'],
            'hue': hsv[0] * 2,  # OpenCV uses 0-180 for hue
            'saturation': hsv[1] / 255 * 100,
            'value': hsv[2] / 255 * 100,
            'percentage': color['percentage']
        })
    
    print("\nExtracted colors in HSV:")
    for color in hsv_colors:
        print(f"  {color['hex']}: H={color['hue']:.0f}°, S={color['saturation']:.0f}%, V={color['value']:.0f}%")
    
    # Check for complementary colors (180° apart)
    print("\nChecking for color harmonies:")
    for i, color1 in enumerate(hsv_colors):
        for color2 in hsv_colors[i+1:]:
            hue_diff = abs(color1['hue'] - color2['hue'])
            if hue_diff > 180:
                hue_diff = 360 - hue_diff
            
            if 170 <= hue_diff <= 190:
                print(f"  Complementary: {color1['hex']} and {color2['hex']}")
            elif 110 <= hue_diff <= 130:
                print(f"  Triadic: {color1['hex']} and {color2['hex']}")
            elif 25 <= hue_diff <= 35:
                print(f"  Analogous: {color1['hex']} and {color2['hex']}")

def multi_image_color_comparison():
    """Compare colors across multiple images"""
    print("\n=== Multi-Image Color Comparison ===")
    
    extractor = ColorExtractor()
    
    # Extract colors from multiple images
    image_files = list(Path("../sample_images").glob("*.jpg"))
    image_files = [f for f in image_files if "mask" not in f.name][:3]  # First 3 non-mask images
    
    all_colors = {}
    for image_file in image_files:
        colors = extractor.extract_colors(str(image_file), num_colors=3)
        all_colors[image_file.name] = colors
    
    # Find common colors across images
    print("\nTop 3 colors per image:")
    for filename, colors in all_colors.items():
        print(f"\n{filename}:")
        for color in colors:
            print(f"  {color['hex']} - {color['percentage']:.1f}%")
    
    # Calculate average color
    all_rgb_values = []
    for colors in all_colors.values():
        for color in colors:
            all_rgb_values.append(color['rgb'])
    
    if all_rgb_values:
        avg_color = np.mean(all_rgb_values, axis=0).astype(int)
        avg_hex = '#{:02x}{:02x}{:02x}'.format(*avg_color)
        print(f"\nAverage color across all images: {avg_hex} RGB{tuple(avg_color)}")

def create_color_report():
    """Generate comprehensive color analysis report"""
    print("\n=== Comprehensive Color Report ===")
    
    image_path = "../sample_images/product_example.jpg"
    
    # Extract with different methods
    results = {}
    
    # K-means analysis
    kmeans_extractor = ColorExtractor(algorithm='kmeans', preprocessing=True)
    kmeans_colors = kmeans_extractor.extract_colors(image_path, num_colors=5)
    
    # DBSCAN analysis
    dbscan_extractor = ColorExtractor(algorithm='dbscan', preprocessing=True)
    dbscan_colors = dbscan_extractor.extract_colors(image_path, num_colors=5)
    
    # Prepare report
    report = {
        'image': image_path,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'analysis': {
            'kmeans': {
                'colors': kmeans_colors,
                'dominant_color': kmeans_colors[0] if kmeans_colors else None,
                'palette_diversity': len(set(c['hex'] for c in kmeans_colors))
            },
            'dbscan': {
                'colors': dbscan_colors,
                'dominant_color': dbscan_colors[0] if dbscan_colors else None,
                'palette_diversity': len(set(c['hex'] for c in dbscan_colors))
            }
        },
        'statistics': {
            'total_colors_found': len(set(c['hex'] for c in kmeans_colors + dbscan_colors)),
            'common_colors': []
        }
    }
    
    # Find common colors between methods
    kmeans_hexes = {c['hex'] for c in kmeans_colors}
    dbscan_hexes = {c['hex'] for c in dbscan_colors}
    common_hexes = kmeans_hexes & dbscan_hexes
    
    report['statistics']['common_colors'] = list(common_hexes)
    
    # Save report
    report_path = "color_analysis_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport saved to: {report_path}")
    print(f"Total unique colors found: {report['statistics']['total_colors_found']}")
    print(f"Colors common to both methods: {len(common_hexes)}")

def custom_preprocessing_example():
    """Example with custom preprocessing pipeline"""
    print("\n=== Custom Preprocessing Example ===")
    
    # Load image manually for custom preprocessing
    image_path = "../sample_images/sample_image.jpg"
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Apply custom preprocessing
    # 1. Denoise
    denoised = cv2.fastNlMeansDenoisingColored(image_rgb, None, 10, 10, 7, 21)
    
    # 2. Enhance contrast
    lab = cv2.cvtColor(denoised, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    enhanced = cv2.merge([l, a, b])
    enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)
    
    # Save preprocessed image
    cv2.imwrite("preprocessed_image.jpg", cv2.cvtColor(enhanced_rgb, cv2.COLOR_RGB2BGR))
    
    # Extract colors from preprocessed image
    extractor = ColorExtractor(preprocessing=False)  # Already preprocessed
    colors = extractor.extract_colors("preprocessed_image.jpg", num_colors=5)
    
    print("\nColors from custom preprocessed image:")
    for color in colors:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")

def color_palette_export():
    """Export color palettes in various formats"""
    print("\n=== Color Palette Export ===")
    
    extractor = ColorExtractor()
    
    image_path = "../sample_images/color_test_image.jpg"
    colors = extractor.extract_colors(image_path, num_colors=6)
    
    # Export as different formats
    
    # 1. CSS variables
    css_vars = ":root {\n"
    for i, color in enumerate(colors):
        css_vars += f"  --color-{i+1}: {color['hex']};\n"
    css_vars += "}"
    
    with open("colors.css", "w") as f:
        f.write(css_vars)
    print("\nCSS variables saved to colors.css")
    
    # 2. SCSS map
    scss_map = "$colors: (\n"
    for i, color in enumerate(colors):
        scss_map += f"  'color-{i+1}': {color['hex']},\n"
    scss_map = scss_map.rstrip(',\n') + "\n);"
    
    with open("colors.scss", "w") as f:
        f.write(scss_map)
    print("SCSS map saved to colors.scss")
    
    # 3. Adobe Swatch Exchange (ASE) format hint
    print("\nFor Adobe Swatch Exchange (.ase) format, use:")
    for i, color in enumerate(colors):
        print(f"  Color {i+1}: RGB({color['rgb'][0]}, {color['rgb'][1]}, {color['rgb'][2]})")

if __name__ == "__main__":
    # Run all advanced examples
    examples = [
        performance_comparison,
        color_distribution_analysis,
        color_harmony_detection,
        multi_image_color_comparison,
        create_color_report,
        custom_preprocessing_example,
        color_palette_export
    ]
    
    for example in examples:
        example()
        print("-" * 50)
    
    print("\n✅ All advanced examples completed!")