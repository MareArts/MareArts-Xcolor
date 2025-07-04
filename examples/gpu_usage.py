#!/usr/bin/env python3
"""
GPU-accelerated color extraction examples for marearts-xcolor
Demonstrates automatic GPU detection and fallback mechanisms
"""

from marearts_xcolor import (
    ColorExtractor,
    ColorExtractorGPU,
    is_gpu_available,
    get_gpu_info,
    print_gpu_info,
    GPU_SUPPORT
)
import numpy as np
import time

def check_gpu_availability():
    """Check and display GPU availability"""
    print("=== GPU Availability Check ===")
    
    if not GPU_SUPPORT:
        print("❌ GPU support not installed")
        print("To enable GPU support, install:")
        print("  pip install cupy-cuda11x")
        print("  pip install cuml-cu11")
        return False
        
    print(f"✅ GPU support module available")
    
    if is_gpu_available():
        print("✅ GPU hardware detected")
        print("\nGPU Information:")
        print_gpu_info()
        return True
    else:
        print("❌ No GPU hardware detected")
        print("The package will automatically use CPU")
        return False

def basic_gpu_usage():
    """Basic GPU-accelerated color extraction"""
    print("\n=== Basic GPU Usage ===")
    
    if not GPU_SUPPORT:
        print("GPU support not available, using CPU version")
        extractor = ColorExtractor()
    else:
        # This automatically uses GPU if available, CPU if not
        extractor = ColorExtractorGPU(use_gpu='auto')
        print(f"Using device: {extractor.device}")
    
    # Load your image
    image_path = "../sample_images/sample_image.jpg"
    
    # For this example, we'll use a generated image
    image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
    
    # Extract colors
    colors = extractor.extract_colors(image, num_colors=5)
    
    print("\nExtracted colors:")
    for i, color in enumerate(colors):
        print(f"  Color {i+1}: {color['hex']} ({color['percentage']:.1f}%)")

def gpu_mode_examples():
    """Examples of different GPU modes"""
    print("\n=== GPU Mode Examples ===")
    
    if not GPU_SUPPORT:
        print("GPU support not available")
        return
    
    # Test image
    image = np.random.randint(0, 255, (720, 1280, 3), dtype=np.uint8)
    
    # 1. Auto mode (default) - uses GPU if available
    print("\n1. Auto mode (recommended):")
    extractor_auto = ColorExtractorGPU(use_gpu='auto')
    print(f"   Device: {extractor_auto.device}")
    colors = extractor_auto.extract_colors(image, num_colors=3)
    print(f"   Found {len(colors)} colors")
    
    # 2. Force GPU mode - errors if GPU not available
    print("\n2. Force GPU mode:")
    try:
        extractor_force = ColorExtractorGPU(use_gpu='force')
        print(f"   Device: {extractor_force.device}")
        colors = extractor_force.extract_colors(image, num_colors=3)
        print(f"   Found {len(colors)} colors")
    except RuntimeError as e:
        print(f"   Error: {e}")
    
    # 3. Never use GPU - always uses CPU
    print("\n3. CPU-only mode:")
    extractor_cpu = ColorExtractorGPU(use_gpu='never')
    print(f"   Device: {extractor_cpu.device}")
    colors = extractor_cpu.extract_colors(image, num_colors=3)
    print(f"   Found {len(colors)} colors")

