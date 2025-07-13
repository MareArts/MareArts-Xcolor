# MareArts XColor

**High-performance color extraction library for Python**

[![PyPI version](https://badge.fury.io/py/marearts-xcolor.svg)](https://badge.fury.io/py/marearts-xcolor)
[![Python Support](https://img.shields.io/pypi/pyversions/marearts-xcolor.svg)](https://pypi.org/project/marearts-xcolor/)
[![Downloads](https://pepy.tech/badge/marearts-xcolor)](https://pepy.tech/project/marearts-xcolor)
[![Platform Support](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)](https://pypi.org/project/marearts-xcolor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MareArts XColor is a powerful color extraction library that uses advanced clustering algorithms to extract dominant colors from images. It features both CPU and GPU acceleration, multiple color space support, and intelligent preprocessing for accurate color analysis.

## 🚀 Installation

### For CPU Users (Most Common)
```bash
pip install marearts-xcolor
```

### For GPU Users (Advanced Performance)
```bash
# For CUDA 11.x
pip install marearts-xcolor[gpu] cupy-cuda11x

# For CUDA 12.x  
pip install marearts-xcolor[gpu] cupy-cuda12x
```

## 📋 Requirements

- Python 3.9, 3.10, 3.11, or 3.12
- Operating System: Windows, macOS, or Linux
- Architecture: x86_64 or ARM64

## 🎯 Quick Start

### Basic Usage

```python
from marearts_xcolor import ColorExtractor

# Create extractor instance
extractor = ColorExtractor()

# Extract 5 dominant colors from an image
colors = extractor.extract_colors("your_image.jpg")

# Print results
for color in colors:
    print(f"RGB: {color['rgb']}, Percentage: {color['percentage']:.2f}%")
```

### Advanced Usage with GPU

```python
from marearts_xcolor import ColorExtractor

# Enable GPU acceleration (automatically falls back to CPU if unavailable)
extractor = ColorExtractor(
    n_colors=7,
    algorithm='dbscan',
    lab_space=True,
    use_gpu='auto'
)

# Extract colors
colors = extractor.extract_colors("image.jpg")
```

### Command Line Interface

```bash
# Basic usage
xcolor image.jpg --colors 5

# Advanced options
xcolor image.jpg --colors 8 --algorithm dbscan --fast

# Batch processing
xcolor *.jpg --output results.json --gpu auto
```

## 🌟 Key Features

### 🎨 Color Extraction
- **Multiple Algorithms**: K-means and DBSCAN clustering
- **Color Spaces**: RGB and LAB support
- **Smart Preprocessing**: CLAHE enhancement and bilateral filtering
- **Accurate Results**: Perceptually uniform color extraction

### ⚡ Performance
- **GPU Acceleration**: Optional CUDA support for 10-50x speedup
- **Optimized Implementation**: Cython-compiled with C++ backend
- **Smart Fallback**: Automatic CPU fallback when GPU unavailable
- **Batch Processing**: Efficient processing of multiple images

### 🛠️ Flexibility
- **Pure Python API**: Easy integration with existing projects
- **Mask Support**: Extract colors from specific regions
- **Color Similarity**: Find similar colors using perceptual metrics
- **Export Options**: JSON, CSV, and image outputs

## 📚 Examples

### Extract Colors from Product Images

```python
from marearts_xcolor import ColorExtractor
import json

extractor = ColorExtractor(n_colors=5, use_gpu='auto')

# Analyze product image
colors = extractor.extract_colors("product.jpg")

# Save results
with open('product_colors.json', 'w') as f:
    json.dump(colors, f, indent=2)
```

### Batch Process Multiple Images

```python
import glob
from marearts_xcolor import ColorExtractor

extractor = ColorExtractor(n_colors=5, use_gpu='auto')

# Process all images in directory
for image_path in glob.glob("images/*.jpg"):
    colors = extractor.extract_colors(image_path)
    print(f"\n{image_path}:")
    for color in colors:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")
```

### Color Similarity Analysis

```python
from marearts_xcolor import ColorExtractor

# Extract colors from reference image
extractor_ref = ColorExtractor(n_colors=5)
reference_colors = extractor_ref.extract_colors("reference.jpg")

# Extract more colors from target image
extractor_target = ColorExtractor(n_colors=10)
target_colors = extractor_target.extract_colors("target.jpg")

# Analyze similarity
for ref_color in reference_colors:
    similar = extractor.find_similar_colors(
        ref_color['rgb'], 
        target_colors,
        threshold=10.0  # Delta-E threshold
    )
    print(f"Similar to {ref_color['hex']}: {len(similar)} colors found")
```

## 🏗️ Repository Structure

```
marearts-xcolor/
├── examples/           # Complete code examples
│   ├── README.md          # Examples documentation
│   ├── basic_usage.py     # Simple color extraction
│   ├── gpu_usage.py       # GPU acceleration examples
│   ├── advanced_usage.py  # Advanced features
│   ├── integration_examples.py  # Integration with other libraries
│   └── cli_usage.sh       # Command-line examples
└── sample_images/      # Test images
    ├── sample_image.jpg
    ├── product_example.jpg
    ├── color_test_image.jpg
    └── sample_mask.jpg
```

## 🔧 Configuration Options

| Parameter | Options | Description |
|-----------|---------|-------------|
| `n_colors` | int (e.g., 1-20) | Number of colors to extract |
| `algorithm` | 'kmeans', 'dbscan' | Clustering algorithm |
| `lab_space` | True/False | Use LAB color space (True) or RGB (False) |
| `use_gpu` | 'auto', 'force', 'never' | GPU acceleration mode |
| `preprocessing` | True/False | Enable CLAHE enhancement and bilateral filtering |

## 💡 Tips for Best Results

1. **Use LAB color space** for perceptually accurate colors
2. **Enable preprocessing** for images with poor lighting
3. **GPU acceleration** provides significant speedup for large images
4. **DBSCAN clustering** works better for images with distinct color regions

## 🐛 Troubleshooting

### GPU not detected?
```python
# Check GPU availability
from marearts_xcolor.gpu_utils import get_gpu_info
print(get_gpu_info())
```

### Installation issues?
```bash
# For CPU-only installation
pip install marearts-xcolor --no-deps
pip install numpy opencv-python scikit-learn pillow matplotlib scipy

# Verify installation
python -c "import marearts_xcolor; print(marearts_xcolor.__version__)"
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🔗 Links

- [PyPI Package](https://pypi.org/project/marearts-xcolor/)
- [GitHub Repository](https://github.com/marearts/marearts-xcolor)
- [MareArts Homepage](https://marearts.com)
- [Live Test](https://live.marearts.com)

## MareArts Solutions
- [Autpmatic Number Plate Recognition](https://github.com/MareArts/MareArts-ANPR)
- [MareArts Reatime Video & Image Stiching](https://github.com/MareArts/MareArts-MAST)
- [MareArts Dominent Color Extraction](https://github.com/marearts/marearts-xcolor)

## 📞 Support

For questions or support:
- Email: support@marearts.com

---

**Made with ❤️ by MareArts**