def generate_binary_labels_from_file(file_path):
    all_labels = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Extract the sentence part from the line
                sentence = line.strip().split('. ', 1)[-1]
                # Generate a list of 0s and 1s (0 for non-space, 1 for space)
                binary_labels = [1 if char == ' ' else 0 for char in sentence]
                all_labels.append(binary_labels)
                print("Binary labels for line:", binary_labels)  # Optional: Print each line's labels
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return all_labels

# Path to your sentences file
sentences_file_path = 'sentences.txt'
binary_labels = generate_binary_labels_from_file(sentences_file_path)

# Optional: Print all labels
print(binary_labels)
print(len(binary_labels))
