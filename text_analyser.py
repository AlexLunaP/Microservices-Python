import string
import re

key_words = ["conduct","contempt","covid","party",
	     	"punishment","gathering","law","responsibility"]

# Open the file in read mode
text = open("Boris.txt", "r")

# Create an empty dictionary
words_by_frequency = dict()

# Define the pattern for enumerations (letter or Roman numeral) with parentheses
enumeration_pattern = r'\b(?:[a-hj-zA-HJ-Z]|[ivxIVX]+)\)'

additional_punctuation = '“”‘’–—…«»•'

# Combine the standard punctuation, digits, and additional punctuation characters
all_punctuation = string.punctuation + string.digits + additional_punctuation

total_words = 0
total_words_length = 0
total_sentences = 0

# Loop through each line of the file
for line in text:
	# Remove the leading spaces and newline character
	line = line.strip()

	# Convert the characters in line to
	# lowercase to avoid case mismatch
	line = line.lower()

    # Remove enumerations using regex
	cleaned_line = re.sub(enumeration_pattern, '', line)

	# Remove the punctuation marks, digits, and additional punctuation from the line
	cleaned_line = cleaned_line.translate(str.maketrans('', '', all_punctuation))

	# Split the line into words
	words = cleaned_line.split()

	# Filter out empty strings from the list of words
	words = [word for word in words if word]

	# Count the total words and total words length
	total_words += len(words)
	total_words_length += sum(len(word) for word in words)

	# Count the number of sentences in the line (assuming sentences end with '.', '!', '?')
	total_sentences += len(re.findall(r'[.!?;:]', line))

	# Iterate over each word in line
	for word in words:
		#Calculate average word length
		total_words = total_words + 1
		total_words_length = total_words_length + len(word)

		if word in key_words:
			# Check if the word is already in dictionary
			if word in words_by_frequency:
				# Increment count of word by 1
				words_by_frequency[word] = words_by_frequency[word] + 1
			else:
				# Add the word to dictionary with count 1
				words_by_frequency[word] = 1

print("Average word length = ", round(total_words_length/total_words, 4), "≈", round(total_words_length/total_words),"letters \n")
print("Average sentence length ≈", round(total_words / total_sentences, 4), "≈", round(total_words / total_sentences), "words \n")

# Print words by frequency
for key in list(words_by_frequency.keys()):
	print("The word", key, "appears", words_by_frequency[key], "times")
 