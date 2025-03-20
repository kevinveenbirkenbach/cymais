import os
import argparse

def generate_ansible_roles_index(roles_dir, output_file, caption: str):
    """Generates an index.rst file listing all .rst files in the given directory."""
    
    roles_dir = os.path.abspath(roles_dir)
    output_file = os.path.abspath(output_file)
    output_dir = os.path.dirname(output_file)

    if not os.path.exists(roles_dir):
        print(f"Error: Directory {roles_dir} does not exist.")
        return
    
    os.makedirs(output_dir, exist_ok=True)

    rst_files = [f for f in os.listdir(roles_dir) if f.endswith(".rst")]
    rst_files.sort()  # Alphabetisch sortieren

    # Berechne relative Pfade zur korrekten Verlinkung
    rel_paths = [os.path.relpath(os.path.join(roles_dir, f), start=output_dir) for f in rst_files]

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"{caption}\n===================\n\n")
        f.write(f".. toctree::\n   :maxdepth: 1\n   :caption: {caption}\n\n")
        
        for rel_path in rel_paths:
            file_name_without_ext = os.path.splitext(rel_path)[0]
            f.write(f"   {file_name_without_ext}\n")

    print(f"Index generated at {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an index for documentation.")
    parser.add_argument("--roles-dir", required=True, help="Directory containing .rst files.")
    parser.add_argument("--output-file", required=True, help="Path to the output index.rst file.")
    parser.add_argument("--caption", required=True, help="The index title")

    args = parser.parse_args()
    generate_ansible_roles_index(args.roles_dir, args.output_file, args.caption)
