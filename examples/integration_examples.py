#!/usr/bin/env python3
"""
Integration examples showing how to use marearts-xcolor with other libraries
"""

from marearts_xcolor import ColorExtractor
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import json
from pathlib import Path

def matplotlib_visualization():
    """Create visualizations using matplotlib"""
    print("=== Matplotlib Integration ===")
    
    extractor = ColorExtractor(n_colors=6)
    
    # Extract colors
    image_path = "../sample_images/sample_image.jpg"
    colors = extractor.extract_colors(image_path)
    
    # Create pie chart of color distribution
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Pie chart
    percentages = [c['percentage'] for c in colors]
    hex_colors = [c['hex'] for c in colors]
    
    ax1.pie(percentages, labels=hex_colors, colors=hex_colors, autopct='%1.1f%%')
    ax1.set_title('Color Distribution')
    
    # Color swatches
    y_pos = np.arange(len(colors))
    ax2.barh(y_pos, percentages, color=hex_colors)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(hex_colors)
    ax2.set_xlabel('Percentage')
    ax2.set_title('Color Percentages')
    
    plt.tight_layout()
    plt.savefig('color_visualization.png', dpi=150, bbox_inches='tight')
    print("Visualization saved to color_visualization.png")
    plt.close()

def pillow_palette_generation():
    """Generate color palettes using PIL/Pillow"""
    print("\n=== Pillow Integration ===")
    
    extractor = ColorExtractor(n_colors=5)
    
    # Extract colors from multiple images
    images = ["sample_image.jpg", "product_example.jpg", "color_test_image.jpg"]
    
    # Create combined palette
    palette_width = 800
    palette_height = 200
    swatch_width = palette_width // 5
    
    combined_image = Image.new('RGB', (palette_width, palette_height * len(images)), 'white')
    draw = ImageDraw.Draw(combined_image)
    
    for img_idx, image_name in enumerate(images):
        image_path = f"../sample_images/{image_name}"
        colors = extractor.extract_colors(image_path)
        
        y_offset = img_idx * palette_height
        
        # Draw color swatches
        for i, color in enumerate(colors):
            x1 = i * swatch_width
            x2 = (i + 1) * swatch_width
            y1 = y_offset
            y2 = y_offset + palette_height - 30
            
            # Draw swatch
            draw.rectangle([x1, y1, x2, y2], fill=color['hex'])
            
            # Add text
            text = f"{color['hex']}\n{color['percentage']:.1f}%"
            text_bbox = draw.textbbox((0, 0), text)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = x1 + (swatch_width - text_width) // 2
            draw.text((text_x, y2 + 5), text, fill='black')
        
        # Add image name
        draw.text((10, y_offset + 10), image_name, fill='white')
    
    combined_image.save('combined_palette.png')
    print("Combined palette saved to combined_palette.png")

def pandas_color_analysis():
    """Analyze colors using pandas DataFrame"""
    print("\n=== Pandas Integration ===")
    
    extractor = ColorExtractor(n_colors=5)
    
    # Collect color data from multiple images
    data = []
    
    for image_file in Path("../sample_images").glob("*.jpg"):
        if "mask" not in image_file.name:
            colors = extractor.extract_colors(str(image_file))
            
            for rank, color in enumerate(colors, 1):
                data.append({
                    'image': image_file.name,
                    'rank': rank,
                    'hex': color['hex'],
                    'r': color['rgb'][0],
                    'g': color['rgb'][1],
                    'b': color['rgb'][2],
                    'percentage': color['percentage'],
                    'luminance': 0.299*color['rgb'][0] + 0.587*color['rgb'][1] + 0.114*color['rgb'][2]
                })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Analysis
    print("\nColor Analysis Summary:")
    print(f"Total colors extracted: {len(df)}")
    print(f"Average percentage per color: {df['percentage'].mean():.2f}%")
    print(f"Most common color rank 1: {df[df['rank']==1]['hex'].mode().iloc[0]}")
    
    # Group by luminance
    df['brightness'] = pd.cut(df['luminance'], bins=[0, 85, 170, 255], labels=['Dark', 'Medium', 'Bright'])
    brightness_dist = df.groupby('brightness')['percentage'].sum()
    
    print("\nBrightness Distribution:")
    print(brightness_dist)
    
    # Save to CSV
    df.to_csv('color_analysis.csv', index=False)
    print("\nDetailed analysis saved to color_analysis.csv")

