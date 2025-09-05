import sys
import re
from collections import Counter

def count_words_chars_lines(text):
    """
    Counts words, characters, and lines in a given text.
    Handles punctuation and ignores case for word counting.
    """
    # Count lines by splitting the text at newlines
    lines = text.split('\n')
    line_count = len(lines)

    # Count characters
    char_count = len(text)

    # Convert text to lowercase and remove punctuation for word counting
    cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
    
    # Split the cleaned text into words
    words = cleaned_text.split()
    word_count = len(words)
    
    return word_count, char_count, line_count, words

def find_most_common_words(word_list, n=3):
    """
    Finds the n most common words and their frequencies from a list of words.
    """
    # Use Counter to count word frequencies
    word_counts = Counter(word_list)
    
    # Find the n most common words
    most_common = word_counts.most_common(n)
    
    return most_common

def main():
    """
    Main function to run the script.
    It checks for a command-line argument and processes the text.
    """
    # Check if a text string was provided as a command-line argument
    if len(sys.argv) < 2:
        print("Error: No text string provided.")
        print("Usage: python word_counter.py \"Your text string here.\"")
        sys.exit(1)

    # Get the text from the command-line argument
    text_string = sys.argv[1]

    # Process the text
    word_count, char_count, line_count, word_list = count_words_chars_lines(text_string)
    most_common_words = find_most_common_words(word_list)

    # Display the results
    print(f"--- Word Counter Report ---")
    print(f"Text provided: \"{text_string}\"")
    print(f"Number of words: {word_count}")
    print(f"Number of characters: {char_count}")
    print(f"Number of lines: {line_count}")
    
    print("\nTop 3 most common words:")
    if most_common_words:
        for word, freq in most_common_words:
            print(f"  - '{word}': {freq} times")
    else:
        print("  - No words found.")

if __name__ == "__main__":
    main()
