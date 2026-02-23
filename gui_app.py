"""
Desktop GUI Application for Handwriting Generator
Tkinter-based interface with custom dark theme
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import random
import threading
import os
from datetime import datetime

# Import modules
try:
    import config
    from vector_extractor import VectorExtractor
    from feature_extractor import FeatureExtractor
    from style_matcher import StyleMatcher
    from style_transfer import StyleTransfer
    from text_generator import TextGenerator
    from svg_renderer import SVGRenderer
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please run setup.py first!")
    input("Press Enter to exit...")
    exit(1)

class HandwritingGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Handwriting Generator")
        self.root.geometry("1000x700")
        self.root.configure(bg=config.GUI_BG_COLOR)
        
        # Initialize variables
        self.canvas = None
        self.is_drawing = False
        self.strokes = []
        self.current_stroke = []
        self.last_point = None
        self.start_time = 0
        self.session_id = None
        self.personalized_style = None
        self.current_output_path = None
        
        # Color rotation
        self.color_index = 0
        self.colors = config.GUI_TEXT_COLORS
        
        # Initialize modules
        self.init_modules()
        
        # Create GUI
        self.create_gui()
        
    def get_random_color(self):
        """Get random text color from palette"""
        color = self.colors[self.color_index]
        self.color_index = (self.color_index + 1) % len(self.colors)
        return color
    
    def init_modules(self):
        """Initialize processing modules"""
        try:
            self.vector_extractor = VectorExtractor()
            self.feature_extractor = FeatureExtractor()
            self.svg_renderer = SVGRenderer()
            
            # Check if database exists
            if os.path.exists(config.DATABASE_PATH):
                self.style_matcher = StyleMatcher(config.DATABASE_PATH)
                self.db_status = "✓ Database Loaded"
            else:
                self.style_matcher = None
                self.db_status = "✗ Database Missing - Run setup.py"
        except Exception as e:
            self.db_status = f"✗ Error: {str(e)}"
            self.style_matcher = None
    
    def create_gui(self):
        """Create GUI elements"""
        
        # Title
        title_label = tk.Label(
            self.root,
            text="✍ HANDWRITING GENERATOR",
            font=config.GUI_TITLE_FONT,
            bg=config.GUI_BG_COLOR,
            fg=self.get_random_color()
        )
        title_label.pack(pady=10)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg=config.GUI_BG_COLOR)
        status_frame.pack(fill=tk.X, padx=10)
        
        self.status_label = tk.Label(
            status_frame,
            text=f"STATUS: {self.db_status}",
            font=config.GUI_FONT,
            bg=config.GUI_BG_COLOR,
            fg=self.get_random_color(),
            anchor='w'
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Main container
        main_frame = tk.Frame(self.root, bg=config.GUI_BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Drawing
        left_frame = tk.Frame(main_frame, bg=config.GUI_BG_COLOR)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Canvas label
        canvas_label = tk.Label(
            left_frame,
            text="STEP 1: DRAW YOUR HANDWRITING SAMPLE",
            font=config.GUI_FONT,
            bg=config.GUI_BG_COLOR,
            fg=self.get_random_color()
        )
        canvas_label.pack(pady=5)
        
        # Instructions
        instr_text = "Write: 'The quick brown fox jumps over the lazy dog'"
        instr_label = tk.Label(
            left_frame,
            text=instr_text,
            font=('Consolas', 8, 'italic'),
            bg=config.GUI_BG_COLOR,
            fg=self.get_random_color()
        )
        instr_label.pack(pady=2)
        
        # Canvas
        canvas_frame = tk.Frame(left_frame, bg='#2a2a2a', relief=tk.SUNKEN, bd=2)
        canvas_frame.pack(pady=5)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            width=config.CANVAS_WIDTH,
            height=config.CANVAS_HEIGHT,
            bg='white',
            cursor='crosshair'
        )
        self.canvas.pack()
        
        # Bind canvas events
        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)
        
        # Canvas buttons
        canvas_btn_frame = tk.Frame(left_frame, bg=config.GUI_BG_COLOR)
        canvas_btn_frame.pack(pady=5)
        
        self.clear_btn = self.create_button(
            canvas_btn_frame,
            "CLEAR",
            self.clear_canvas,
            self.get_random_color()
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.process_btn = self.create_button(
            canvas_btn_frame,
            "PROCESS SAMPLE →",
            self.process_sample,
            self.get_random_color()
        )
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        # Analysis results
        results_label = tk.Label(
            left_frame,
            text="ANALYSIS RESULTS:",
            font=config.GUI_FONT,
            bg=config.GUI_BG_COLOR,
            fg=self.get_random_color()
        )
        results_label.pack(pady=5)
        
        self.results_text = scrolledtext.ScrolledText(
            left_frame,
            height=8,
            width=60,
            font=('Consolas', 8),
            bg='#2a2a2a',
            fg='#00FF00',
            insertbackground='white'
        )
        self.results_text.pack(pady=5)
        
        # Right panel - Generation
        right_frame = tk.Frame(main_frame, bg=config.GUI_BG_COLOR)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Generation label
        gen_label = tk.Label(
            right_frame,
            text="STEP 2: GENERATE TEXT",
            font=config.GUI_FONT,
            bg=config.GUI_BG_COLOR,
            fg=self.get_random_color()
        )
        gen_label.pack(pady=5)
        
        # Text input
        input_label = tk.Label(
            right_frame,
            text="Enter text to generate:",
            font=config.GUI_FONT,
            bg=config.GUI_BG_COLOR,
            fg=self.get_random_color()
        )
        input_label.pack(pady=2)
        
        self.text_input = scrolledtext.ScrolledText(
            right_frame,
            height=6,
            width=50,
            font=('Consolas', 10),
            bg='#2a2a2a',
            fg='white',
            insertbackground='white'
        )
        self.text_input.pack(pady=5)
        self.text_input.insert('1.0', "Hello World!\nThis is a test of the handwriting generator.")
        
        # Generation buttons
        gen_btn_frame = tk.Frame(right_frame, bg=config.GUI_BG_COLOR)
        gen_btn_frame.pack(pady=5)
        
        self.generate_btn = self.create_button(
            gen_btn_frame,
            "✨ GENERATE",
            self.generate_text,
            self.get_random_color()
        )
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        self.generate_btn['state'] = 'disabled'
        
        self.download_btn = self.create_button(
            gen_btn_frame,
            "📥 SAVE SVG",
            self.save_output,
            self.get_random_color()
        )
        self.download_btn.pack(side=tk.LEFT, padx=5)
        self.download_btn['state'] = 'disabled'
        
        # Preview label
        preview_label = tk.Label(
            right_frame,
            text="OUTPUT PREVIEW:",
            font=config.GUI_FONT,
            bg=config.GUI_BG_COLOR,
            fg=self.get_random_color()
        )
        preview_label.pack(pady=5)
        
        # Output info
        self.output_text = scrolledtext.ScrolledText(
            right_frame,
            height=15,
            width=50,
            font=('Consolas', 8),
            bg='#2a2a2a',
            fg='#FFB6C1',
            insertbackground='white'
        )
        self.output_text.pack(pady=5, fill=tk.BOTH, expand=True)
        self.output_text.insert('1.0', "Output will appear here after generation...")
    
    def create_button(self, parent, text, command, color):
        """Create styled button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=config.GUI_BUTTON_FONT,
            bg='#2a2a2a',
            fg=color,
            activebackground='#3a3a3a',
            activeforeground=color,
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5,
            cursor='hand2'
        )
        return btn
    
    def start_drawing(self, event):
        """Start drawing on canvas"""
        self.is_drawing = True
        self.current_stroke = []
        self.start_time = datetime.now().timestamp() * 1000
        self.last_point = (event.x, event.y)
        
        point = {
            'x': event.x,
            'y': event.y,
            'timestamp': 0,
            'pressure': 0.5,
            'velocity': 0
        }
        self.current_stroke.append(point)
    
    def draw(self, event):
        """Draw on canvas"""
        if not self.is_drawing:
            return
        
        current_time = datetime.now().timestamp() * 1000 - self.start_time
        
        # Calculate velocity
        velocity = 0
        if self.last_point:
            dx = event.x - self.last_point[0]
            dy = event.y - self.last_point[1]
            distance = (dx**2 + dy**2)**0.5
            
            if len(self.current_stroke) > 0:
                time_delta = current_time - self.current_stroke[-1]['timestamp']
                velocity = distance / time_delta if time_delta > 0 else 0
        
        point = {
            'x': event.x,
            'y': event.y,
            'timestamp': current_time,
            'pressure': 0.5,
            'velocity': velocity
        }
        self.current_stroke.append(point)
        
        # Draw line
        if self.last_point:
            self.canvas.create_line(
                self.last_point[0], self.last_point[1],
                event.x, event.y,
                width=2,
                fill='black',
                capstyle=tk.ROUND,
                smooth=True
            )
        
        self.last_point = (event.x, event.y)
    
    def stop_drawing(self, event):
        """Stop drawing"""
        if self.is_drawing and len(self.current_stroke) > 0:
            self.strokes.append(self.current_stroke)
            self.current_stroke = []
        self.is_drawing = False
        self.last_point = None
    
    def clear_canvas(self):
        """Clear canvas"""
        self.canvas.delete('all')
        self.strokes = []
        self.current_stroke = []
        self.results_text.delete('1.0', tk.END)
        self.update_status("Canvas cleared", "#FFFF00")
    
    def process_sample(self):
        """Process handwriting sample"""
        if len(self.strokes) == 0:
            messagebox.showwarning("No Input", "Please draw something first!")
            return
        
        if self.style_matcher is None:
            messagebox.showerror("Database Missing", 
                               "Handwriting database not found!\n\nPlease run setup.py first.")
            return
        
        # Disable button
        self.process_btn['state'] = 'disabled'
        self.update_status("Processing sample...", "#00FFFF")
        
        # Process in thread
        thread = threading.Thread(target=self._process_sample_thread)
        thread.start()
    
    def _process_sample_thread(self):
        """Process sample in background thread"""
        try:
            # Extract vectors
            vectors = self.vector_extractor.extract_from_strokes(self.strokes)
            
            if not vectors:
                self.root.after(0, lambda: messagebox.showerror("Error", "Failed to extract vectors"))
                return
            
            # Extract features
            features, feature_vector = self.feature_extractor.extract_features(vectors)
            
            if features is None:
                self.root.after(0, lambda: messagebox.showerror("Error", "Failed to extract features"))
                return
            
            # Find best match
            match_result = self.style_matcher.find_best_match(feature_vector)
            
            if match_result is None:
                self.root.after(0, lambda: messagebox.showerror("Error", "Failed to find matching style"))
                return
            
            similarity = match_result['similarity_score']
            
            # Check similarity threshold
            if similarity < config.MIN_SIMILARITY_THRESHOLD:
                msg = f"⚠ LOW SIMILARITY MATCH ⚠\n\n"
                msg += f"Similarity: {similarity*100:.1f}%\n"
                msg += f"Minimum recommended: {config.MIN_SIMILARITY_THRESHOLD*100:.0f}%\n\n"
                msg += "The match quality is poor. Results may not look like your handwriting.\n\n"
                msg += "Do you want to proceed anyway?"
                
                result = messagebox.askyesno("Low Similarity Warning", msg)
                if not result:
                    self.root.after(0, lambda: self.process_btn.config(state='normal'))
                    return
            
            # Transfer style
            style_transfer = StyleTransfer()
            self.personalized_style = style_transfer.transfer_style(
                features,
                match_result['best_match']
            )
            
            # Display results
            self.root.after(0, lambda: self._display_results(features, match_result, similarity))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Processing failed:\n{str(e)}"))
        finally:
            self.root.after(0, lambda: self.process_btn.config(state='normal'))
    
    def _display_results(self, features, match_result, similarity):
        """Display analysis results"""
        self.results_text.delete('1.0', tk.END)
        
        # Determine quality
        if similarity >= config.SIMILARITY_EXCELLENT:
            quality = "EXCELLENT"
            quality_color = "#00FF00"
        elif similarity >= config.SIMILARITY_GOOD:
            quality = "GOOD"
            quality_color = "#90EE90"
        elif similarity >= config.SIMILARITY_FAIR:
            quality = "FAIR"
            quality_color = "#FFFF00"
        else:
            quality = "POOR"
            quality_color = "#FFB6C1"
        
        result = "╔" + "═" * 48 + "╗\n"
        result += "║" + " HANDWRITING ANALYSIS COMPLETE ".center(48) + "║\n"
        result += "╚" + "═" * 48 + "╝\n\n"
        
        result += f"✓ MATCH FOUND!\n"
        result += f"  Style: {match_result['best_match']['name']}\n"
        result += f"  Similarity: {similarity*100:.1f}%\n"
        result += f"  Quality: {quality}\n"
        result += f"  Confidence: {match_result['confidence'].upper()}\n\n"
        
        result += "EXTRACTED FEATURES:\n"
        result += "-" * 50 + "\n"
        
        feature_labels = {
            'slant_angle': 'Slant Angle',
            'letter_spacing': 'Letter Spacing',
            'stroke_thickness': 'Stroke Thickness',
            'cursive_ratio': 'Cursive Style',
            'loop_size': 'Loop Size',
            'connection_type': 'Connection Type',
            'baseline_variation': 'Baseline Wobble',
            'aspect_ratio': 'Aspect Ratio',
            'pressure_variation': 'Pressure Variation',
            'avg_speed': 'Writing Speed'
        }
        
        for key, value in features.items():
            label = feature_labels.get(key, key)
            if isinstance(value, float):
                result += f"  • {label}: {value:.3f}\n"
            else:
                result += f"  • {label}: {value}\n"
        
        result += "\n" + "=" * 50 + "\n"
        result += "✓ Ready to generate text!\n"
        
        self.results_text.insert('1.0', result)
        
        # Enable generation
        self.generate_btn['state'] = 'normal'
        self.update_status(f"Analysis complete! Similarity: {similarity*100:.1f}% ({quality})", quality_color)
    
    def generate_text(self):
        """Generate handwritten text"""
        if self.personalized_style is None:
            messagebox.showwarning("Not Ready", "Please process a handwriting sample first!")
            return
        
        input_text = self.text_input.get('1.0', tk.END).strip()
        
        if not input_text:
            messagebox.showwarning("No Text", "Please enter some text to generate!")
            return
        
        self.generate_btn['state'] = 'disabled'
        self.update_status("Generating handwriting...", "#00FFFF")
        
        # Generate in thread
        thread = threading.Thread(target=self._generate_text_thread, args=(input_text,))
        thread.start()
    
    def _generate_text_thread(self, input_text):
        """Generate text in background thread"""
        try:
            # Generate text
            text_gen = TextGenerator(self.personalized_style)
            characters = text_gen.generate_text(input_text)
            
            # Render to SVG
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"handwriting_{timestamp}.svg"
            output_path = os.path.join(config.OUTPUT_FOLDER, output_filename)
            
            self.svg_renderer.render_to_svg(characters, output_path)
            self.current_output_path = output_path
            
            # Display info
            self.root.after(0, lambda: self._display_output_info(output_path, len(characters)))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Generation failed:\n{str(e)}"))
        finally:
            self.root.after(0, lambda: self.generate_btn.config(state='normal'))
    
    def _display_output_info(self, output_path, num_chars):
        """Display output information"""
        self.output_text.delete('1.0', tk.END)
        
        info = "╔" + "═" * 48 + "╗\n"
        info += "║" + " GENERATION COMPLETE ".center(48) + "║\n"
        info += "╚" + "═" * 48 + "╝\n\n"
        
        info += f"✓ Generated successfully!\n\n"
        info += f"Output Details:\n"
        info += f"  • Format: SVG (Vector)\n"
        info += f"  • Characters: {num_chars}\n"
        info += f"  • File: {os.path.basename(output_path)}\n"
        info += f"  • Location: {output_path}\n\n"
        
        # Get file size
        file_size = os.path.getsize(output_path) / 1024
        info += f"  • Size: {file_size:.2f} KB\n\n"
        
        info += "=" * 50 + "\n"
        info += "You can now:\n"
        info += "  • Click 'SAVE SVG' to choose save location\n"
        info += "  • Generate more text\n"
        info += "  • Open file in design software\n"
        
        self.output_text.insert('1.0', info)
        
        self.download_btn['state'] = 'normal'
        self.update_status("✓ Generation complete!", "#00FF00")
    
    def save_output(self):
        """Save output to user-selected location"""
        if self.current_output_path is None:
            messagebox.showwarning("No Output", "Please generate text first!")
            return
        
        # Ask user where to save
        filename = filedialog.asksaveasfilename(
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")],
            initialfile=os.path.basename(self.current_output_path)
        )
        
        if filename:
            try:
                # Copy file
                import shutil
                shutil.copy2(self.current_output_path, filename)
                messagebox.showinfo("Success", f"File saved to:\n{filename}")
                self.update_status(f"Saved to: {filename}", "#00FF00")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def update_status(self, message, color):
        """Update status bar"""
        self.status_label.config(text=f"STATUS: {message}", fg=color)

def main():
    """Main function"""
    # Check if setup has been run
    if not os.path.exists(config.DATABASE_PATH):
        print("\n" + "=" * 60)
        print("⚠ DATABASE NOT FOUND ⚠")
        print("=" * 60)
        print("\nPlease run setup first:")
        print("  1. Double-click: SETUP.bat")
        print("  2. Or run: python setup.py")
        print("\n" + "=" * 60)
        input("\nPress Enter to exit...")
        return
    
    # Create and run GUI
    root = tk.Tk()
    app = HandwritingGeneratorGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
