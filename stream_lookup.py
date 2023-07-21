'''
second script used for "/stream" challenge

same as https://wordfinderx.com/words-for/_/length/7/include-letters/abiuydl/?dictionary=all_en&extended_fields=true
basically take all the letters found in the stream and try to find a 7 letter word with all the characters
'''

def read_words_from_file(file_path):
    words_list = []
    with open(file_path, 'r') as file:
        for line in file:
            # Remove any leading/trailing whitespace and append the word to the list
            word = line.strip()
            words_list.append(word)
    return words_list


if __name__ == '__main__':

    file_path = 'data/word-list-7-letters.txt'
    words = read_words_from_file(file_path)

    # set chars that were found in the stream
    characters_to_check = ['a','b','i','u','y','d','l']

    for word in words:
        if all(char in word for char in characters_to_check):
            print(word)