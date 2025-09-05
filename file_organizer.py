import argparse
import os
import shutil
import sys
from collections import defaultdict

def organize_files(source_dir, dry_run=False):
    """
    Organizes files in a given directory by moving them into subfolders
    based on their file extensions.

    Args:
        source_dir (str): The path to the directory to organize.
        dry_run (bool): If True, shows what would be done without
                        actually moving any files.
    """
    print(f"--- File Organizer{' (Dry Run)' if dry_run else ''} ---")
    if not os.path.isdir(source_dir):
        print(f"Error: Directory not found at '{source_dir}'", file=sys.stderr)
        return

    # Use defaultdict to easily group files by extension
    files_by_extension = defaultdict(list)
    total_files = 0
    
    # First, scan the directory to find all files and group them
    print("Scanning directory...")
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        if os.path.isfile(item_path):
            total_files += 1
            # Get the file extension
            _, extension = os.path.splitext(item)
            extension = extension.lower().strip('.')
            if extension:
                files_by_extension[extension].append(item_path)
            else:
                files_by_extension['no_extension'].append(item_path)

    if not files_by_extension:
        print("No files found to organize.")
        return

    processed_count = 0
    for extension, file_list in files_by_extension.items():
        # Create a new subfolder for the extension
        folder_name = extension if extension != 'no_extension' else 'no_extension'
        target_dir = os.path.join(source_dir, folder_name)

        if not os.path.exists(target_dir):
            if dry_run:
                print(f"Would create folder: '{target_dir}'")
            else:
                try:
                    os.makedirs(target_dir)
                    print(f"Created folder: '{target_dir}'")
                except PermissionError:
                    print(f"Error: Permission denied to create folder '{target_dir}'. Skipping files for this extension.", file=sys.stderr)
                    continue
                except OSError as e:
                    print(f"Error creating folder '{target_dir}': {e}. Skipping.", file=sys.stderr)
                    continue
        
        # Move files into the subfolder
        for file_path in file_list:
            processed_count += 1
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(target_dir, file_name)

            if dry_run:
                print(f"[Dry Run] Would move '{file_name}' to '{target_dir}'")
            else:
                try:
                    shutil.move(file_path, destination_path)
                    print(f"Moved '{file_name}' to '{target_dir}'")
                except PermissionError:
                    print(f"Error: Permission denied to move '{file_name}'. Skipping.", file=sys.stderr)
                except Exception as e:
                    print(f"Error moving '{file_name}': {e}. Skipping.", file=sys.stderr)

        # Show progress
        percentage = (processed_count / total_files) * 100
        print(f"Progress: {processed_count}/{total_files} files ({percentage:.1f}%) processed.")

    print("\nOrganization complete.")


def main():
    """
    Main function to parse command-line arguments and run the organizer.
    """
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by file extension.",
        epilog="Example usage:\n  python file_organizer.py C:\\Users\\MyUser\\Downloads\n  python file_organizer.py /home/user/documents --dry-run"
    )
    parser.add_argument(
        "path",
        type=str,
        help="The path to the folder to organize."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the changes without actually moving any files."
    )

    args = parser.parse_args()
    organize_files(args.path, args.dry_run)


if __name__ == "__main__":
    main()
