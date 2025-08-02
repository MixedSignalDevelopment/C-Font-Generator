# **C Font Generator GUI**

## **Overview**

This application provides a user-friendly graphical interface (GUI) for creating and converting fonts into C-language header files, suitable for use in embedded systems, microcontrollers, and graphical display projects.

The tool offers two primary functionalities:

1. **TTF to C Conversion**: Automatically convert any standard TrueType Font (.ttf) file into a complete C font array.  
2. **Manual** Character **Creation**: Manually design individual characters on a pixel grid and generate the corresponding C array.

Both methods support generating font data in either 8-bit (uint8\_t) or 16-bit (uint16\_t) formats, processed row-wise.

## **Features**

### **TTF to C Converter**

* **Load Any TTF Font**: Use the file browser to load any .ttf font file from your system.  
* **Custom Dimensions**: Specify the exact pixel width and height for the output characters.  
* **Selectable Bit Depth**: Choose between generating uint8\_t or uint16\_t data arrays.  
* **Automatic C-Header Generation**: Creates a single, flattened static const array containing all ASCII characters from space (0x20) to tilde (0x7E).  
* **Clear Formatting**: The output C code is well-commented, indicating which character each block of data represents.

### **Manual Character Creator**

* **Pixel Grid Editor**: Opens a new window with a checkbox grid based on your specified character dimensions.  
* **Visual Design**: Simply click the checkboxes to turn pixels on or off and visually design your character.  
* **Selectable** Bit **Depth**: Choose between an 8-bit or 16-bit output for your custom character array.  
* **Instant C-Code Generation**: Generates a C array for the single character you designed.

## **Requirements**

To run this script, you need Python 3 and the following library:

* **Pillow**: The Python Imaging Library fork, used for font rendering and image manipulation.

You can install the required library using pip:

```pip install Pillow```

## **How to Use**

1. **Save the Script**: Save the application code as a Python file (e.g., font\_generator.py).  
2. **Run from Terminal**: Open a terminal or command prompt, navigate to the directory where you saved the file, and run the script:  
   python font\_generator.py

3. The main application window will appear.

### **To Convert a TTF Font:**

1. In the "TTF to C Converter" section, enter your desired **Font Width** and **Font Height**.  
2. Select the desired **Bit Depth** (8-bit or 16-bit).  
3. Click the **"Load TTF Font"** button and select a .ttf file.  
4. Click the **"Convert** TTF to C Font" button.  
5. A new window will appear containing the generated C header file content. You can copy this code and save it as a .h file in your project.

### **To Create a Manual Character:**

1. In the "Manual Character Creator" section, enter your desired **Char Width** and **Char Height**.  
2. Select the desired **Bit Depth**.  
3. Click the **"Create Manual Character"** button.  
4. A new window with a grid of checkboxes will appear. Click the boxes to design your character.  
5. In the grid window, click the **"Generate C Code"** button.  
6. A new window will appear with the C array for your custom character.

## **Generated C Code Format**

The script generates font data in a row-wise format. Each row of pixels is packed into one or more data elements (uint8\_t or uint16\_t).

* **Bit Packing**: Bits are packed from left to right, corresponding to the most significant bit (MSB) to the least significant bit (LSB) of the data type.  
* **TTF Output**: The TTF converter generates a single, large array. Each character is represented by a block of height data elements.  

 ``` // Example for a 6x8 font (8-bit)  
  static const uint8\_t Font6x8\[\] \= {  
      0x20,  // '\!' row 0  
      0x20,  // '\!' row 1  
      0x20,  // '\!' row 2  
      0x20,  // '\!' row 3  
      0x20,  // '\!' row 4  
      0x00,  // '\!' row 5  
      0x20,  // '\!' row 6  
      0x00,  // '\!' row 7  
      // ... next character ...  
  }; 
  ```
 


## **License**

**This project is licensed under the MIT License \- see the LICENSE.md file for details**