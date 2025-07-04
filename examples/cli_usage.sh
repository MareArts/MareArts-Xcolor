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
echo "xcolor image.jpg --colors 8"
echo

# With mask
echo "3. Extract colors with mask:"
echo "xcolor product.jpg --mask mask.png"
echo

# Output to JSON
echo "4. Save results to JSON:"
echo "xcolor image.jpg --output colors.json"
echo

# Batch processing
echo "5. Process multiple images:"
echo "xcolor *.jpg --colors 5"
echo

# Different algorithm
echo "6. Use DBSCAN algorithm:"
echo "xcolor image.jpg --algorithm dbscan"
echo

# Disable preprocessing for speed
echo "7. Fast extraction (no preprocessing):"
echo "xcolor image.jpg --fast"
echo

# Version information
echo "8. Show version:"
echo "xcolor --version"
echo

# Help
echo "9. Show all options:"
echo "xcolor --help"
echo

echo "=== Practical Examples ==="
echo

# E-commerce product color extraction
echo "E-commerce product colors:"
echo 'find ./products -name "*.jpg" -exec xcolor {} --colors 5 --output {}.json \;'
echo

# Brand color extraction
echo "Brand color extraction:"
echo "xcolor logo.png --colors 3 --algorithm dbscan"
echo

# Create color report
echo "Generate color report:"
echo "xcolor image.jpg --colors 10 --output color_report.json"