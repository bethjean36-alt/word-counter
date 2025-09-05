import sys
import string
from collections import Counter
import os

def word_counter(text):
    """
    Analyzes a given text to count words, characters, and lines,
    and finds the three most common words.

    Args:
        text (str): The input text to analyze.

    Returns:
        tuple: A tuple containing:
               - An integer for the word count.
               - An integer for the character count.
               - An integer for the line count.
               - A list of the three most common words and their counts.
    """
    # Count characters and lines
    char_count = len(text)
    line_count = text.count('\n') + 1 if text else 0

    # Process text for word counting and frequency analysis
    # Convert to lowercase to make counting case-insensitive
    processed_text = text.lower()
    
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    processed_text = processed_text.translate(translator)
    
    # Split text into words and count them
    words = processed_text.split()
    word_count = len(words)
    
    # Find the 3 most common words
    word_counts = Counter(words)
    most_common_words = word_counts.most_common(3)
    
    return word_count, char_count, line_count, most_common_words

def main():
    """
    Main function to read text from either a command-line argument,
    a file, or standard input, and then display the analysis results.
    """
    text_to_analyze = ""
    # Check if a command-line argument is provided
    if len(sys.argv) > 1:
        # Check if the argument is a file path
        if os.path.exists(sys.argv[1]):
            try:
                with open(sys.argv[1], 'r', encoding='utf-8') as file:
                    text_to_analyze = file.read()
            except Exception as e:
                print(f"An error occurred while reading the file: {e}")
                sys.exit(1)
        else:
            # If the argument is not a file, treat it as the text to analyze.
            text_to_analyze = sys.argv[1]
    else:
        # If no argument is provided, read from standard input
        print("Reading from standard input. Press Ctrl+D (or Ctrl+Z on Windows) to stop.")
        text_to_analyze = sys.stdin.read()

    # If there's no text, print a message and exit
    if not text_to_analyze:
        print("No text was provided for analysis.")
        return

    # Perform the analysis
    word_count, char_count, line_count, most_common = word_counter(text_to_analyze)

    # Print the results
    print("\n--- Analysis Results ---")
    print(f"Total Words: {word_count}")
    print(f"Total Characters: {char_count}")
    print(f"Total Lines: {line_count}")
    
    print("\nTop 3 Most Common Words:")
    if most_common:
        for word, count in most_common:
            print(f"  '{word}': {count} times")
    else:
        print("  (No words found)")

if __name__ == "__main__":
    main()