def performance_comparison():
    """Compare GPU vs CPU performance"""
    print("\n=== Performance Comparison ===")
    
    if not GPU_SUPPORT or not is_gpu_available():
        print("GPU not available for comparison")
        return
    
    # Test with different image sizes
    test_cases = [
        (480, 640, "Small (VGA)"),
        (1080, 1920, "Medium (Full HD)"),
        (2160, 3840, "Large (4K)")
    ]
    
    for height, width, name in test_cases:
        print(f"\n{name} - {width}x{height}:")
        
        # Generate test image
        image = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        
        # CPU timing
        cpu_extractor = ColorExtractor()
        start = time.time()
        cpu_colors = cpu_extractor.extract_colors(image, num_colors=5)
        cpu_time = time.time() - start
        
        # GPU timing
        gpu_extractor = ColorExtractorGPU(use_gpu='auto')
        start = time.time()
        gpu_colors = gpu_extractor.extract_colors(image, num_colors=5)
        gpu_time = time.time() - start
        
        # Results
        speedup = cpu_time / gpu_time if gpu_time > 0 else 0
        print(f"  CPU time: {cpu_time:.3f}s")
        print(f"  GPU time: {gpu_time:.3f}s")
        print(f"  Speedup: {speedup:.1f}x")

def batch_processing_gpu():
    """Batch processing with GPU acceleration"""
    print("\n=== Batch Processing with GPU ===")
    
    if not GPU_SUPPORT:
        print("Using CPU for batch processing")
        extractor = ColorExtractor()
    else:
        print("Using GPU for batch processing")
        extractor = ColorExtractorGPU(use_gpu='auto')
        print(f"Device: {extractor.device}")
    
    # Process multiple images
    num_images = 10
    image_size = (720, 1280, 3)
    
    print(f"\nProcessing {num_images} images of size {image_size[1]}x{image_size[0]}...")
    
    start_time = time.time()
    
    for i in range(num_images):
        # Generate test image (in real use, load your images)
        image = np.random.randint(0, 255, image_size, dtype=np.uint8)
        
        # Extract colors
        colors = extractor.extract_colors(image, num_colors=5)
        
        # Show progress
        print(f"  Image {i+1}/{num_images} - Top color: {colors[0]['hex']}")
    
    total_time = time.time() - start_time
    avg_time = total_time / num_images
    
    print(f"\nBatch processing complete:")
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Average per image: {avg_time:.3f}s")
    print(f"  Images per second: {1/avg_time:.1f}")

def advanced_gpu_features():
    """Advanced GPU features and settings"""
    print("\n=== Advanced GPU Features ===")
    
    if not GPU_SUPPORT or not is_gpu_available():
        print("GPU not available")
        return
    
    # Create extractor with custom settings
    extractor = ColorExtractorGPU(
        method='kmeans',
        n_clusters=7,
        use_gpu='auto',
        preprocessing=True,
        use_lab_space=True
    )
    
    print(f"Configuration:")
    print(f"  Device: {extractor.device}")
    print(f"  Method: {extractor.method}")
    print(f"  Preprocessing: {extractor.preprocessing}")
    print(f"  Color space: {'LAB' if extractor.use_lab_space else 'RGB'}")
    
    # Run benchmark
    print("\nRunning benchmark...")
    benchmark_results = extractor.benchmark(
        image_sizes=[(720, 1280), (1080, 1920)]
    )
    
    print("\nBenchmark Results:")
    for size, data in benchmark_results['benchmarks'].items():
        mp_per_sec = data['pixels'] / data['time_seconds'] / 1e6
        print(f"  {size}: {data['time_seconds']:.3f}s ({mp_per_sec:.1f} MP/s)")

def main():
    """Run all GPU examples"""
    print("MareArts XColor - GPU Acceleration Examples\n")
    
    # Check GPU availability first
    gpu_available = check_gpu_availability()
    
    # Run examples
    basic_gpu_usage()
    
    if GPU_SUPPORT:
        gpu_mode_examples()
        performance_comparison()
        batch_processing_gpu()
        
        if gpu_available:
            advanced_gpu_features()
    
    print("\n=== Examples Complete ===")
    print("\nKey Points:")
    print("- GPU acceleration is automatic when available")
    print("- Falls back to CPU seamlessly")
    print("- Use 'auto' mode for best compatibility")
    print("- Force mode for GPU-required applications")
    print("- Significant speedup for large images and batches")

if __name__ == "__main__":
    main()