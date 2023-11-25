#!/usr/bin/env python
# coding: utf-8

# In[19]:


import Vigenere_Functions as funcs

english_frequencies = {'a':8.4966,'b':2.0720,'c':4.5388,'d':3.3844,'e':11.1607,'f':1.8121,'g':2.4705,'h':3.0034,'i':7.5448,'j':0.1965,'k':1.1016,'l':5.4893,'m':3.0129,'n':6.6544,'o':7.1635,'p':3.1671,'q':0.1962,'r':7.5809,'s':5.7351,'t':6.9509,'u':3.6308,'v':1.0074,'w':1.2899,'x':0.2902,'y':1.7779,'z':0.2722}
lst_percentages = [7.55,1.61,5.22,1.68,3.06,8.16,0.74,1.89,7.26,1.42,3.43,4.05,2.85,6.58,11.91,2.68,5.05,5.77,5.96,2.33,0.19,1.39,0.54,0.13,0.82,0.38,2.09,1.41,0.25,0.67,1.75]
lst_percentages.insert(26,0.06)
english_frequencies = dict(zip(funcs.alphabet,lst_percentages))
english_data = [j/100 for i,j in english_frequencies.items()]


###
###            
### Various functions

def indexes(words,word):
    results = []
    for i in range(0,len(words)):
        try:
            index = words.index(word,i)
        except:
            break
        if index not in results:
                results.append(index)
    return results
            

#Factorizing Algorithm
def factorize2(number):
    while number>1:
        for i in range(2,number+1):
            if number%i==0:
                number = int(number/i)
                yield i
                break

###
###
###


