import os
import argparse
import pathspec

def load_gitignore_patterns(source_dir):
    """Loads .gitignore patterns from the given source directory and returns a PathSpec object."""
    gitignore_path = os.path.join(source_dir, ".gitignore")
    if not os.path.exists(gitignore_path):
        return pathspec.PathSpec.from_lines("gitwildmatch", [])

    with open(gitignore_path, "r", encoding="utf-8") as f:
        patterns = f.readlines()
    
    return pathspec.PathSpec.from_lines("gitwildmatch", patterns)

def generate_yaml_index(source_dir, output_file):
    """Generates an index file listing all YAML files in the specified directory while respecting .gitignore rules."""
    
    yaml_files = []
    spec = load_gitignore_patterns(source_dir)  # Load .gitignore rules
    
    # Walk through the source directory and collect YAML files
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), start=source_dir)

            if file.endswith(('.yml', '.yaml')) and not spec.match_file(file_path):
                yaml_files.append(os.path.join(root, file))
    
    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the YAML index to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("YAML Files\n===========\n\n")
        f.write("This document lists all `.yaml` and `.yml` files found in the specified directory, excluding ignored files.\n\n")

        for file in sorted(yaml_files):
            relative_file_path = os.path.relpath(file, start=os.path.dirname(output_file))
            f.write(f".. literalinclude:: {relative_file_path}\n   :language: yaml\n   :linenos:\n\n")


    print(f"YAML index has been generated at {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an index for YAML files while respecting .gitignore.")
    parser.add_argument("--source-dir", required=True, help="Directory containing YAML files.")
    parser.add_argument("--output-file", required=True, help="Path to the output .rst file.")

    args = parser.parse_args()
    generate_yaml_index(args.source_dir, args.output_file)
