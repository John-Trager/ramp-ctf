'''
"/exception" challenge

known constraints:
- 7 chars
- doesn't start with H
- DoesNotSumToFortyTwoCaseInsensitive
- no L
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

    file_path = 'data/word-42-list.txt'
    words = read_words_from_file(file_path)


    for word in words:
        if word[0].lower() == 'h':
            continue

        if len(word) != 7:
            continue

        if 'l' in word.lower():
            continue

        print(word)



