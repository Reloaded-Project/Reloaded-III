import os

def strip_whitespace(file_path):
    if file_path.endswith('.md'):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Check if the last line ends with a newline
        has_newline_at_end = lines and lines[-1].endswith('\n')

        with open(file_path, 'w') as file:
            for i, line in enumerate(lines):
                # Remove trailing spaces
                line = line.rstrip()

                # Add newline to all lines except the last one if it didn't originally have a newline
                if i < len(lines) - 1 or has_newline_at_end:
                    line += '\n'

                file.write(line)

def main():
    git_root = os.popen('git rev-parse --show-toplevel').read().strip()
    docs_dir = os.path.join(git_root, 'docs')
    for dirpath, dirnames, filenames in os.walk(docs_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            strip_whitespace(file_path)

if __name__ == '__main__':
    main()