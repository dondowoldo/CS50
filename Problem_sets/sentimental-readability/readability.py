from cs50 import get_string


def main():
    text = get_string("Text: ")

    # Prints Grade +16 if the rounded coleman index is greater or equal to 16
    if coleman_index(count_letters(text), count_words(text), count_sentences(text)) >= 16:
        print("Grade 16+")

    # Prints Before Grade 1 if the rounded coleman index is less than 1
    elif coleman_index(count_letters(text), count_words(text), count_sentences(text)) < 1:
        print("Before Grade 1")

    # Prints specific readability grade for a text input by user
    else:
        print(f"Grade {coleman_index(count_letters(text), count_words(text), count_sentences(text))}")

    # Check if character [i] is alphabetic and increase count by 1 if so


def count_letters(text):
    letters = 0
    for i in range(len(text)):
        if text[i].isalpha():
            letters += 1
    return letters

    # Check if character [i] is a space and increase count by 1 if so


def count_words(text):
    spaces = 0
    words = 0
    for i in range(len(text)):
        if text[i].isspace():
            spaces += 1
    words = spaces + 1
    return words

    # Check if character [i] is "?", "!", or "." and if so, increase count of sentences by 1
    

def count_sentences(text):
    sentences = 0
    for i in range(len(text)):
        if text[i] == "?" or text[i] == "!" or text[i] == ".":
            sentences += 1
    return sentences

    # Calculating readability grading based on the Coleman-Liau index


def coleman_index(letters, words, sentences):
    l = (letters / words) * 100
    w = (sentences / words) * 100
    index = (0.0588 * l) - (0.296 * w) - 15.8
    return round(index)


if __name__ == "__main__":
    main()