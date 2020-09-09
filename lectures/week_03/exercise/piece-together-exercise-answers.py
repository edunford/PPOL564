# Answers to Breakout Exercise

text = "An initial attempt to rescue the group, stranded in mountain refuge for two nights, was abandoned on Monday night because of smoke from the Creek Fire. But helicopters were able to land early on Tuesday and are have begun taking the hikers to safety. Fires in California have burned through a record 2m acres in recent weeks. In total, these blazes span an area larger than the US state of Delaware. California is currently experiencing an unprecedented heatwave."



# Count the number words in the text
# Answer: C, A, B, D
def word_count(text):
    tmp = text.split(" ")
    count = len(tmp)
    return count

word_count(text)








# Count the number of unique words.
# Answer: A, D, C, B
def unique_words(text):
    a = set(text.split(' '))
    count = len(a)
    return count

unique_words(text)


# H F D C A B E G





# Count up the number of times each word is used.
# Answer: H, F, D, A, C, B, E, G
def usage_count(text):
    words = text.split(" ")
    word_count = {}
    for word in words:
        word = word.replace(".","")
        word = word.replace(",","")
        word = word.lower()
        if word  in word_count.keys():
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count
