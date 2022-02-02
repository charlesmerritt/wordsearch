import pprint as pp
import json

def main():
    # First, the file needs to take in the text files and properly parse them.
    # Separating wordbank.txt by spaces and reading wordpuzzle.txt and converting it into a nested list or a matrix.
    wordpuzzle = []
    with open('wordpuzzle.txt', 'r') as f:
        content = f.readlines()
        for single_line_letters in content:
            single_line_letters = single_line_letters.strip()
            single_line_letters = list(single_line_letters)
            wordpuzzle.append(single_line_letters)
        print("The wordpuzzle.txt matrix is...")
        pp.pprint(wordpuzzle)

    # wordpuzzle.txt has been parsed into a matrix, where each character is able to be accessed by with 2 indices [i][j]
    # Now we need to create an algorithim that can search through wordpuzzle.txt, looking for the words parsed out from
    # the wordbank.txt file. It needs to search both vertically and horizontally.
    wordbank = []
    with open('wordbank.txt', 'r') as v:
        bank = v.readline()
        bank = bank.split(' ')
        for word in bank:
            wordbank.append(word)
        print("The wordbank.txt list is...")
        print(wordbank)


    # The required search(word) method call...

    search(wordpuzzle, 'CAT')

def bank_check(temp, word):
    # helper method that goes through the temp string generated in the search methods and checks whether or not
    # the words in wordbank are found
    x = temp.find(word)
    if x != -1 or temp == word:
        print(temp)
        print("Word found!")
        return x
    return -1

def horizontal_search(wordpuzzle, word, output):
    # method to search along a single list/line of wordpuzzle and look for the presence of any item of wordbank.txt
    temp = ""
    for pos_y, row in enumerate(wordpuzzle):
        for letter in row:
            temp += letter
        forwards_x = bank_check(temp, word)
        backwards_x = bank_check(temp[::-1], word)
        if forwards_x != -1:
            output[word]['position'].append([forwards_x + 1, pos_y + 1])
            output[word]['direction'].append('forwards')
        elif backwards_x != -1:
            output[word]['position'].append([len(row) - backwards_x, pos_y + 1])
            output[word]['direction'].append('backwards')
        temp = ""

def vertical_search(wordpuzzle, word, output):
    # method to search up/down thru wordpuzzle and look for the presence of any item of wordbank.txt
    length = len(wordpuzzle)
    temp = ""
    for i in range(length):
        for j in range(length):
            temp += wordpuzzle[j][i]
        down_x = bank_check(temp, word)
        up_x = bank_check(temp[::-1], word)
        if down_x != -1:
            output[word]['position'].append([i + 1, down_x + 1])
            output[word]['direction'].append('down')
        elif up_x != -1:
            output[word]['position'].append([i + 1, length - up_x])
            output[word]['direction'].append('up')
        temp = ""

def diagonal_search(wordpuzzle, word, output):
    # method to search diagonal thru wordpuzzle and look for the presence of any item of wordbank.txt
    temp = ""
    length = len(wordpuzzle)
    # down forwards | up backwards
    for i in range(length - 2, 0, -1):
        row_i = i
        col_i = 0
        while (True):
            if row_i >= length:
                break
            temp += wordpuzzle[row_i][col_i]
            row_i += 1
            col_i += 1
        x_pos = bank_check(temp, word)
        backwards_x_pos = bank_check(temp[::-1], word)
        if x_pos != -1:
            output[word]['position'].append([x_pos + 2, i + 2])
            output[word]['direction'].append('downforwards')
        if backwards_x_pos != -1:
            output[word]['position'].append([backwards_x_pos + 2, i + 2])
            output[word]['direction'].append('upbackwards')
        temp = ""
    # down forwards pt 2 | up backwards pt 2
    for i in range(length - 2, -1, -1):
        row_i = 0
        col_i = i
        while(True):
            if col_i >= length:
                break
            temp += wordpuzzle[row_i][col_i]
            col_i += 1
            row_i += 1
        x_pos = bank_check(temp, word)
        backwards_x_pos = bank_check(temp[::-1], word)
        if x_pos != -1:
            output[word]['position'].append([x_pos + 2, i + 2])
            output[word]['direction'].append('downforwards')
        if backwards_x_pos != -1:
            output[word]['position'].append([backwards_x_pos + 2, i + 2])
            output[word]['direction'].append('upbackwards')
        temp = ""
    # down backwards | up forwards
    for i in range(length - 2, 0, -1):
        row_i = i
        col_i = length - 1
        while(True):
            if row_i >= length:
                break
            temp += wordpuzzle[row_i][col_i]
            col_i -= 1
            row_i += 1
        x_pos = bank_check(temp, word)
        backwards_x_pos = bank_check(temp[::-1], word)
        if x_pos != -1:
            print(f"downbackwards {x_pos}")
            print(f"downbackwards {i}")
            output[word]['position'].append([length - x_pos, i + 1])
            output[word]['direction'].append('downbackwards')
        if backwards_x_pos != -1:
            print(f"upforwards {backwards_x_pos}")
            print(f"upforwards {i}")
            output[word]['position'].append([length - i, length - backwards_x_pos])
            output[word]['direction'].append('upforwards')
        temp = ""
    # up forwards pt 2 | down backwards pt 2
    for i in range(1, length):
        row_i = i
        col_i = 0
        while(True):
            if row_i < 0:
                break
            temp += wordpuzzle[row_i][col_i]
            row_i -= 1
            col_i += 1
        x_pos = bank_check(temp, word)
        backwards_x_pos = bank_check(temp[::-1], word)
        if x_pos != -1:
            print("test")
            output[word]['position'].append([x_pos + 2, i + 2])
            output[word]['direction'].append('upforwards')
        if backwards_x_pos != -1:
            print("test")
            output[word]['position'].append([backwards_x_pos + 2, i + 2])
            output[word]['direction'].append('downbackwards')
        temp = ""



def search(wordpuzzle, word):
    # cohesive search(word) method allows you to use all functions for search within one method, this function also
    # yields the output in JSON format.
    output = {word: {'position': [], 'direction': []}}
    horizontal_search(wordpuzzle, word, output)
    vertical_search(wordpuzzle, word, output)
    diagonal_search(wordpuzzle, word, output)
    print(output)
    with open('output.json', 'w') as f:
        f.write(str(output))


if __name__ == '__main__':
    main()

