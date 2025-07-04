#!/bin/bash
# CLI usage examples for marearts-xcolor

echo "=== MareArts XColor CLI Examples ==="
echo

# Basic usage
echo "1. Basic color extraction:"
echo "xcolor image.jpg"
echo

# Specify number of colors
echo "2. Extract specific number of colors:"
echo "xcolor image.jpg -n 8"
echo

# With mask
echo "3. Extract colors with mask:"
echo "xcolor product.jpg -m mask.png"
echo

# Output to JSON
echo "4. Save results to JSON:"
echo "xcolor image.jpg -o colors.json"
echo

# Batch processing
echo "5. Process multiple images:"
echo "xcolor *.jpg -n 5 --batch"
echo

# Different algorithm
echo "6. Use DBSCAN algorithm:"
echo "xcolor image.jpg --method dbscan"
echo

# High quality mode
echo "7. High quality extraction:"
echo "xcolor image.jpg --quality high"
echo

# Find similar colors
echo "8. Find similar colors to RGB value:"
echo "xcolor image.jpg --similar 255,0,0 --threshold 30"
echo

# Help
echo "9. Show all options:"
echo "xcolor --help"
echo

echo "=== Practical Examples ==="
echo

# E-commerce product color extraction
echo "E-commerce product colors:"
echo 'find ./products -name "*.jpg" -exec xcolor {} -n 5 -o {}.json \;'
echo

# Brand color matching
echo "Brand color matching:"
echo "xcolor logo.png --similar 34,139,34 --threshold 20"
echo

# Create color report
echo "Generate color report:"
echo "xcolor image.jpg --format report > color_report.txt"