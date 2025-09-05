# log_parser.py
# A script to parse log files and generate a summary report.

import re
import sys
from collections import Counter, defaultdict
from datetime import datetime

def parse_log_file(filepath):
    """
    Parses a single log file, counting log levels, and extracting timestamps
    and error messages.

    Args:
        filepath (str): The path to the log file.

    Returns:
        dict: A dictionary containing parsing results.
              Returns None if the file cannot be read.
    """
    results = {
        'total_lines': 0,
        'line_counts': Counter({'ERROR': 0, 'WARNING': 0, 'INFO': 0}),
        'timestamps': [],
        'error_messages': defaultdict(int)
    }

    try:
        with open(filepath, 'r') as f:
            for line in f:
                results['total_lines'] += 1
                line = line.strip()

                # Find log level and count it
                match_level = re.search(r'\b(ERROR|WARNING|INFO)\b', line)
                if match_level:
                    level = match_level.group(1)
                    results['line_counts'][level] += 1
                
                # Find timestamps
                match_time = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
                if match_time:
                    try:
                        timestamp = datetime.strptime(match_time.group(0), '%Y-%m-%d %H:%M:%S')
                        results['timestamps'].append(timestamp)
                    except ValueError:
                        pass
                
                # Find error messages
                if 'ERROR' in line:
                    error_message = re.sub(r'.*ERROR:?\s*', '', line).strip()
                    if error_message:
                        results['error_messages'][error_message] += 1

    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'. Skipping.")
        return None
    except Exception as e:
        print(f"An error occurred while reading '{filepath}': {e}. Skipping.")
        return None
    
    # Sort timestamps to find first and last
    if results['timestamps']:
        results['timestamps'].sort()

    return results

def get_most_common_errors(errors_dict, num_errors=3):
    """
    Returns the most common error messages from a dictionary of errors.
    """
    common_errors = Counter(errors_dict).most_common(num_errors)
    return common_errors

def generate_summary(file_results):
    """
    Generates a formatted summary table from the parsing results.

    Args:
        file_results (dict): A dictionary where keys are filepaths and values
                             are the parsing results.
    """
    if not file_results:
        print("No valid log files to process.")
        return

    print("--- Log Analysis Summary ---")
    
    for filepath, results in file_results.items():
        if results is None:
            continue
        
        print(f"\n--- Results for: {filepath} ---")
        
        # Log counts
        print("Log Level Counts:")
        for level, count in results['line_counts'].items():
            print(f"  - {level}: {count}")

        # Timestamps
        if results['timestamps']:
            first_entry = results['timestamps'][0].strftime('%Y-%m-%d %H:%M:%S')
            last_entry = results['timestamps'][-1].strftime('%Y-%m-%d %H:%M:%S')
            print(f"\nTime Range:")
            print(f"  - First entry: {first_entry}")
            print(f"  - Last entry: {last_entry}")
        else:
            print("\nTime Range: No valid timestamps found.")
        
        # Most common errors
        common_errors = get_most_common_errors(results['error_messages'])
        if common_errors:
            print(f"\nMost Common Errors:")
            for msg, count in common_errors:
                print(f"  - ({count} times) {msg}")
        else:
            print("\nMost Common Errors: No ERROR messages found.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python log_parser.py <log_file1.log> <log_file2.txt> ...")
        sys.exit(1)
        
    log_files = sys.argv[1:]
    
    all_file_results = {}
    for log_file in log_files:
        all_file_results[log_file] = parse_log_file(log_file)
    
    generate_summary(all_file_results)
