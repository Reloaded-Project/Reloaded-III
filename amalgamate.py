import os
import sys

def process_files(directory, output_file):
    for root, dirs, files in os.walk(directory):
         # Ignore folders starting with a dot
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.yml') or file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                
                output_file.write(f"---\nFile: {file_path}\n---\n")
                output_file.write(content)
                output_file.write("\n\n")

# Directory to start the search from
# Default to '.' if no argument is provided
directory = sys.argv[1] if len(sys.argv) > 1 else '.'

# Output file name
output_filename = 'concatenated_docs.txt'

with open(output_filename, 'w') as output_file:
    process_files(directory, output_file)

print(f"Concatenation complete. Output written to {output_filename}.")