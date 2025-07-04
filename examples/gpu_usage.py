#!/usr/bin/env python3
"""
GPU acceleration examples for marearts-xcolor package
"""

from marearts_xcolor import ColorExtractor
import time
from pathlib import Path

def check_gpu_availability():
    """Check if GPU is available for acceleration"""
    print("=== GPU Availability Check ===")
    
    try:
        from marearts_xcolor import get_gpu_info, print_gpu_info
        
        # Get GPU information
        gpu_info = get_gpu_info()
        print(f"\nGPU Available: {gpu_info.get('available', False)}")
        
        # Print detailed GPU info
        print_gpu_info()
        
    except ImportError:
        print("\nGPU support not available in this installation.")
        print("Install with: pip install marearts-xcolor[gpu]")

def gpu_modes_example():
    """Demonstrate different GPU modes"""
    print("\n=== GPU Modes Example ===")
    
    image_path = "../sample_images/sample_image.jpg"
    
    # Auto mode (default) - uses GPU if available
    print("\n1. Auto mode (uses GPU if available):")
    try:
        auto_extractor = ColorExtractor(n_colors=5, use_gpu='auto')
        colors = auto_extractor.extract_colors(image_path)
        print(f"   Extracted {len(colors)} colors successfully")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Never mode - always uses CPU
    print("\n2. Never mode (always uses CPU):")
    try:
        cpu_extractor = ColorExtractor(n_colors=5, use_gpu='never')
        colors = cpu_extractor.extract_colors(image_path)
        print(f"   Extracted {len(colors)} colors successfully")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Force mode - requires GPU
    print("\n3. Force mode (requires GPU):")
    try:
        gpu_extractor = ColorExtractor(n_colors=5, use_gpu='force')
        colors = gpu_extractor.extract_colors(image_path)
        print(f"   Extracted {len(colors)} colors successfully with GPU")
    except RuntimeError as e:
        print(f"   Expected error if no GPU: {e}")

def performance_comparison():
    """Compare CPU vs GPU performance"""
    print("\n=== Performance Comparison ===")
    
    image_path = "../sample_images/product_example.jpg"
    
    # CPU timing
    print("\nCPU Performance:")
    cpu_extractor = ColorExtractor(n_colors=10, use_gpu='never', algorithm='kmeans')
    
    start_time = time.time()
    cpu_colors = cpu_extractor.extract_colors(image_path)
    cpu_time = time.time() - start_time
    
    print(f"  Time: {cpu_time:.3f} seconds")
    print(f"  Colors found: {len(cpu_colors)}")
    
    # GPU timing (if available)
    print("\nGPU Performance (if available):")
    try:
        gpu_extractor = ColorExtractor(n_colors=10, use_gpu='auto', algorithm='kmeans')
        
        start_time = time.time()
        gpu_colors = gpu_extractor.extract_colors(image_path)
        gpu_time = time.time() - start_time
        
        print(f"  Time: {gpu_time:.3f} seconds")
        print(f"  Colors found: {len(gpu_colors)}")
        
        if gpu_time < cpu_time:
            speedup = cpu_time / gpu_time
            print(f"  Speedup: {speedup:.2f}x faster than CPU")
    except Exception as e:
        print(f"  GPU not available: {e}")

def batch_processing_gpu():
    """Batch process images with GPU acceleration"""
    print("\n=== Batch Processing with GPU ===")
    
    # Create GPU-accelerated extractor
    extractor = ColorExtractor(n_colors=5, use_gpu='auto')
    
    # Process multiple images
    image_dir = Path("../sample_images")
    images = list(image_dir.glob("*.jpg"))
    images = [img for img in images if "mask" not in img.name]
    
    print(f"\nProcessing {len(images)} images...")
    
    total_start = time.time()
    results = {}
    
    for image_path in images:
        start_time = time.time()
        colors = extractor.extract_colors(str(image_path))
        process_time = time.time() - start_time
        
        results[image_path.name] = {
            'colors': len(colors),
            'time': process_time
        }
        
        print(f"  {image_path.name}: {len(colors)} colors in {process_time:.3f}s")
    
    total_time = time.time() - total_start
    avg_time = total_time / len(images)
    
    print(f"\nTotal time: {total_time:.3f} seconds")
    print(f"Average per image: {avg_time:.3f} seconds")

def gpu_memory_efficient():
    """Demonstrate memory-efficient GPU processing"""
    print("\n=== Memory-Efficient GPU Processing ===")
    
    # Process large images efficiently
    large_image = "../sample_images/product_example.jpg"
    
    # Use different clustering algorithms
    for algorithm in ['kmeans', 'dbscan']:
        print(f"\n{algorithm.upper()} with GPU:")
        
        extractor = ColorExtractor(
            n_colors=8,
            algorithm=algorithm,
            use_gpu='auto',
            preprocessing=True
        )
        
        try:
            start_time = time.time()
            colors = extractor.extract_colors(large_image)
            elapsed = time.time() - start_time
            
            print(f"  Processed in {elapsed:.3f} seconds")
            print(f"  Top 3 colors:")
            for i, color in enumerate(colors[:3]):
                print(f"    {i+1}. {color['hex']} - {color['percentage']:.1f}%")
                
        except Exception as e:
            print(f"  Error: {e}")

def gpu_fallback_example():
    """Demonstrate graceful GPU fallback"""
    print("\n=== GPU Fallback Example ===")
    
    image_path = "../sample_images/sample_image.jpg"
    
    # This will automatically fall back to CPU if GPU is not available
    extractor = ColorExtractor(
        n_colors=5,
        use_gpu='auto',  # Automatic fallback
        algorithm='kmeans'
    )
    
    print("\nExtracting colors with automatic GPU/CPU selection...")
    colors = extractor.extract_colors(image_path)
    
    print(f"Successfully extracted {len(colors)} colors")
    print("Mode: GPU (if available) or CPU (fallback)")
    
    # Show extracted colors
    print("\nExtracted colors:")
    for color in colors:
        print(f"  {color['hex']} - {color['percentage']:.1f}%")

if __name__ == "__main__":
    # Run all GPU examples
    examples = [
        check_gpu_availability,
        gpu_modes_example,
        performance_comparison,
        batch_processing_gpu,
        gpu_memory_efficient,
        gpu_fallback_example
    ]
    
    for example in examples:
        example()
        print("-" * 50)
    
    print("\n✅ All GPU examples completed!")
    print("\nNote: GPU acceleration requires:")
    print("- CUDA-capable GPU")
    print("- Installation with: pip install marearts-xcolor[gpu]")
    print("- Appropriate CUDA drivers")