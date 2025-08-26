    # file="iogytcytcyaeugvut nnruonfwnfiwfffwefrrg Facetious Abstemiously Facetiously Adventitious bro Adventitiously Abstemious"
    # content = file.read()
    # c=content.lower()
    # w=c.split()
    # d=[]
    # p=[]
    # for i in w:
    #     print("I",i)
    #     for j in i:
    #         if j in 'aeiou':
    #             p.append(j)
    #             if p==['a','e','i','o','u']:
    #                 d.append(i)

    # print("words with vowels in order are:",d)
    # print(w)
# Sample list of words; you can replace this with your own list or input
words = [
    "facetious", "abstemiously", "education", "sequential", "author", "abstemious",
    "facetiously", "subcontinental", "automobile", "queasy"
]

def has_vowels_in_order(word):
    vowels = "aeiou"
    idx = 0
    for char in word.lower():
        if idx < len(vowels) and char == vowels[idx]:
            idx += 1
    return idx == len(vowels)

print("Words with all vowels in alphabetical order:")
for word in words:
    if has_vowels_in_order(word):
        print(word)