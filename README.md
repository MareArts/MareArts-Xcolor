# MareArts XColor - Customer Repository

Welcome to the **MareArts XColor** customer repository! This repository contains examples, tutorials, and documentation for using the `marearts-xcolor` Python package.

## Installation

Install the package from PyPI:

```bash
pip install marearts-xcolor
```

## Quick Start

```python
from marearts_xcolor import ColorExtractor

# Create extractor instance
extractor = ColorExtractor()

# Extract colors from an image
colors = extractor.extract_colors("your_image.jpg", num_colors=5)

# Print dominant colors
for color in colors:
    print(f"RGB: {color['rgb']}, Percentage: {color['percentage']:.2f}%")
```

## Repository Structure

- `examples/` - Complete usage examples
- `tutorials/` - Step-by-step tutorials
- `sample_images/` - Test images for experimentation
- `docs/` - Additional documentation

## Features

- **High Performance**: Optimized Cython implementation with C++ backend
- **Multiple Algorithms**: K-means and DBSCAN clustering support
- **Color Space Support**: RGB, LAB, HSV color spaces
- **Advanced Preprocessing**: CLAHE and bilateral filtering
- **CLI Interface**: Command-line tools for batch processing
- **Cross-Platform**: Windows, macOS, Linux support (x86_64 + ARM64)

## Package Information

- **PyPI Package**: `marearts-xcolor`
- **Python Versions**: 3.9, 3.10, 3.11, 3.12
- **Architectures**: x86_64, ARM64
- **License**: MIT

## Links

- [PyPI Package](https://pypi.org/project/marearts-xcolor/)
- [Package Documentation](https://github.com/marearts/marearts-xcolor)
- [Issue Tracker](https://github.com/marearts/marearts-xcolor/issues)

## Examples

Browse the `examples/` directory for:
- Basic color extraction
- Advanced configuration options
- Batch processing workflows
- Integration with other libraries
- Performance optimization tips

## Support

For questions, bug reports, or feature requests, please use the [GitHub Issues](https://github.com/marearts/marearts-xcolor/issues).