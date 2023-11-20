deText = "АННЮИ ОМТДА ТЪОЯЛ ЩТРИП ООСИС МВИЕЗ ИКРОТ УБУОВ СЫНЗТ АЕКАЛ ИНСЕМ НЯАРЕ ЕЧОНТ ОНПХИ АЫЛСВ ОЕТАП НКИРМ ИИОНС ЫЫХВВ РАОНЛ ЙСОКЕ ЕЧЕАП АВСОЕ ПРОНЕ ВИНАЛ ПЫНАЫ ЛНОАВ ААЙИМ ВХНЬЕ ВАКРС СУНМЛ ОКВСМ МУЙОР ПВЯОР БОЫВО ТМАГД ТОРЕО АВНОМ ИНСКТСЫНСЧМХЭАДЫЛЬ"
# Loại bỏ khoảng trắng trong chuỗi
deText = deText.replace(" ", "")
deText = deText.replace(",", "")
deText = deText.replace(".", "")
deText = deText.replace("й", "и")
print(deText)
print(len(deText))
deText = deText.upper()
LEN_KEY = 13
col = LEN_KEY
row = int(len(deText) / col)
sec_key = [2, 3, 4, 1, 10, 8, 7, 5, 9, 11, 6]
for i in range(len(sec_key)):
    sec_key[i] -= 1
print(sec_key)
TEXT = [list(deText[i : i + col]) for i in range(0, len(deText), col)]
for rom in TEXT:
    for id in sec_key:
        print(rom[id], end="")
