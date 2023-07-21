'''
"/hash" challenge
'''
import hashlib

def crack_md5_hash(plaintext, salt, target_hash):
    # Concatenate plaintext and salt
    data = plaintext + salt

    # Calculate the MD5 hash
    md5_hash = hashlib.md5(data.encode()).hexdigest()

    # Compare with the target hash
    if md5_hash == target_hash:
        return plaintext
    else:
        return None

def read_words_from_file(file_path):
    words_list = []
    with open(file_path, 'r') as file:
        for line in file:
            # Remove any leading/trailing whitespace and append the word to the list
            word = line.strip()
            words_list.append(word)
    return words_list


if __name__ == '__main__':
    known_salt = "449f6ff92e44"
    target_md5_hash = "7a4e24bf3da8d7fb2367dd1009d791d8"

    file_path = 'data/word-list-7-letters.txt'
    words = read_words_from_file(file_path)


    for word in words:
        ans = crack_md5_hash(word, known_salt, target_md5_hash)

        if ans != None:
            print(ans)
            break