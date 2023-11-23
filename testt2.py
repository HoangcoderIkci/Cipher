strEncr = """
ЮРЬЙЖ КБМПО ЬЛФКЯ ЖКЬЗГ ЦЗЭЦУ КПДЭЖ ЫЦДЭЖ ЫЦДШН ШЦЮЦО ЖИЬОФ ЭЗЦРЦ СЬЫБЭ ЖГЖШЖ ДЦЖАК НРФКК ЬБШФЭ ТДЖСЦ ЭЦРПЩ НКФЕМ ПОЦШГ ФКЬШИ ЬЭТУФ ОЦГФС ДФШОЖ ЭФОТК ЦЗЭТФ ФШГЖЛ ФКЖЕЖ ЮЦГЦР ЬЫРЦЖ ЗЩЦШЖ ГВЬБЦ ЭЗОЬМ ЦЗЭЖЭ ЖОЫРЖ ШЬГЬО ЬФЕАК БУЖЭФ ОТКПЕ ГЖШГК НВЬГВ ЖЕНГЬ ЛФКЖФ СКБЮЖ КБЬКК ЬДЖЩЬ ЕОЦГК ЬШРНМ ФИСЬБ СЬСШЦ ДЬВКЖ ЕУФОЦ ГФСЗЖ ШФОЬЭ НЭЛФЫЦДЦЮЬБГШФОФЫРЖКЖДЬКЖБЖАЬК ЖДЬКЖБРЬАЮЦГЦРЦДЮЦЗЭФЕ
"""

strEncr = strEncr.replace("Ъ", "ь")
strEncr = strEncr.replace(" ", "")
strEncr = strEncr.replace("\n", "")
strEncr = strEncr.upper()
print((23 * -4) % 31)
for i in strEncr:
    o = ord(i) - ord("А")
    o = (o * 23) % 31
    print(chr(o + ord("А")), end="")
# dict_big = {}
# temp = ()
# for i in range(len(strEncr) - 3):
#     temp = (strEncr[i], strEncr[i + 1], strEncr[i + 2], strEncr[i + 3])
#     if temp not in dict_big:
#         dict_big[temp] = 1
#     else:
#         dict_big[temp] += 1
# sorted_dict = dict(sorted(dict_big.items(), key=lambda item: item[1]))
# with open("TEXT.txt", "w", encoding="utf-8") as f:
#     # for k, v in sorted_dict.items():
#     #     f.write(f"  {k} : {v}   ")
#     f.write(strEncr)
# l = ["Ж", "О", "К", "Н"]
# for i in l:
#     print(ord(i) - ord("А"))
# print((6 - 27 * 14) % 31)