class Twist:
    
    def __init__(self, key_length_upper_limit, text):
        """
        Initialises the class used to perform the Twist Algorithm to find the key length.
        
        Parameters:
        key_length_upper_limit (integer): Keys of length 0 to this number will be checked
        text (string) : The ciphertext that you want to decipher
        """
        self.n = key_length_upper_limit
        self.encrypted = text
    
    def letter_percentages(self):
        """
        Produces an array with the rate at which each letter of the alphabet occurs within the n subsections of the ciphertext,
        for each different key of length n.
        
        
        """
        all_key_lengths = {}
        for m in range(1,self.n+1):
            nth_letter_2 = {}
            for i in range(0,m):
                nth_letter_2[i] = self.encrypted[i::m]
            all_key_lengths[m] = nth_letter_2

        all_key_frequencies = {}
        for k,dicts in all_key_lengths.items():
            letter_frequencies = {}
            for i,j in dicts.items():
                letter_counts = {}
                for letter in j:
                    if letter not in letter_counts:
                        letter_counts[letter]=0
                    letter_counts[letter]+=1
                letter_frequencies[i]=letter_counts
            all_key_frequencies[k]=letter_frequencies

        all_key_letters = {}
        for length in all_key_frequencies:
            sub_dict = {}
            for num in all_key_frequencies[length]:
                letters_in = []
                for letter in all_key_frequencies[length][num]:
                    letters_in.append(letter[0])
                    #letters_in.append(letter)
                sub_dict[num]=letters_in
            all_key_letters[length]=sub_dict


        all_key_frequencies_complete = all_key_frequencies
        for j in funcs.alphabet:
            for index in all_key_letters:
            #for index in all_key_letters.keys():
                for i in all_key_letters[index]:
                    if j not in all_key_letters[index][i]:
                        all_key_frequencies_complete[index][i][j]=0



        all_key_frequencies_complete_sorted = {}
        for index in all_key_frequencies_complete:
            sub_dict = {}
            for i in all_key_frequencies_complete[index]:
                sub_dict[i] = (sorted(all_key_frequencies_complete[index][i].items(),key=lambda letters: letters[1], reverse=True))
            all_key_frequencies_complete_sorted[index] = sub_dict


        all_key_percentages = {}
        for i in all_key_frequencies_complete_sorted:
            sub_dict = {}
            for j in all_key_frequencies_complete_sorted[i]:
                percentage_list_2 = []
                if (j-1)<=(len(self.encrypted)%i):
                    divisor = (len(self.encrypted)//i)+1
                else:
                    divisor = len(self.encrypted)//i

                for k in all_key_frequencies_complete_sorted[i][j]:
                    tuple_new = (k[0],k[1]/divisor)
                    percentage_list_2.append(tuple_new)
                sub_dict[j] = percentage_list_2
            all_key_percentages[i]=sub_dict

        return all_key_percentages
    
    def twist_values(self, all_key_percentages):
        """
        Implements the twist algorithm to measure the unevenness of the distribution of letters in all the subsections.
        The percentage
        """
        Cj_dict = {}
        for i in all_key_percentages:
            final_list = [0 for l in range(0,funcs.SO_LUONG_CAI)]
            #final_list = [0*l for l in range(0,funcs.SO_LUONG_CAI)]
            for j in all_key_percentages[i]:
                Cj_list = [k[1] for k in all_key_percentages[i][j]]
                final_list = [final_list[n]+Cj_list[n] for n in range(0,len(Cj_list))]
            # print(sum(final_list))
            Cj_dict[i]=final_list


        twists = {}
        for i in Cj_dict:
            twist = 0
            for j in enumerate(Cj_dict[i]):
                if j[0]<int(funcs.SO_LUONG_CAI/2):
                    twist+=j[1]
                else:
                    twist-=j[1]
            twist=twist*(100/i)
            twists[i]=twist
        return twists
    
    def key_length(self, twists, method):
        """
        Calculates the most likely key length. For the twist algorithm this is the key length with the highest twist value.
        For the twistplus algorithm the previous twist values are taken into account to look for a significant jump in the value.
        
        Parameters:
        twists (array): An array of the key lengths and the twist values associated with them.
        method (string): A string to choose which algorithm you want to implement to give the key length.
        
        Returns:
        mode (integer): An integer giving the most likely length of the key.
        """
        #print(twists)
        if method == "twist":
            mode_value = 0
            for i,j in twists.items():
                if j>mode_value:
                    mode = i
                    mode_value = j
            sort_key = sorted(twists.items(), key=lambda x: x[1], reverse=True)
            return mode,sort_key
        elif method == "twistplus":
            twistplus = {}
            twistlist = [x[1] for x in twists.items()]
            for i in twistlist:
                subtract = 0
                for j in range(0,twistlist.index(i)):
                    subtract+=(twistlist[j]/twistlist.index(i))
                number = i - subtract
                if twistlist.index(i)!=0:
                    twistplus[twistlist.index(i)+1]=number
            
            mode_value = 0
            for i,j in twistplus.items():
                if j>mode_value:
                    mode = i
                    mode_value = j
            return mode,sorted(twistplus.items(), key=lambda x: x[1], reverse=True)
        else:
            raise ValueError("Oops! Unrecognised method in Twist.key_length() ,it must either be twist or twistplus.")



                
class Kasiski:
    
    def __init__(self, text):
        """
        Initialises the class used to perform the Kasiski Algorithm to find the key length.
        This tries to look for repeated fragments of multiple letters within the ciphertext, by taking the distance between
        repeats you can guess the key length.
        
        Parameters:
        text (string) : The ciphertext that you want to decipher
        """
        self.encrypted = text
    
    def repeats(self, n):
        """
        Produces all n letter repeated fragments of text with the number of times they occur.
        
        Parameters:
        n (integer) : The length of the repeated fragments you want to search for.
        
        Returns:
        elements (array) : An array of all the n letter fragments of text within the ciphertext
        filtered (dictionary) : An array of the repeated n letter fragments of text, with the number of times they're repeated.
        """
        
        elements = []
        for i in range(0,len(self.encrypted)):
            if i<(len(self.encrypted)-n+1):
                j=0
                string = ""
                while j<n:
                    string = string + self.encrypted[i+j]
                    j+=1
                elements.append(string)

        duplicates = {}
        for i in elements:
            if i not in duplicates:
                duplicates[i]=0
            duplicates[i]+=1

        filtered = {}
        for i,j in duplicates.items():
            if j!=1:
                filtered[i]=j
        
        return (elements, filtered)
    
    def spacings(self, elements, filtered):
        numbers = []
        for i in range(0,len(filtered)):
            numbers.append(indexes(elements,list(filtered)[i]))

        difference =[]
        for i in numbers:
            for j in range(0,len(i)-1):
                difference.append(i[j+1]-i[j])
        return difference
    
    def key_length(self, difference):
        kas_factors={}
        for i in range(2,len(self.encrypted)):
            counts=0
            for d in difference:
                if d%i==0:
                    counts+=1
            if counts!=0:
                kas_factors[i]=counts
        sorted_kas_factors = dict(sorted(kas_factors.items(), key=lambda item: item[1], reverse=True))
# Sắp xếp kas_factors theo thứ tự giảm dần của value và lưu vào sorted_kas_factors.
        # kas_mode = 0
        # for i in kas_factors:
        #     x = kas_factors[i]
        #     if x>=kas_mode:
        #         kas_mode=i

        return next(iter(sorted_kas_factors)),sorted_kas_factors
    
class Frequency:
    
    def __init__(self, length):
        """
        Used to find the most likely shift for each subsection of letters within the ciphertext.
        
        Parameters:
        length (integer) : The assumed key length.
        """
        self.mode = length
    
    def likely_letters(self, encrypted):
        nth_letter = {}
        for i in range(0,self.mode):
            nth_letter[i] = encrypted[i::self.mode]

        letter_frequencies = {}
        for i,j in nth_letter.items():
            letter_counts = {}
            for letter in j:
                if letter not in letter_counts:
                    letter_counts[letter]=0
                letter_counts[letter]+=1
            letter_frequencies[i]=letter_counts
            
        

        sorted_frequencies_alphabetical = {}
        for i in letter_frequencies:
            sorted_frequencies_alphabetical[i] = (sorted(letter_frequencies[i].items(), key=lambda letters: letters[0]))

        all_present_letters = {}
        for i in sorted_frequencies_alphabetical:
            letter_list = []
            for k in sorted_frequencies_alphabetical[i]:
                letter_list.append(k[0])
            all_present_letters[i]=letter_list

        sorted_frequencies_alphabetical_complete = sorted_frequencies_alphabetical
        for j in funcs.alphabet:
            for i in all_present_letters:
                if j not in all_present_letters[i]:
                    position = funcs.alphabet.index(j)
                    insert_element = (j,0)
                    sorted_frequencies_alphabetical_complete[i].insert(position, insert_element)

        sorted_frequencies_percentages = {}
        for i in sorted_frequencies_alphabetical_complete:
            percentage_list = []
            if i<=(len(encrypted)%self.mode):
                divisor = (len(encrypted)//self.mode)+1
            else:
                divisor = len(encrypted)//self.mode
            for j in sorted_frequencies_alphabetical_complete[i]:
                new_tuple = (j[0],j[1]/divisor)
                percentage_list.append(new_tuple)
            sorted_frequencies_percentages[i]=percentage_list

        test_percentages = [[x[1] for x in sorted_frequencies_percentages[i]] for i in sorted_frequencies_percentages]

        cycle_list2 = []
        for j in range(0,len(test_percentages)):
            append_list = []
            for n in range(0, len(test_percentages[j])):
                append_list.append(test_percentages[j][n::]+test_percentages[j][0:n:])
            cycle_list2.append(append_list)

        statistical_results = []
        for n in cycle_list2:
            letter_pairs =[]
            for sublist in n:
                letter_pair = funcs.alphabet[(n.index(sublist))]   #error here, need to get the right index
                chi = 0
                for j in sublist:
                    value = ((j-english_data[sublist.index(j)])**2)/english_data[sublist.index(j)]
                    chi+=value
                t = (letter_pair,chi)
                letter_pairs.append(t)
            statistical_results.append(letter_pairs)
        #print(statistical_results)

        statistical_sorted = []
        for i in statistical_results:
            sorted_stats = sorted(i, key=lambda pair: pair[1])
            statistical_sorted.append(sorted_stats)

        return statistical_sorted
    
    def shortened_letters(self,n,statistical_sorted):
        """
        Shows the n most likely letters for the key word in each position.
        
        Parameters:
        n (integer) : The top n characters
        statistical_sorted (array) : An array of len(keyword) which contains the ordered list of the likely keyword characters.
        """
        statistical_sorted_shortened = {}
        for i in range(0,len(statistical_sorted)):
            sublist = []
            for j in range(0,n):
                sublist.append(statistical_sorted[i][j][0])
            statistical_sorted_shortened[i]=sublist
        
        return statistical_sorted_shortened
    
if __name__ == "__main__":
    normal_text = "there are various kinds of certainty. a belief is psychologically certain when the subject who has it is supremely convinced of its truth. certainty in this sense is similar to incorrigibility, which is the property a belief has of being such that the subject is incapable of giving it up.but psychological certainty is not the same thing as incorrigibility. a belief can be certain in this sense without being incorrigible; this may happen, for example, when the subject receives a very compelling bit of counterevidence to the (previously) certain belief and gives it up for that reason."
    normal_text="""Technology has profoundly transformed our lives, creating both opportunities and challenges in every sector of society. From the way we communicate to the manner in which we travel and work, it has ushered in a new era of efficiency and connectivity. The advent of the internet and mobile technology has made information accessible to a wider audience, democratizing knowledge and fostering innovation.

In the field of healthcare, technology has revolutionized the way we diagnose and treat illnesses. Advanced medical devices and sophisticated software enable doctors to provide more accurate diagnoses and personalized treatments, improving patient outcomes. Telemedicine, a relatively new concept, allows patients to consult with healthcare professionals remotely, making healthcare more accessible to people living in remote areas.

Education has also been transformed by technology. The traditional classroom setting is being supplemented with digital learning tools, online courses, and virtual classrooms. These advancements have made education more flexible and inclusive, allowing students from different backgrounds to access quality education. Interactive learning platforms and educational apps make learning more engaging and effective.

In the business world, technology has changed the way companies operate and compete. E-commerce platforms have opened up new markets, enabling small businesses to reach customers globally. Automation and artificial intelligence have streamlined business processes, increasing productivity and reducing costs. Big data analytics allows businesses to make more informed decisions, tailoring their products and services to meet customer needs.

However, technology also presents significant challenges. The rapid pace of technological change can lead to job displacement as automation replaces human labor. Cybersecurity is another major concern, as the increasing amount of data stored online makes businesses and individuals vulnerable to cyberattacks. Ensuring data privacy has become more challenging, raising ethical questions about the use and sharing of information.

The impact of technology on the environment is another critical issue. While technological advancements have improved energy efficiency, they have also led to increased consumption and waste. Electronic waste is a growing problem, with millions of devices being discarded each year. The production and disposal of these devices have significant environmental impacts.

Socially, technology has changed the way we interact with each other. Social media platforms have connected people across the globe, but they have also contributed to the spread of misinformation and the erosion of privacy. The constant connectivity can lead to increased stress and reduced face-to-face interactions, affecting mental health.

Despite these challenges, the potential of technology to improve lives and solve complex problems is immense. Governments, businesses, and individuals must work together to harness the benefits of technology while mitigating its negative impacts. This includes investing in education and training to prepare the workforce for the jobs of the future, implementing robust cybersecurity measures, and promoting responsible use of technology.

As we look to the future, the integration of technology into our lives is set to continue. Emerging technologies like artificial intelligence, the Internet of Things, and blockchain have the potential to bring about even greater changes. It is crucial that we approach these advancements with a sense of responsibility and a commitment to creating a better, more sustainable world for future generations.

In conclusion, technology is a powerful tool that has the ability to transform every aspect of our lives. While it brings numerous benefits, it also poses significant challenges that require careful consideration and proactive management. By embracing technology with a balanced and thoughtful approach, we can ensure that its advancements contribute positively to society and the planet.
"""
    #normal_text = "OMILASCSIGWHWGMWLSHRUPABGHRJAWXQRHFYTTXCIJAKXINXZRIJDALFKXUVGYEMVQTZEEYKNEYPVRIMHPRVQMXCFITXQZDMWFXQKXLLWVQUIOINVGCIPSDQWVXJEKZBUXUIDEPVTYMERPOGUAVXTIKLPRILCSEOWMVPPZYJCMXIQMEEPMLLVRJNKJSMTMGVRFEEYKURAITXKDXACYOPKEQZVRVWUALVDVZIERVXCVSTSSDTKXRGYRQTDNCYVASEQIZRHWGTEKDWTEPGVWUQQSIKJICMQIIEWLXLRTZNJIZSTVCBXGMEBSTSJPVHIMPUHWJAZIEMEKKVCVZROQURUBOMPBWLJZZTJSSLVENBWJEIZNZIPLESNWVFLRNZKZBPLXKWCPDVYBNIJEPAGLXHKEJAKEAHKVGIIPPCIMYWRWYEFDPUGVYUKHVGRPFMKPGVNITHFSGLKAIPGROMJWBJKACZTLRRWTKHBGKSTAIVTIJDOHRQFVGIRJYIVBKHVEXRQATZEEYXKVFSEENQOLHKMMGXZIEXUNXTTIJDORTTRXKMCASLOKUQRWYXGTTTIUDKORRJRVGTPAMMZTERRATSPKTWXWVTRSJWGEVQTUXJOWISAWLPVEXALYZIRXUGRVGXGVJVNAOSAECWTMBVXVGGLQNOZRIPTHPKCKGVRQFVGIRJIJNQHPRXFTGWESICDDORTMEVGUDAIRMMGWUBOIFCRHXZJVNEFECWQJTLRKMITWSSIQGLQFXVXPTSYSXCJBWLXIVLOXVSEENKAHWJMWUQFIKXKVVPWSZQTKFYGTNMBLRKZLCMGLUMIQIHPCZIXRVRXXQWAZJFITORRGFYTATZJRILBMEXLENKAHWJMWUQFLKLGATHHMVVIIZIEXUPPCIDVLKIQYTEVQDUQFMMLPRBZFNMPUHZIKRYFMMIHIASSNDVMWGYUIPBHMVFHLOJSIIIPBQHGBBZUYAHJXQIRJIJNYAEYMKCGLJJEKDWTLVRKITIRAMMZTKEERZRIXAHXWJZSWNRUIFCRHXZJVGPNTGWOIZLPVVZTMAKDSTMTUKRBQTKNRUIHNTJXZQMNBKMEXJMQBWZIMYWJSIPFNILGYIWRSTCYEUKWHRXZLZLRARCEWBWEEDMYSCIIEVMPUHTJUVIGIYIIKDTQVMKKTYEKJQZBZLRQMUTRRVHWXCLADVZQIGWWIPIQSMEBASEYPSYUQCLWJZAZSEIRGJKJZXFHMXWTPFFCTAFLRPBUQNXZSPICKEIOQLMPMRPKVILPCDOKRPIYEXMHAVVVURMAIUFWAXUIJNXXSPIJWGAUPRTMMGWVRXTTWSBGKDDOXLEEHTMSBGZIOISFXJLDQVKEKVITEYCKMEAPSPFRAHYFMEIUATZXFHIQIZSIIKVUVVDZLJIPMJMQVHMXRDTUVVRXXJMXYTIJLAGGWRRFATYZZXMYXBQVIVKJZXFHMXRRIUWJFMOSNZDKVSXVGJVDSSXTIRWBTIIUMCAWJDOTMSMTEPBROECGMTKRWYXJMGHTZYXGGRSWXGKWUSCJOOGNPTLCVVLGRITKEQXFNQJSPWGGIIIZIEXCAPBXFHIZMBRIIRTPJIJCCSEAPRFQZWJCSZZYIPYIMVGXZEEJBNIEQRNQZRVRTZZTJNWKLGQCJVVVAORTEDSWVIVJUVBGWGSIIFWCSMEZUGORWSYUQCLWJZAGRQMEHKDXKYRGABYYRVVCJALXFXGHIEEKXCKZZLVIAAVVRXHCBPWVZQIICUEJFGKDTIDJZKGUECPGVVPRXAZGMFMEKGBWPGRGYAIFXZSPAPISLOBNIHWVEPLHOEIDVMSSMEJQZBHXZJVNBKXYIKUEHGKJNZIPLESNWVFSEOPKIAZZVQVBLRKDAGRBXYITKGPXZXIRMFWLIJEWPPVOMILASCSIQRHPRYDGRPIDIPBHOEMZQSTESMIFMCLVXTMLJVGZIPKNMXYZGNEIIRPUWALHKJQTGEIRWGLRVRJPUVXVSEEPLLHWKZPKPRGKVQVXJARNBKMFEXVQEXUKGMWHPRQWAKBWTMCGQURFSWHGDXJIJWMORTHZWEIGKIUZIILLIRVJBWLTIJLAGGMFRCVSKMJKWYEYSWXJMHLHVQQIIFLRZGAXNRZAQIEAXVRXQGVRDZVZEYMDTCKIZLOSAUGVECPANILGYIWRSTCYEUKWHRXZLZLRARCYMXUXVMIIXJMKLGIROSKCMXLFSTMCTBLHZVXREGJFVOAWHZVXWTRRGKIFXTVTCZIIVBWJXJMVSSSZNHYGXYIAPPCIRGAUGBRKVKJJAIUOWZLRWGVGISVJDDAORSSIQCBXVRRILZLRIISUQDUSWKZOZNGPLVPTJSENBGRGGFRPMRAMMDBEGNRCICLIVMEXZKEFIUWVZTZWRILXIQYTIFNPJIXOWMJNGVMPBTYETOQURFJRJHMRAMEBUKRGECLGIAALYSFJIFTZXGBWLWVXPGPYIEKGAUALVKWZIAXZENWUAITCVUPBKPXQQBWVFQMRMIIJEPLHVPMZKUQCPVBRZDIPVHAOWVQDIPATOKFQMXRZIEXUNQBWZIMYWRWWEPLXUHZQQJYNPJQWAIDSIFBUKRXYITBDOEIIMYWGLVFGVTMMKNWLXRGYRQTDNCNCQRIZMKMIIIPRXDBYRRKRXKDTPQGVKZWUXYMUQCJPLYMYMAZVWVQCNMEZLAGNXZSPICKXIVQTMAKKSRZTWEIZBNIJSIOHWGJIWJZZLRNFFUWUALVACZYEIWMOXALQVIBORTVFFWAIJCSZZYIPYIMVGBLEJPZKWSEEHRZDTSKDVMVRWGSPAXIPVPAKSSXVGJVDSSXTPDBNWNINWDRXFOPKJHXLVGNIOIZIBKKEEKMQVDMXVXPTSYSXCKVIVSLMTOZRWZWUMIASTJVZMAYVLGUTYKZIOZIPLESNWVPIJGQQINVKMHQRPECDVZIYPZKGVRLJKCMORGIIRGBDMXYDVMWSEEHDTDJOTCIORUEMIVPTWSKZVZMNPKSDZXUKRWWAXRZVRIZTHXVMKNEAKVWJQIPWTMCIMNPKLCBLLEGKZUEPLKLGATHHMVVIIZIEXUEXALRNMTWRSWVGAEVRJDJOPVXPEPLPJSDHQZQRRKXQKGLEKDVMEOIKXGZUTSIZAAWGEZRCJALAFMTJJBVWYVCGLKVIMXEGMFRUPMEMEXWTGYYJMQVUAITCVUPBKPMUIEVAVMNAPGSFPVPPALRNBNINFZPKBNASKMITWSSIQGDTYCRNXKGGSWSWZAPZVNPCLVPVMVJGPRXNVAQRVFYUJTUIWDBYJVXRPUWEVWVNAOKAMWMEICAGYVTRIAKVWVPPAVVLCOVRGRVGNJSGFIAOHRVRXKWCHRUKZUEPXZZGUPUEXZUKRGLSCGUQYETDVMXRGYRQTDNCNDBNEOECEPKTKEEYBNSHKYXHCAHTGMWGGUJNIEICLRJPZKXUEKMVAPKZRIKKQRRKWEWCAVZWCZICSJMVQKLPPOWYSPMVXAICKXYZXREAIKL"
    normal_text = """ТЕХНОЛОГИЯ ГЛУБОКО ПРЕОБРАЗОВАЛА НАШУ ЖИЗНЬ, СОЗДАВАЯ КАК ВОЗМОЖНОСТИ, ТАК И ВЫЗОВЫ В КАЖДОМ СЕКТОРЕ ОБЩЕСТВА. ОТ СПОСОБА, КАК МЫ ОБЩАЕМСЯ, ДО СПОСОБА, КАК МЫ ПУТЕШЕСТВУЕМ И РАБОТАЕМ, ОНА ПРИНЕСЛА НОВУЮ ЭПОХУ ЭФФЕКТИВНОСТИ И СВЯЗАННОСТИ. ПОЯВЛЕНИЕ ИНТЕРНЕТА И МОБИЛЬНОЙ ТЕХНОЛОГИИ СДЕЛАЛО ИНФОРМАЦИЮ ДОСТУПНОЙ ШИРОКОЙ АУДИТОРИИ, ДЕМОКРАТИЗИРУЯ ЗНАНИЯ И СОДЕЙСТВУЯ ИННОВАЦИЯМ.

В ОБЛАСТИ ЗДРАВООХРАНЕНИЯ ТЕХНОЛОГИЯ РЕВОЛЮЦИОНИЗИРОВАЛА СПОСОБЫ ДИАГНОСТИКИ И ЛЕЧЕНИЯ БОЛЕЗНЕЙ. СОВРЕМЕННЫЕ МЕДИЦИНСКИЕ УСТРОЙСТВА И СЛОЖНЫЕ ПРОГРАММЫ ПОЗВОЛЯЮТ ВРАЧАМ ДЕЛАТЬ БОЛЕЕ ТОЧНЫЕ ДИАГНОЗЫ И ПЕРСОНАЛИЗИРОВАННОЕ ЛЕЧЕНИЕ, УЛУЧШАЯ ИСХОДЫ ДЛЯ ПАЦИЕНТОВ. ТЕЛЕМЕДИЦИНА, ОТНОСИТЕЛЬНО НОВАЯ КОНЦЕПЦИЯ, ПОЗВОЛЯЕТ ПАЦИЕНТАМ КОНСУЛЬТИРОВАТЬСЯ С МЕДИЦИНСКИМИ СПЕЦИАЛИСТАМИ НА РАССТОЯНИИ, СДЕЛАВ ЗДРАВООХРАНЕНИЕ БОЛЕЕ ДОСТУПНЫМ ДЛЯ ЛЮДЕЙ, ЖИВУЩИХ В УДАЛЕННЫХ РАЙОНАХ.

ОБРАЗОВАНИЕ ТАКЖЕ БЫЛО ТРАНСФОРМИРОВАНО ТЕХНОЛОГИЕЙ. ТРАДИЦИОННОЕ ОБУЧЕНИЕ В КЛАССЕ ДОПОЛНЯЕТСЯ ЦИФРОВЫМИ УЧЕБНЫМИ ИНСТРУМЕНТАМИ, ОНЛАЙН-КУРСАМИ И ВИРТУАЛЬНЫМИ КЛАССАМИ. ЭТИ ДОСТИЖЕНИЯ СДЕЛАЛИ ОБРАЗОВАНИЕ БОЛЕЕ ГИБКИМ И ИНКЛЮЗИВНЫМ, ПОЗВОЛЯЯ СТУДЕНТАМ ИЗ РАЗЛИЧНЫХ СРЕД СМОТРЕТЬ КАЧЕСТВЕННОЕ ОБРАЗОВАНИЕ. ИНТЕРАКТИВНЫЕ ПЛАТФОРМЫ ДЛЯ ОБУЧЕНИЯ И ОБРАЗОВАТЕЛЬНЫЕ ПРИЛОЖЕНИЯ ДЕЛАЮТ ПРОЦЕСС ОБУЧЕНИЯ БОЛЕЕ ЗАНИМАТЕЛЬНЫМ И ЭФФЕКТИВНЫМ.

В ДЕЛОВОМ МИРЕ ТЕХНОЛОГИЯ ИЗМЕНИЛА СПОСОБЫ ФУНКЦИОНИРОВАНИЯ И КОНКУРЕНЦИИ КОМПАНИЙ. ПЛАТФОРМЫ ЭЛЕКТРОННОЙ ТОРГОВЛИ ОТКРЫЛИ НОВЫЕ РЫНКИ, ПОЗВОЛИВ МАЛЫМ БИЗНЕСАМ ДОСТИГАТЬ КЛИЕНТОВ ГЛОБАЛЬНО. АВТОМАТИЗАЦИЯ И ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ ОПТИМИЗИРОВАЛИ БИЗНЕС-ПРОЦЕССЫ, ПОВЫШАЯ ПРОДУКТИВНОСТЬ И СНИЖАЯ ЗАТРАТЫ. АНАЛИЗ БОЛЬШИХ ДАННЫХ ПОЗВОЛЯЕТ КОМПАНИЯМ ПРИНИМАТЬ БОЛЕЕ ОСМЫСЛЕННЫЕ РЕШЕНИЯ, ПРИСПОСАБЛИВАЯ СВОИ ПРОДУКТЫ И УСЛУГИ К ПОТРЕБНОСТЯМ КЛИЕНТОВ.

ТЕМ НЕМЕНЕЕ, ТЕХНОЛОГИЯ ТАКЖЕ ПРЕДСТАВЛЯЕТ ЗНАЧИТЕЛЬНЫЕ ВЫЗОВЫ. БЫСТРЫЙ ТЕМП ТЕХНОЛОГИЧЕСКИХ ИЗМЕНЕНИЙ МОЖЕТ ПРИВЕСТИ К СМЕЩЕНИЮ РАБОЧИХ МЕСТ, ПОСКОЛЬКУ АВТОМАТИЗАЦИЯ ЗАМЕНЯЕТ РАБОЧУЮ СИЛУ ЧЕЛОВЕКА. КИБЕРБЕЗОПАСНОСТЬ ЕЩЕ ОДНА ВАЖНАЯ ПРОБЛЕМА, ПОСКОЛЬКУ УВЕЛИЧИВАЮЩЕЕСЯ КОЛИЧЕСТВО ХРАНЯЩИХСЯ В СЕТИ ДАННЫХ ДЕЛАЕТ КОМПАНИИ И ЛИЦ НЕРАНИМЫМИ К КИБЕРАТАКАМ. ОБЕСПЕЧЕНИЕ КОНФИДЕНЦИАЛЬНОСТИ ДАННЫХ СТАЛО БОЛЕЕ СЛОЖНЫМ, ВОЗНИКАЮТ ЭТИЧЕСКИЕ ВОПРОСЫ О ИСПОЛЬЗОВАНИИ И РАСПРОСТРАНЕНИИ ИНФОРМАЦИИ.

ВЛИЯНИЕ ТЕХНОЛОГИИ НА ОКРУЖАЮЩУЮ СРЕДУ ТОЖЕ ЯВЛЯЕТСЯ КРИТИЧЕСКОЙ ПРОБЛЕМОЙ. НЕСМОТРЯ НА ТО, ЧТО ТЕХНОЛОГИЧЕСКИЕ ДОСТИЖЕНИЯ УЛУЧШИЛИ ЭНЕРГОЭФФЕКТИВНОСТЬ, ОНИ ТАКЖЕ ПРИВЕЛИ К УВЕЛИЧЕНИЮ ПОТРЕБЛЕНИЯ И ОТХОДОВ. ЭЛЕКТРОННЫЕ ОТХОДЫ СТАНОВЯТСЯ РАСТУЩЕЙ ПРОБЛЕМОЙ, С МИЛЛИОНАМИ УСТРОЙСТВ, ВЫБРАСЫВАЕМЫХ КАЖДЫЙ ГОД. ПРОИЗВОДСТВО И УТИЛИЗАЦИЯ ЭТИХ УСТРОЙСТВ ОКАЗЫВАЮТ ЗНАЧИТЕЛЬНОЕ ВЛИЯНИЕ НА ОКРУЖАЮЩУЮ СРЕДУ.

СОЦИАЛЬНО, ТЕХНОЛОГИЯ ИЗМЕНИЛА СПОСОБ, КАК МЫ ВЗАИМОДЕЙСТВУЕМ ДРУГ С ДРУГОМ. СОЦИАЛЬНЫЕ МЕДИА ПЛАТФОРМЫ СВЯЗАЛИ ЛЮДЕЙ ПО ВСЕМУ МИРУ, НО ОНИ ТАКЖЕ ПРИСПОСОБИЛИСЬ К РАСПРОСТРАНЕНИЮ ДИСИНФОРМАЦИИ И УЩЕМЛЕНИЮ ПРАВ ЧАСТНОЙ ЖИЗНИ. ПОСТОЯННАЯ СВЯЗАННОСТЬ МОЖЕТ ПРИВОДИТЬ К УВЕЛИЧЕНИЮ СТРЕССА И УМЕНЬШЕНИЮ ЛИЦОМ К ЛИЦУ ВЗАИМОДЕЙСТВИЯ, ВЛИЯЯ НА МЕНТАЛЬНОЕ ЗДОРОВЬЕ.

НЕСМОТРЯ НА ЭТИ ВЫЗОВЫ, ПОТЕНЦИАЛ ТЕХНОЛОГИИ УЛУЧШИТЬ ЖИЗНЬ И РЕШИТЬ СЛОЖНЫЕ ПРОБЛЕМЫ ОГРОМЕН. ПРАВИТЕЛЬСТВА, КОМПАНИИ И ЛИЦА ДОЛЖНЫ РАБОТАТЬ ВМЕСТЕ, ЧТОБЫ ИСПОЛЬЗОВАТЬ ПРЕИМУЩЕСТВА ТЕХНОЛОГИИ, СОКРА"""
    keyword = "ЯВЛЯЕТСЯ"
    #keyword = keyword.upper()
    TEXT =  funcs.Text(normal_text, keyword)
    formats = TEXT.formatted()

    #print(TEXT.encrypt(formats))

    encrypted_text = TEXT.encrypt(formats)
    

    #performing Twist Algorithm

    TWIST = Twist(19, encrypted_text)

    enc_perc = TWIST.letter_percentages()

    twist_vals = TWIST.twist_values(enc_perc)

    key_len,dict_key_tiem_nang = TWIST.key_length(twist_vals, "twistplus")
    # print("dic_key_tiem_nang: ")
    # print(dict_key_tiem_nang)
    # print("################################################################")
    #key_len,dict_key_tiem_nang = TWIST.key_length(twist_vals, "twist")
    #Finding the shifts in the key used

    # KAKASHI = Kasiski(encrypted_text)
    # elem,filt = KAKASHI.repeats(10)
    # difference=KAKASHI.spacings(elem, filt)
    # len_kashi = KAKASHI.key_length(difference)
    # print("len kakashi  ",len_kashi)
    FREQ = Frequency(key_len)
    letters_tiem_nang_in_key = FREQ.likely_letters(encrypted_text)
    #print(letters)
    print("\n \n")
    so_luong_variant_in_one_place_of_key = 5
    top_letters = FREQ.shortened_letters(so_luong_variant_in_one_place_of_key, letters_tiem_nang_in_key)
    key_tiem_nang = ""
    for lt in top_letters:
        print(lt,top_letters[lt])
        key_tiem_nang+=top_letters[lt][0]
    print("These are the 5 most likely letters of the keyword in the 0 position, 1 position, etc.")
    decrypted_text=TEXT.decrypt(encrypted=encrypted_text,keyword=key_tiem_nang)
    print(decrypted_text)
