# import wordninja


# def split_string(s):
#     return " ".join(wordninja.split(s))


# # Ví dụ sử dụng
# chuoi = "TheraininspainfallsmainlyontheplainitcanbechallengingtoreadthistextwithoutspacesbutwiththepropermethodstoolsandtechniquesitcanbeachievedsuccessfullytryusingnltklibraryforsentencetokenizationandwordtokenizationaswellasotherNLPlibrariesandtoolstohelpyourestorethespacesinthisstringofwords"
# chuoi_tach_tu = split_string(chuoi)
# print(chuoi_tach_tu)


import pymorphy2

morph = pymorphy2.MorphAnalyzer()


# Hàm tạm thời để tách từ (cần cải thiện)
def split_russian_string(s):
    words = []
    temp_word = ""
    for char in s:
        temp_word += char
        if morph.word_is_known(temp_word):
            words.append(temp_word)
            temp_word = ""
    return " ".join(words)


# Ví dụ sử dụng
chuoi = "вашпримертекста"
chuoi_tach_tu = split_russian_string(chuoi)
print(chuoi_tach_tu)
