# -----------------------------------------------------------------------------
# Author: Sergio Luna 
# License: MIT License 
# Description: This script provides a GUI to convert TTF fonts and manually
#              create characters, exporting them as C-compatible font arrays.
# -----------------------------------------------------------------------------

import tkinter as tk
from tkinter import filedialog, messagebox, font as tkFont
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

class FontGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("C Font Generator")
        self.root.geometry("450x420")

        self.ttf_path = None
        self.manual_char_window = None

        # --- Main Layout ---
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Bit Depth Selection ---
        self.bit_depth_var = tk.StringVar(value="16-bit")

        # --- TTF Converter Section ---
        ttf_frame = tk.LabelFrame(main_frame, text="TTF to C Converter", padx=10, pady=10)
        ttf_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(ttf_frame, text="Font Width:").grid(row=0, column=0, sticky="w", pady=2)
        self.ttf_width_entry = tk.Entry(ttf_frame, width=10)
        self.ttf_width_entry.grid(row=0, column=1, sticky="w")
        self.ttf_width_entry.insert(0, "11")

        tk.Label(ttf_frame, text="Font Height:").grid(row=1, column=0, sticky="w", pady=2)
        self.ttf_height_entry = tk.Entry(ttf_frame, width=10)
        self.ttf_height_entry.grid(row=1, column=1, sticky="w")
        self.ttf_height_entry.insert(0, "18")
        
        tk.Label(ttf_frame, text="Bit Depth:").grid(row=2, column=0, sticky="w", pady=2)
        self.ttf_bit_depth_menu = tk.OptionMenu(ttf_frame, self.bit_depth_var, "8-bit", "16-bit")
        self.ttf_bit_depth_menu.grid(row=2, column=1, sticky="w")

        self.load_ttf_button = tk.Button(ttf_frame, text="Load TTF Font", command=self.load_ttf)
        self.load_ttf_button.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)

        self.ttf_label = tk.Label(ttf_frame, text="No font loaded", fg="gray")
        self.ttf_label.grid(row=4, column=0, columnspan=2, sticky="w")

        self.convert_button = tk.Button(ttf_frame, text="Convert TTF to C Font", command=self.convert_ttf_to_c)
        self.convert_button.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)


        # --- Manual Creator Section ---
        manual_frame = tk.LabelFrame(main_frame, text="Manual Character Creator", padx=10, pady=10)
        manual_frame.pack(fill=tk.X, pady=10)

        tk.Label(manual_frame, text="Char Width:").grid(row=0, column=0, sticky="w", pady=2)
        self.manual_width_entry = tk.Entry(manual_frame, width=10)
        self.manual_width_entry.grid(row=0, column=1, sticky="w")
        self.manual_width_entry.insert(0, "8")

        tk.Label(manual_frame, text="Char Height:").grid(row=1, column=0, sticky="w", pady=2)
        self.manual_height_entry = tk.Entry(manual_frame, width=10)
        self.manual_height_entry.grid(row=1, column=1, sticky="w")
        self.manual_height_entry.insert(0, "8")
        
        tk.Label(manual_frame, text="Bit Depth:").grid(row=2, column=0, sticky="w", pady=2)
        self.manual_bit_depth_menu = tk.OptionMenu(manual_frame, self.bit_depth_var, "8-bit", "16-bit")
        self.manual_bit_depth_menu.grid(row=2, column=1, sticky="w")

        self.create_manual_button = tk.Button(manual_frame, text="Create Manual Character", command=self.open_manual_creator)
        self.create_manual_button.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)

    def load_ttf(self):
        path = filedialog.askopenfilename(
            title="Select a TTF Font",
            filetypes=[("TrueType Fonts", "*.ttf")]
        )
        if path:
            self.ttf_path = path
            font_name = os.path.basename(path)
            self.ttf_label.config(text=f"Loaded: {font_name}", fg="green")
            messagebox.showinfo("Success", f"Successfully loaded {font_name}")

    def convert_ttf_to_c(self):
        if not self.ttf_path:
            messagebox.showerror("Error", "Please load a TTF font file first.")
            return

        try:
            width = int(self.ttf_width_entry.get())
            height = int(self.ttf_height_entry.get())
            font_size = height # Use height as a good starting point for font size
            bit_depth = int(self.bit_depth_var.get().replace('-bit', ''))
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer values for width and height.")
            return

        try:
            font = ImageFont.truetype(self.ttf_path, font_size)
            font_name = os.path.splitext(os.path.basename(self.ttf_path))[0].replace("-", "_")
            c_code = self.generate_c_font_from_ttf(font, font_name, width, height, bit_depth)
            self.show_code_in_window(f"{font_name}.h", c_code)
        except Exception as e:
            messagebox.showerror("Conversion Error", f"Failed to convert font: {e}")

    def generate_c_font_from_ttf(self, font, font_name, char_width, char_height, bit_depth):
        all_char_data = []
        
        char_comments = { 32: "sp", 34: '""', 39: "'", 92: "\\" }

        for char_code in range(32, 127):
            char = chr(char_code)
            image = Image.new('1', (char_width, char_height), 0)
            draw = ImageDraw.Draw(image)
            
            try:
                bbox = font.getbbox(char)
                char_w, char_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw_x = (char_width - char_w) // 2
                draw_y = (char_height - char_h) // 2 - bbox[1]
            except AttributeError:
                char_w, char_h = draw.textsize(char, font=font)
                draw_x = (char_width - char_w) / 2
                draw_y = (char_height - char_h) / 2

            draw.text((draw_x, draw_y), char, font=font, fill=1)
            pixels = list(image.getdata())
            
            hex_array_str, _ = self.pixels_to_c_array(pixels, char_width, char_height, bit_depth)
            
            comment_char = char_comments.get(char_code, char)
            if comment_char == '"': comment_char = '\\"'
            
            all_char_data.append((hex_array_str, comment_char))

        font_array_name = f"Font{char_width}x{char_height}"
        c_type = f"uint{bit_depth}_t"
        
        formatted_lines = []
        for i, (hex_str, comment) in enumerate(all_char_data):
            line = f"    {hex_str}"
            if i < len(all_char_data) - 1:
                line += ","
            line += f"  // {comment}"
            formatted_lines.append(line)
        
        array_content = "\n".join(formatted_lines)

        c_code = f"""#ifndef {font_name.upper()}_H
#define {font_name.upper()}_H

#include <stdint.h>

// Font data for {font_name} {char_width}x{char_height}
// Format: {char_height} words ({c_type}) per character, row-wise.
static const {c_type} {font_array_name}[] = {{
{array_content}
}};

#endif // {font_name.upper()}_H
"""
        return c_code

    def open_manual_creator(self):
        try:
            width = int(self.manual_width_entry.get())
            height = int(self.manual_height_entry.get())
            if width <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter valid, positive integer values for width and height.")
            return
        
        if self.manual_char_window and self.manual_char_window.winfo_exists():
            self.manual_char_window.lift()
            return

        self.manual_char_window = tk.Toplevel(self.root)
        self.manual_char_window.title(f"Draw Character ({width}x{height})")
        
        self.checkboxes = []
        frame = tk.Frame(self.manual_char_window, padx=10, pady=10)
        frame.pack()

        for y in range(height):
            row_vars = []
            for x in range(width):
                var = tk.IntVar()
                cb = tk.Checkbutton(frame, variable=var, onvalue=1, offvalue=0)
                cb.grid(row=y, column=x)
                row_vars.append(var)
            self.checkboxes.append(row_vars)
            
        generate_button = tk.Button(self.manual_char_window, text="Generate C Code", command=self.generate_manual_c_code)
        generate_button.pack(pady=10, padx=10, fill=tk.X)

    def generate_manual_c_code(self):
        width = len(self.checkboxes[0])
        height = len(self.checkboxes)
        bit_depth = int(self.bit_depth_var.get().replace('-bit', ''))
        
        pixels = []
        for y in range(height):
            for x in range(width):
                pixels.append(self.checkboxes[y][x].get())
        
        hex_array_str, num_elements = self.pixels_to_c_array(pixels, width, height, bit_depth)
        
        c_type = f"uint{bit_depth}_t"

        c_code = f"""
// Manually created character, {width}x{height}
// Total elements ({c_type}): {num_elements}
const {c_type} custom_char_{width}x{height}[{num_elements}] = {{
    {hex_array_str}
}};
"""
        self.show_code_in_window(f"Manual Char {width}x{height}", c_code)

    def pixels_to_c_array(self, pixels, width, height, bit_depth):
        elements_list = []
        
        for row in range(height):
            row_element = 0
            for col in range(width):
                pixel_index = row * width + col
                if pixels[pixel_index] == 1:
                    row_element |= (1 << ((bit_depth - 1) - (col % bit_depth)))

                if (col + 1) % bit_depth == 0 or col == width - 1:
                    elements_list.append(row_element)
                    row_element = 0
        
        hex_format = f"0x{{:0{bit_depth//4}X}}"
        hex_array = [hex_format.format(elem) for elem in elements_list]
        hex_array_str = ", ".join(hex_array)
        
        return hex_array_str, len(hex_array)

    def show_code_in_window(self, title, code):
        code_window = tk.Toplevel(self.root)
        code_window.title(title)
        code_window.geometry("600x700")
        
        text_widget = tk.Text(code_window, wrap=tk.WORD, font=("Courier New", 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, code)
        text_widget.config(state=tk.DISABLED)

        scrollbar = tk.Scrollbar(text_widget, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget['yscrollcommand'] = scrollbar.set

if __name__ == "__main__":
    root = tk.Tk()
    app = FontGeneratorApp(root)
    root.mainloop()
