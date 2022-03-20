# Proprietary content. ©Great Learning. All Rights Reserved. Unauthorized use or distribution prohibited

import concurrent.futures
import time
import re


# function to find no of words in a sentence
def number_of_words(sentence):
    # splits the sentence into a list of words
    number_of_words = len(sentence.split())
    print("\nNumber of words in the sentence : {}".format(number_of_words))
    time.sleep(1)


# function to find no of characters in a sentence
def number_of_characters(sentence):
    number_of_characters = len(sentence)
    print("\nNumber of characters in the sentence : {}".format(number_of_characters))
    time.sleep(1)


# function to find no of odd words in a sentence
def number_of_odd_words(sentence):
    odd_word_count = 0
    # first split into a list of words
    word_list = sentence.split()
    for words in word_list:
        # for each word check if it contains odd no. of characters
        if (len(words) % 2) != 0:
            odd_word_count = odd_word_count + 1
    print("\nNumber of odd words in the sentence : {}".format(odd_word_count))
    time.sleep(1)


# function to find no of vowels in a sentence
def number_of_vowels(sentence):
    # create a regular expression to check all the vowels
    regexPattern = re.compile('[aeiouAEIOU]')
    # check if the sentence has any of the characters listed in the pattern
    listOfmatches = regexPattern.findall(sentence)
    print("\nNumber of vowels in the sentence : {}".format(len(listOfmatches)))
    time.sleep(1)


if __name__ == '__main__':
    sentence = "ThreadPoolExecutor is an essential component in achieving Thread pool pattern in python."
    # start counter to check execution time of all the tasks in thread pool
    start = time.perf_counter()
    # Create a thread pool with required no. of threads
    with concurrent.futures.ThreadPoolExecutor(4) as executor:
        futures = []
        # assign task for each thread (not in our control!)
        futures.append(executor.submit(number_of_words, (sentence)))
        futures.append(executor.submit(number_of_characters, (sentence)))
        futures.append(executor.submit(number_of_vowels, (sentence)))
        futures.append(executor.submit(number_of_odd_words, (sentence)))
        # wait until all the threads are complete
    # end counter to check execution time of all the tasks in thread pool
    finish = time.perf_counter()
    # print time taken to execute the commands
    print(f'\nFinished in {round(finish - start, 2)} second(s)')

