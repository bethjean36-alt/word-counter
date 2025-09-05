import argparse
import os
import shutil
import datetime
import filecmp

def create_backup_folder(dest_path):
    """
    Creates a new backup folder with a timestamp in the destination path.
    Returns the path to the newly created folder.
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_folder_name = f'backup_{timestamp}'
    backup_path = os.path.join(dest_path, backup_folder_name)
    try:
        os.makedirs(backup_path)
        print(f"Created new backup folder: {backup_path}")
        return backup_path
    except OSError as e:
        print(f"Error creating directory {backup_path}: {e}")
        return None

def backup_files(source, destination, is_full_backup, log_file):
    """
    Copies files from the source to the destination based on the backup type.
    """
    copied_count = 0
    skipped_count = 0
    errors_count = 0
    total_files = 0
    
    # Walk through the source directory
    for root, dirs, files in os.walk(source):
        total_files += len(files)
        
        # Calculate the relative path from the source to the current directory
        relative_path = os.path.relpath(root, source)
        dest_dir = os.path.join(destination, relative_path)
        
        # Ensure the destination subdirectory exists
        os.makedirs(dest_dir, exist_ok=True)
        
        for filename in files:
            source_file = os.path.join(root, filename)
            dest_file = os.path.join(dest_dir, filename)
            
            try:
                # Check if the file already exists in the destination
                if os.path.exists(dest_file):
                    if is_full_backup:
                        # Full backup: check if files are identical to avoid redundant copy
                        if filecmp.cmp(source_file, dest_file, shallow=False):
                            log_message = f"SKIPPED (Identical): {source_file}"
                            print(log_message)
                            log_file.write(log_message + '\n')
                            skipped_count += 1
                        else:
                            log_message = f"COPYING (Full Backup - Modified): {source_file}"
                            print(log_message)
                            shutil.copy2(source_file, dest_file)
                            log_file.write(log_message + '\n')
                            copied_count += 1
                    else:
                        # Incremental backup: check modification times
                        source_mod_time = os.path.getmtime(source_file)
                        dest_mod_time = os.path.getmtime(dest_file)
                        
                        if source_mod_time > dest_mod_time:
                            log_message = f"COPYING (Incremental - Newer): {source_file}"
                            print(log_message)
                            shutil.copy2(source_file, dest_file)
                            log_file.write(log_message + '\n')
                            copied_count += 1
                        else:
                            log_message = f"SKIPPED (Incremental - Already up-to-date): {source_file}"
                            print(log_message)
                            log_file.write(log_message + '\n')
                            skipped_count += 1
                else:
                    # File does not exist in destination, copy it
                    log_message = f"COPYING (New): {source_file}"
                    print(log_message)
                    shutil.copy2(source_file, dest_file)
                    log_file.write(log_message + '\n')
                    copied_count += 1
            except Exception as e:
                log_message = f"ERROR backing up {source_file}: {e}"
                print(log_message)
                log_file.write(log_message + '\n')
                errors_count += 1
                
    return copied_count, skipped_count, errors_count, total_files

def main():
    parser = argparse.ArgumentParser(description="A robust file backup script.")
    parser.add_argument("source", help="Source directory to backup.")
    parser.add_argument("destination", help="Destination directory for the backup.")
    parser.add_argument("--full", action="store_true", help="Perform a full backup, overwriting existing files if different. Default is incremental.")

    args = parser.parse_args()

    # Validate source and destination paths
    if not os.path.isdir(args.source):
        print(f"Error: Source directory '{args.source}' does not exist.")
        return
    if not os.path.isdir(args.destination):
        print(f"Error: Destination directory '{args.destination}' does not exist.")
        return

    # Create the top-level backup folder with timestamp
    backup_dest_path = create_backup_folder(args.destination)
    if not backup_dest_path:
        return

    # Create the log file
    log_path = os.path.join(backup_dest_path, 'backup.log')
    try:
        with open(log_path, 'w') as log_file:
            log_file.write(f"Backup Log - Started: {datetime.datetime.now()}\n")
            backup_type = "Full" if args.full else "Incremental"
            log_file.write(f"Backup Type: {backup_type}\n")
            log_file.write(f"Source: {args.source}\n")
            log_file.write(f"Destination: {backup_dest_path}\n\n")

            copied, skipped, errors, total = backup_files(args.source, backup_dest_path, args.full, log_file)

            log_file.write(f"\n--- Summary ---\n")
            log_file.write(f"Total files in source: {total}\n")
            log_file.write(f"Files copied: {copied}\n")
            log_file.write(f"Files skipped: {skipped}\n")
            log_file.write(f"Files with errors: {errors}\n")
            log_file.write(f"Backup completed: {datetime.datetime.now()}\n")
            
            print("\n--- Backup Summary ---")
            print(f"Total files processed: {total}")
            print(f"Files copied: {copied}")
            print(f"Files skipped: {skipped}")
            print(f"Files with errors: {errors}")
            print(f"Backup log created at: {log_path}")
            
    except IOError as e:
        print(f"Error creating or writing to log file at {log_path}: {e}")

if __name__ == "__main__":
    main()
