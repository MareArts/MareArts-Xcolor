#!/usr/bin/env python3
"""
Real-time webcam color extraction with beautiful visualization
"""

import cv2
import numpy as np
from marearts_xcolor import ColorExtractor
import time
import threading
from typing import List, Dict


class WebcamColorExtractor:
    def __init__(self, n_colors: int = 5, record_video: bool = False):
        self.n_colors = n_colors
        self.extractor = ColorExtractor(n_colors=n_colors, preprocessing=True)
        self.current_colors = []
        self.last_extraction_time = 0
        self.extraction_interval = 0.1  # Extract colors every 0.1 seconds for real-time
        self.extraction_thread = None
        self.roi_for_extraction = None
        self.extraction_lock = threading.Lock()
        self.circle_radius = 50  # Even bigger circle
        
        # Video recording settings
        self.record_video = record_video
        self.video_writer = None
        self.video_start_time = None
        self.video_segment_duration = 30  # 30 seconds per segment
        self.video_segment_count = 1
        self.recording_active = False
        
    def get_xor_color(self, background_color: tuple) -> tuple:
        """Calculate XOR color for visibility against background"""
        # Convert to int to avoid numpy scalar issues
        r, g, b = int(background_color[0]), int(background_color[1]), int(background_color[2])
        
        # Simple XOR approach
        xor_r = 255 - r
        xor_g = 255 - g  
        xor_b = 255 - b
        
        # Ensure good contrast
        if abs(xor_r - r) + abs(xor_g - g) + abs(xor_b - b) < 300:
            # If not enough contrast, use white or black
            if (r + g + b) / 3 > 127:
                return (0, 0, 0)  # Black on light background
            else:
                return (255, 255, 255)  # White on dark background
        
        return (xor_r, xor_g, xor_b)
    
    def extract_roi_from_circle(self, frame: np.ndarray) -> np.ndarray:
        """Extract ROI rectangle around the circle"""
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        
        # Create square ROI around circle
        x1 = max(0, center_x - self.circle_radius)
        y1 = max(0, center_y - self.circle_radius)
        x2 = min(width, center_x + self.circle_radius)
        y2 = min(height, center_y + self.circle_radius)
        
        # Extract ROI
        roi = frame[y1:y2, x1:x2]
        return roi
    
    def extract_colors_async(self, frame: np.ndarray):
        """Extract colors from ROI in a separate thread"""
        if self.extraction_thread and self.extraction_thread.is_alive():
            return
        
        # Extract small ROI around circle
        roi = self.extract_roi_from_circle(frame)
        if roi.size == 0:
            return
            
        self.roi_for_extraction = roi.copy()
        
        def extract():
            try:
                # Use fallback k-means directly on small ROI for speed
                self.fallback_color_extraction()
            except Exception as e:
                print(f"Color extraction error: {e}")
        
        self.extraction_thread = threading.Thread(target=extract)
        self.extraction_thread.daemon = True
        self.extraction_thread.start()
    
    def fallback_color_extraction(self):
        """Fast color extraction using OpenCV k-means on ROI"""
        try:
            if self.roi_for_extraction is None or self.roi_for_extraction.size == 0:
                return
                
            # Reshape ROI for k-means
            data = self.roi_for_extraction.reshape((-1, 3))
            data = np.float32(data)
            
            # Apply k-means with fewer iterations for speed
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 5, 1.0)
            k = min(self.n_colors, len(data))  # Don't exceed number of pixels
            if k < 1:
                return
                
            _, labels, centers = cv2.kmeans(data, k, None, criteria, 3, cv2.KMEANS_RANDOM_CENTERS)
            
            # Convert centers to uint8 and count labels
            centers = np.uint8(centers)
            unique_labels, counts = np.unique(labels, return_counts=True)
            
            # Create color list
            colors = []
            total_pixels = len(labels)
            
            for label, count in zip(unique_labels, counts):
                b, g, r = centers[label]
                percentage = (count / total_pixels) * 100
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                
                colors.append({
                    'rgb': (int(r), int(g), int(b)),
                    'hex': hex_color,
                    'percentage': percentage
                })
            
            # Sort by percentage
            colors.sort(key=lambda x: x['percentage'], reverse=True)
            
            with self.extraction_lock:
                self.current_colors = colors[:self.n_colors]
                self.last_extraction_time = time.time()
                
        except Exception as e:
            print(f"ROI color extraction error: {e}")
    
    def hex_to_bgr(self, hex_color) -> tuple:
        """Convert hex color to BGR tuple"""
        # Handle different input types
        if isinstance(hex_color, tuple):
            # Already RGB tuple, convert to BGR
            if len(hex_color) >= 3:
                return (int(hex_color[2]), int(hex_color[1]), int(hex_color[0]))
            return (0, 0, 0)
        
        if not isinstance(hex_color, str):
            return (0, 0, 0)
            
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            return (0, 0, 0)  # Return black for invalid hex
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (b, g, r)  # OpenCV uses BGR
        except ValueError:
            return (0, 0, 0)  # Return black for invalid hex
    
    def hex_to_rgb(self, hex_color) -> tuple:
        """Convert hex color to RGB tuple"""
        # Handle different input types
        if isinstance(hex_color, tuple):
            # Already RGB tuple
            if len(hex_color) >= 3:
                return (int(hex_color[0]), int(hex_color[1]), int(hex_color[2]))
            return (0, 0, 0)
        
        if not isinstance(hex_color, str):
            return (0, 0, 0)
            
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            return (0, 0, 0)  # Return black for invalid hex
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (r, g, b)
        except ValueError:
            return (0, 0, 0)  # Return black for invalid hex
    
    def rgb_to_hex(self, rgb_color) -> str:
        """Convert RGB tuple to hex string"""
        if isinstance(rgb_color, tuple) and len(rgb_color) >= 3:
            r, g, b = int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2])
            return f"#{r:02x}{g:02x}{b:02x}"
        return "#000000"
    
    def draw_color_table(self, frame: np.ndarray, colors: List[Dict]) -> np.ndarray:
        """Draw beautiful color table on the frame"""
        if not colors:
            return frame
        
        _, width = frame.shape[:2]
        
        # Table dimensions with larger header
        table_width = 350
        table_height = 70 + len(colors) * 50
        table_x = width - table_width - 20
        table_y = 20
        
        # Draw table background with rounded corners effect
        overlay = frame.copy()
        cv2.rectangle(overlay, (table_x, table_y), (table_x + table_width, table_y + table_height), 
                     (40, 40, 40), -1)
        
        # Add transparency
        cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)
        
        # Draw table header with professional styling
        cv2.rectangle(frame, (table_x, table_y), (table_x + table_width, table_y + 50), 
                     (45, 45, 45), -1, cv2.LINE_AA)
        
        # Professional title with better font
        cv2.putText(frame, "DOMINANT COLORS", (table_x + 15, table_y + 20), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Subtitle with library branding
        cv2.putText(frame, "Powered by MareArts-Xcolor", (table_x + 15, table_y + 38), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.35, (180, 180, 180), 1, cv2.LINE_AA)
        
        # Draw color entries
        for i, color in enumerate(colors):
            y_pos = table_y + 60 + i * 50
            
            # Handle different color formats
            try:
                if isinstance(color, dict):
                    if 'hex' in color:
                        hex_color = color['hex']
                        rgb_color = color.get('rgb', (0, 0, 0))
                        percentage = color.get('percentage', 0)
                    elif 'rgb' in color:
                        rgb_color = color['rgb']
                        hex_color = self.rgb_to_hex(rgb_color)
                        percentage = color.get('percentage', 0)
                    else:
                        # Handle other dictionary formats
                        keys = list(color.keys())
                        if len(keys) > 0:
                            # Try to find RGB-like data
                            first_value = color[keys[0]]
                            if isinstance(first_value, (tuple, list)) and len(first_value) >= 3:
                                rgb_color = first_value
                                hex_color = self.rgb_to_hex(rgb_color)
                                percentage = color.get('percentage', 0)
                            else:
                                rgb_color = (128, 128, 128)
                                hex_color = "#808080"
                                percentage = 0
                        else:
                            rgb_color = (128, 128, 128)
                            hex_color = "#808080"
                            percentage = 0
                elif isinstance(color, (tuple, list)) and len(color) >= 3:
                    # Direct RGB tuple
                    rgb_color = color[:3]
                    hex_color = self.rgb_to_hex(rgb_color)
                    percentage = 20.0  # Default percentage
                else:
                    # Fallback for unknown format
                    rgb_color = (128, 128, 128)
                    hex_color = "#808080"
                    percentage = 0
                
                # Color swatch
                color_bgr = self.hex_to_bgr(rgb_color)
                cv2.rectangle(frame, (table_x + 10, y_pos), (table_x + 50, y_pos + 30), 
                             color_bgr, -1, cv2.LINE_AA)
                cv2.rectangle(frame, (table_x + 10, y_pos), (table_x + 50, y_pos + 30), 
                             (255, 255, 255), 1, cv2.LINE_AA)
                
                # Color information
                hex_text = hex_color.upper()
                rgb_text = f"RGB{rgb_color}"
                percent_text = f"{percentage:.1f}%"
                
            except Exception as e:
                print(f"Error processing color {i}: {e}")
                # Use fallback color
                hex_text = "#808080"
                rgb_text = "RGB(128,128,128)"
                percent_text = "0.0%"
                color_bgr = (128, 128, 128)
            
            # Draw text with shadows for better visibility
            cv2.putText(frame, hex_text, (table_x + 61, y_pos + 12), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, hex_text, (table_x + 60, y_pos + 11), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            
            cv2.putText(frame, rgb_text, (table_x + 61, y_pos + 26), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, rgb_text, (table_x + 60, y_pos + 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1, cv2.LINE_AA)
            
            # Percentage with color-coded bar
            try:
                bar_width = int((percentage / 100) * 100)
                cv2.rectangle(frame, (table_x + 200, y_pos + 15), 
                             (table_x + 200 + bar_width, y_pos + 25), color_bgr, -1, cv2.LINE_AA)
                cv2.rectangle(frame, (table_x + 200, y_pos + 15), 
                             (table_x + 300, y_pos + 25), (100, 100, 100), 1, cv2.LINE_AA)
            except:
                pass
            
            cv2.putText(frame, percent_text, (table_x + 305, y_pos + 23), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        
        return frame
    
    def draw_center_circle(self, frame: np.ndarray) -> np.ndarray:
        """Draw center circle with XOR color and anti-aliasing"""
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        
        # Get background color at center
        background_bgr = frame[center_y, center_x]
        
        # Calculate XOR color
        xor_color = self.get_xor_color(background_bgr)
        
        # Ensure color is in correct format for OpenCV
        xor_color = tuple(int(c) for c in xor_color)
        
        # Draw bigger circle with XOR color and anti-aliasing
        cv2.circle(frame, (center_x, center_y), self.circle_radius, xor_color, 3, cv2.LINE_AA)
        cv2.circle(frame, (center_x, center_y), 4, xor_color, -1, cv2.LINE_AA)
        
        return frame
    
    def draw_fps(self, frame: np.ndarray, fps: float) -> np.ndarray:
        """Draw FPS counter with anti-aliasing"""
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
        return frame
    
    def draw_bottom_branding(self, frame: np.ndarray) -> np.ndarray:
        """Draw professional branding and instructions at bottom"""
        height, width = frame.shape[:2]
        
        # Semi-transparent background for bottom bar
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, height - 80), (width, height), (25, 25, 25), -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Main branding
        cv2.putText(frame, "MareArts-Xcolor", (10, height - 50), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.6, (100, 200, 255), 1, cv2.LINE_AA)
        
        # Installation instruction
        cv2.putText(frame, "pip install marearts-xcolor", (10, height - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1, cv2.LINE_AA)
        
        # Controls on the right
        if self.record_video:
            cv2.putText(frame, "Controls: 'q' quit | 'c' capture | 'r' record", (width - 350, height - 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Controls: 'q'/'x'/ESC to quit | 'c' to capture | 'r' record", (width - 400, height - 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Professional tagline
        cv2.putText(frame, "Advanced Color Extraction Library", (width - 350, height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.35, (150, 150, 150), 1, cv2.LINE_AA)
        
        return frame
    
    def setup_video_recording(self, frame_width: int, frame_height: int):
        """Setup video recording with high quality settings"""
        if not self.record_video:
            return
        
        # High quality video settings
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'XVID'
        fps = 30.0
        filename = f"marearts_xcolor_demo_segment_{self.video_segment_count:03d}.mp4"
        
        self.video_writer = cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))
        self.video_start_time = time.time()
        self.recording_active = True
        
        print(f"🎥 Recording started: {filename}")
    
    def write_video_frame(self, frame: np.ndarray):
        """Write frame to video file and handle segment rotation"""
        if not self.record_video or not self.recording_active:
            return
        
        # Write frame to video
        if self.video_writer is not None:
            self.video_writer.write(frame)
        
        # Check if we need to start a new segment
        current_time = time.time()
        if current_time - self.video_start_time >= self.video_segment_duration:
            self.finish_video_segment()
            self.video_segment_count += 1
            self.setup_video_recording(frame.shape[1], frame.shape[0])
    
    def finish_video_segment(self):
        """Finish current video segment"""
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None
            self.recording_active = False
            print(f"✅ Video segment completed: marearts_xcolor_demo_segment_{self.video_segment_count:03d}.mp4")
    
    def draw_recording_indicator(self, frame: np.ndarray) -> np.ndarray:
        """Draw recording indicator"""
        if not self.record_video or not self.recording_active:
            return frame
        
        # Calculate remaining time in segment
        current_time = time.time()
        elapsed = current_time - self.video_start_time
        remaining = self.video_segment_duration - elapsed
        
        # Recording indicator (red circle)
        cv2.circle(frame, (frame.shape[1] - 50, 30), 8, (0, 0, 255), -1, cv2.LINE_AA)
        cv2.putText(frame, "REC", (frame.shape[1] - 80, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        
        # Segment timer
        cv2.putText(frame, f"Segment: {remaining:.1f}s", (frame.shape[1] - 150, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        
        return frame
    
    def find_camera(self):
        """Find available camera"""
        for i in range(5):  # Check first 5 camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    cap.release()
                    return i
                cap.release()
        return None
    
    def run(self):
        """Main webcam loop"""
        # Find available camera
        camera_idx = self.find_camera()
        if camera_idx is None:
            print("Error: No camera found. Please check:")
            print("1. Camera is connected")
            print("2. Camera permissions are granted")
            print("3. No other applications are using the camera")
            return
        
        print(f"Using camera {camera_idx}")
        cap = cv2.VideoCapture(camera_idx)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
        
        # Set camera resolution for high quality recording
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Setup video recording if enabled
        actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.setup_video_recording(actual_width, actual_height)
        
        fps_counter = 0
        fps_start_time = time.time()
        current_fps = 0
        
        print("🎨 MareArts-Xcolor Real-time Demo")
        print("📦 pip install marearts-xcolor")
        print("🎯 Move objects through the center circle to analyze colors")
        if self.record_video:
            print("🎥 Recording enabled - creating 30s segments")
            print("⌨️  Controls: 'q'/'x'/ESC to quit | 'c' to capture | 'r' to toggle recording")
        else:
            print("⌨️  Controls: 'q'/'x'/ESC to quit | 'c' to capture | 'r' to start recording")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Flip frame horizontally for mirror effect (left-right flip)
            frame = cv2.flip(frame, 1)
            
            # Extract colors periodically
            current_time = time.time()
            if current_time - self.last_extraction_time > self.extraction_interval:
                self.extract_colors_async(frame)
            
            # Draw center circle
            try:
                frame = self.draw_center_circle(frame)
            except Exception as e:
                print(f"Error drawing center circle: {e}")
                # Draw a simple white circle as fallback
                height, width = frame.shape[:2]
                center_x, center_y = width // 2, height // 2
                cv2.circle(frame, (center_x, center_y), self.circle_radius, (255, 255, 255), 3, cv2.LINE_AA)
            
            # Draw color table
            with self.extraction_lock:
                if self.current_colors:
                    try:
                        frame = self.draw_color_table(frame, self.current_colors)
                    except Exception as e:
                        print(f"Error drawing color table: {e}")
            
            # Calculate and draw FPS
            fps_counter += 1
            if current_time - fps_start_time >= 1.0:
                current_fps = fps_counter / (current_time - fps_start_time)
                fps_counter = 0
                fps_start_time = current_time
            
            frame = self.draw_fps(frame, current_fps)
            
            # Draw recording indicator if recording
            frame = self.draw_recording_indicator(frame)
            
            # Draw branding and instructions at bottom
            self.draw_bottom_branding(frame)
            
            # Write frame to video if recording
            self.write_video_frame(frame)
            
            # Display frame
            cv2.imshow('Webcam Color Extractor', frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('x') or key == 27:  # q, x, or ESC
                break
            elif key == ord('c'):
                # Force color extraction
                self.extract_colors_async(frame)
            elif key == ord('r'):
                # Toggle recording
                self.record_video = not self.record_video
                if self.record_video:
                    self.setup_video_recording(actual_width, actual_height)
                    print("🎥 Recording started")
                else:
                    self.finish_video_segment()
                    print("⏹️  Recording stopped")
        
        # Clean up video recording
        if self.recording_active:
            self.finish_video_segment()
        
        cap.release()
        cv2.destroyAllWindows()


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='MareArts-Xcolor Webcam Demo')
    parser.add_argument('--record', '-r', action='store_true', 
                       help='Enable video recording (30s segments)')
    parser.add_argument('--colors', '-c', type=int, default=5,
                       help='Number of colors to extract (default: 5)')
    
    args = parser.parse_args()
    
    try:
        if args.record:
            print("🎥 Video recording enabled - 30 second segments")
            print("📁 Videos will be saved as marearts_xcolor_demo_segment_XXX.mp4")
        
        extractor = WebcamColorExtractor(n_colors=args.colors, record_video=args.record)
        extractor.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()