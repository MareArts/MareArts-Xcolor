# MareArts XColor Examples

This directory contains comprehensive examples demonstrating how to use the marearts-xcolor package.

## 📁 Example Files

### 1. **basic_usage.py**
Basic examples for getting started:
- Simple color extraction
- Preprocessing comparison
- Different clustering methods (K-means vs DBSCAN)
- Color space comparison (RGB vs LAB)
- Masked region extraction
- Batch processing
- Saving color palettes
- Quality settings

### 2. **gpu_usage.py**
GPU acceleration examples:
- GPU detection and availability checking
- Performance comparison (CPU vs GPU)
- Different GPU modes (auto, force, never)
- Batch processing with GPU
- Handling GPU fallback scenarios

### 3. **advanced_usage.py**
Advanced features and analysis:
- Performance benchmarking
- Color distribution analysis
- Color harmony detection
- Multi-image color comparison
- Comprehensive color reports
- Custom preprocessing pipelines
- Color palette exports (CSS, SCSS)

### 4. **integration_examples.py**
Integration with other libraries:
- Matplotlib visualizations
- PIL/Pillow palette generation
- Pandas data analysis
- Web color scheme generation
- JSON API response formatting
- Batch processing pipelines

### 5. **cli_usage.sh**
Command-line interface examples:
- Basic CLI commands
- Advanced options
- Batch processing
- Output formats

## 🚀 Running the Examples

### Prerequisites
```bash
# Install marearts-xcolor
pip install marearts-xcolor

# For GPU examples (optional)
pip install marearts-xcolor[gpu]

# For integration examples
pip install matplotlib pandas pillow
```

### Running Individual Examples
```bash
cd examples

# Run basic examples
python basic_usage.py

# Run GPU examples
python gpu_usage.py

# Run advanced examples
python advanced_usage.py

# Run integration examples
python integration_examples.py

# Run CLI examples
bash cli_usage.sh
```

## 📊 Example Output

Each example creates various output files:
- **Color palettes**: PNG images with extracted colors
- **JSON reports**: Detailed color analysis data
- **CSV files**: Tabular color data for analysis
- **CSS/SCSS files**: Web-ready color variables
- **Visualizations**: Charts and graphs of color distribution

## 💡 Tips

1. **Start Simple**: Begin with `basic_usage.py` to understand core functionality
2. **Check GPU**: Run GPU detection in `gpu_usage.py` before using GPU acceleration
3. **Customize**: Modify examples to fit your specific use case
4. **Performance**: Use quality settings appropriate for your needs
5. **Integration**: See `integration_examples.py` for working with other tools

## 🔍 Common Use Cases

### E-commerce Product Colors
```python
from marearts_xcolor import ColorExtractor

extractor = ColorExtractor(preprocessing=True)
colors = extractor.extract_colors("product.jpg", num_colors=5)
```

### Brand Color Analysis
```python
# Extract and compare brand colors across images
extractor = ColorExtractor(lab_space=True)
colors = extractor.extract_colors("logo.jpg", num_colors=3)
```

### Batch Processing
```python
# Process multiple images efficiently
for image in images:
    colors = extractor.extract_colors(image, quality='medium')
```

## 📝 Notes

- All examples use relative paths assuming you're in the `examples/` directory
- Sample images are provided in the `sample_images/` directory
- GPU examples will automatically fall back to CPU if GPU is not available
- Modify parameters to experiment with different settings

## 🤝 Contributing

Feel free to submit additional examples or improvements via pull requests!

## 📄 License

These examples are part of the marearts-xcolor package and are licensed under the MIT License.