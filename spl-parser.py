import os
import re
from pathlib import Path

def create_directory(directory_path):
    """Create directory if it doesn't exist."""
    os.makedirs(directory_path, exist_ok=True)

def extract_component(file_path, output_dir):
    """
    Extract different components from a .spl file and save them in separate files.
    
    Components:
    - Links
    - Includes
    - Defines
    - Objects
    - Procedures/Functions (including main procedure)
    - Screens
    - Menus
    """
    # Create output directories
    create_directory(output_dir)
    create_directory(os.path.join(output_dir, "links"))
    create_directory(os.path.join(output_dir, "includes"))
    create_directory(os.path.join(output_dir, "defines"))
    create_directory(os.path.join(output_dir, "objects"))
    create_directory(os.path.join(output_dir, "procedures"))
    create_directory(os.path.join(output_dir, "screens"))
    create_directory(os.path.join(output_dir, "menus"))
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
    
    # Extract links
    links = re.findall(r'link\s+[\'"]([^\'"\n]+)[\'"]', content)
    if links:
        with open(os.path.join(output_dir, "links", "all_links.txt"), 'w', encoding='utf-8') as link_file:
            for link in links:
                link_file.write(f"link '{link}'\n")
    
    # Extract includes
    includes = re.findall(r'#include\s+[\'"]([^\'"\n]+)[\'"]', content)
    if includes:
        with open(os.path.join(output_dir, "includes", "all_includes.txt"), 'w', encoding='utf-8') as inc_file:
            for include in includes:
                inc_file.write(f"#include '{include}'\n")
    
    # Extract defines
    defines = re.findall(r'#define\s+(\S+)(?:\s+(.+))?', content)
    if defines:
        with open(os.path.join(output_dir, "defines", "all_defines.txt"), 'w', encoding='utf-8') as def_file:
            for define in defines:
                if define[1]:
                    def_file.write(f"#define {define[0]} {define[1]}\n")
                else:
                    def_file.write(f"#define {define[0]}\n")
    
    # Extract objects
    object_pattern = re.compile(r'object\s+(\S+)(?:\s+\S+)?\s*\n((?:.+\n)*?)(?=\s*object|\s*(?:procedure|field|mode|screen|menu|end))', re.MULTILINE)
    objects = object_pattern.findall(content)
    
    for obj_name, obj_content in objects:
        clean_name = obj_name.replace('-', '_')
        with open(os.path.join(output_dir, "objects", f"{clean_name}.txt"), 'w', encoding='utf-8') as obj_file:
            obj_file.write(f"object {obj_name}\n{obj_content}")
    
    # Extract procedures
    procedure_pattern = re.compile(r'procedure\s+(\S+)(?:\s+\S+)?\s*\n((?:.+\n)*?)(?=\s*(?:procedure|endprocedure))\s*endprocedure', re.MULTILINE)
    procedures = procedure_pattern.findall(content)
    
    for proc_name, proc_content in procedures:
        clean_name = proc_name.replace('-', '_')
        with open(os.path.join(output_dir, "procedures", f"{clean_name}.txt"), 'w', encoding='utf-8') as proc_file:
            proc_file.write(f"procedure {proc_name}\n{proc_content}\nendprocedure")
    
    # Extract main procedure separately
    main_pattern = re.compile(r'procedure\s+main(?:\s+\S+)?\s*\n((?:.+\n)*?)(?=\s*endprocedure)\s*endprocedure', re.MULTILINE)
    main_match = main_pattern.search(content)
    
    if main_match:
        with open(os.path.join(output_dir, "procedures", "main.txt"), 'w', encoding='utf-8') as main_file:
            main_file.write(f"procedure main\n{main_match.group(1)}\nendprocedure")
    
    # Extract screens
    screen_pattern = re.compile(r'screen\s+(\S+)(?:\s+\S+)?\s*\n((?:.+\n)*?)(?=\s*(?:screen|endscreen))\s*endscreen', re.MULTILINE)
    screens = screen_pattern.findall(content)
    
    for screen_name, screen_content in screens:
        clean_name = screen_name.replace('-', '_')
        with open(os.path.join(output_dir, "screens", f"{clean_name}.txt"), 'w', encoding='utf-8') as screen_file:
            screen_file.write(f"screen {screen_name}\n{screen_content}\nendscreen")
    
    # Extract menus
    menu_pattern = re.compile(r'menu\s+(\S+)(?:\s+\S+)?\s*\n((?:.+\n)*?)(?=\s*(?:menu|endmenu))\s*endmenu', re.MULTILINE)
    menus = menu_pattern.findall(content)
    
    for menu_name, menu_content in menus:
        clean_name = menu_name.replace('-', '_')
        with open(os.path.join(output_dir, "menus", f"{clean_name}.txt"), 'w', encoding='utf-8') as menu_file:
            menu_file.write(f"menu {menu_name}\n{menu_content}\nendmenu")
    
    # Extract version-number
    version_pattern = re.compile(r'version-number\s+"([^"]+)"')
    versions = version_pattern.findall(content)
    
    if versions:
        with open(os.path.join(output_dir, "version.txt"), 'w', encoding='utf-8') as version_file:
            for version in versions:
                version_file.write(f'version-number "{version}"\n')
    
    # Save any remaining fields or declarations in a separate file
    with open(os.path.join(output_dir, "globals.txt"), 'w', encoding='utf-8') as globals_file:
        # Extract fields
        field_pattern = re.compile(r'field\s+(.*?)\n((?:.+\n)*?)(?=\s*(?:field|procedure|screen|menu|mode))', re.MULTILINE)
        fields = field_pattern.findall(content)
        
        for field_name, field_content in fields:
            globals_file.write(f"field {field_name}\n{field_content}\n")
        
        # Extract modes
        mode_pattern = re.compile(r'mode\s+(\S+)((?:.+\n)*?)(?=\s*(?:mode|procedure|screen|menu))', re.MULTILINE)
        modes = mode_pattern.findall(content)
        
        for mode_name, mode_content in modes:
            globals_file.write(f"mode {mode_name}{mode_content}\n")

if __name__ == "__main__":
    # Define input and output paths
    input_file = "m50lines.spl"  # Change this to your input file path
    output_directory = "m50lines_components"  # Change this to your desired output directory
    
    # Extract components
    extract_component(input_file, output_directory)
    print(f"Extraction completed. Components saved in {output_directory}")