def web_color_scheme_generator():
    """Generate web color schemes"""
    print("\n=== Web Color Scheme Generator ===")
    
    extractor = ColorExtractor(n_colors=6)
    
    image_path = "../sample_images/product_example.jpg"
    colors = extractor.extract_colors(image_path)
    
    # Generate color scheme
    scheme = {
        'primary': colors[0]['hex'] if len(colors) > 0 else '#000000',
        'secondary': colors[1]['hex'] if len(colors) > 1 else '#666666',
        'accent': colors[2]['hex'] if len(colors) > 2 else '#999999',
        'background': '#ffffff',
        'text': '#000000'
    }
    
    # Determine text color based on primary color luminance
    primary_rgb = colors[0]['rgb'] if colors else [0, 0, 0]
    luminance = 0.299*primary_rgb[0] + 0.587*primary_rgb[1] + 0.114*primary_rgb[2]
    scheme['text'] = '#ffffff' if luminance < 128 else '#000000'
    
    # Generate CSS
    css_template = """
/* Color Scheme from {image} */
:root {{
    --primary: {primary};
    --secondary: {secondary};
    --accent: {accent};
    --background: {background};
    --text: {text};
}}

.button-primary {{
    background-color: var(--primary);
    color: {text};
}}

.button-secondary {{
    background-color: var(--secondary);
    color: var(--text);
}}

.accent-text {{
    color: var(--accent);
}}
"""
    
    css_content = css_template.format(image=image_path, **scheme)
    
    with open('color_scheme.css', 'w') as f:
        f.write(css_content)
    
    print(f"Web color scheme generated:")
    for key, value in scheme.items():
        print(f"  {key}: {value}")
    print("\nCSS saved to color_scheme.css")

def json_api_response():
    """Simulate API response format"""
    print("\n=== JSON API Response Format ===")
    
    # Simulate API endpoint
    def color_extraction_api(image_path, n_colors=5, **kwargs):
        try:
            extractor = ColorExtractor(n_colors=n_colors, **kwargs)
            colors = extractor.extract_colors(image_path)
            
            response = {
                'status': 'success',
                'data': {
                    'image': image_path,
                    'parameters': kwargs,
                    'colors': colors,
                    'metadata': {
                        'total_colors': len(colors),
                        'dominant_color': colors[0] if colors else None,
                        'palette_diversity': len(set(c['hex'] for c in colors))
                    }
                }
            }
        except Exception as e:
            response = {
                'status': 'error',
                'error': str(e),
                'data': None
            }
        
        return response
    
    # Example API calls
    responses = []
    
    # Successful extraction
    response1 = color_extraction_api(
        "../sample_images/sample_image.jpg",
        n_colors=5,
        preprocessing=True
    )
    responses.append(response1)
    
    # With preprocessing disabled
    response2 = color_extraction_api(
        "../sample_images/product_example.jpg",
        n_colors=3,
        preprocessing=False
    )
    responses.append(response2)
    
    # Save API responses
    with open('api_responses.json', 'w') as f:
        json.dump(responses, f, indent=2)
    
    print("API responses saved to api_responses.json")
    print(f"Response 1 status: {response1['status']}")
    print(f"Response 2 status: {response2['status']}")

def batch_processing_pipeline():
    """Create a batch processing pipeline"""
    print("\n=== Batch Processing Pipeline ===")
    
    # Pipeline configuration
    pipeline_config = {
        'input_dir': '../sample_images',
        'output_dir': 'batch_output',
        'settings': {
            'n_colors': 5,
            'preprocessing': True
        }
    }
    
    # Create output directory
    output_dir = Path(pipeline_config['output_dir'])
    output_dir.mkdir(exist_ok=True)
    
    # Process images
    results = []
    
    for image_file in Path(pipeline_config['input_dir']).glob("*.jpg"):
        if "mask" not in image_file.name:
            print(f"Processing: {image_file.name}")
            
            # Extract colors
            extractor = ColorExtractor(**pipeline_config['settings'])
            colors = extractor.extract_colors(str(image_file))
            
            # Save individual result
            result = {
                'filename': image_file.name,
                'colors': colors,
                'timestamp': pd.Timestamp.now().isoformat()
            }
            results.append(result)
            
            # Save color palette
            palette_path = output_dir / f"{image_file.stem}_palette.json"
            with open(palette_path, 'w') as f:
                json.dump(colors, f, indent=2)
    
    # Save batch results
    batch_report = {
        'config': pipeline_config,
        'total_processed': len(results),
        'results': results
    }
    
    with open(output_dir / 'batch_report.json', 'w') as f:
        json.dump(batch_report, f, indent=2)
    
    print(f"\nBatch processing complete!")
    print(f"Processed {len(results)} images")
    print(f"Results saved to {output_dir}/")

if __name__ == "__main__":
    # Run all integration examples
    examples = [
        matplotlib_visualization,
        pillow_palette_generation,
        pandas_color_analysis,
        web_color_scheme_generator,
        json_api_response,
        batch_processing_pipeline
    ]
    
    for example in examples:
        example()
        print("-" * 50)
    
    print("\n✅ All integration examples completed!")