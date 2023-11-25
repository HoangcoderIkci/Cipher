key = "whatisthecode"

#This part of the code is taking out and spaces, upper case letters or punctuation in the text
text = "thiscardoftensymbolizesacrisisthatcannotbeavoidedaprofoundchangethatneedstobeconfrontedandaccepteditevokestheideaofateacheratherapistoraguidebutinacrisisthereisanequalpossibilitythatthehermitwillrenewhimselfordiehethereforealsoreferstopovertysolitudeandevendecayanddegenerationhecanbeseenasavagrantorevenanalcoholicwhoishidingaquartofredwineinhislantern"
alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
edit = ""
for i in text:
    if i in alphabet:
            edit = edit+i
print(edit)
len(edit)
#This part of the code is encrypting the Text with the key
print(" encrypt")
s1 = (len(edit)//len(key))*key + key[:(len(edit)-(len(edit)//len(key)*len(key)))]
print(s1)
encrypted = ""
for i in range(0,len(edit)):
    j = edit[i]
    k = s1[i]
    number = alphabet.index(j) + alphabet.index(k)
    encrypted = encrypted + alphabet[number % 26]
print(encrypted)



#Twist Algorithm for Keyword Length

#key lengths range 0 to 20
key_length_upper_limit = 20
all_key_lengths = {}
for m in range(1,key_length_upper_limit+1):
    nth_letter_2 = {}
    for i in range(0,m):
        nth_letter_2[i] = encrypted[i::m]
    all_key_lengths[m] = nth_letter_2
#print(all_key_lengths)

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
#print(all_key_frequencies)

all_key_letters = {}
for length in all_key_frequencies:
    sub_dict = {}
    for num in all_key_frequencies[length]:
        letters_in = []
        for letter in all_key_frequencies[length][num]:
            letters_in.append(letter[0])
        sub_dict[num]=letters_in
    all_key_letters[length]=sub_dict
    
#print(all_key_letters)

all_key_frequencies_complete = all_key_frequencies
for j in alphabet:
    for index in all_key_letters:
        for i in all_key_letters[index]:
            if j not in all_key_letters[index][i]:
                all_key_frequencies_complete[index][i][j]=0
                
#print(all_key_frequencies_complete)


all_key_frequencies_complete_sorted = {}
for index in all_key_frequencies_complete:
    sub_dict = {}
    for i in all_key_frequencies_complete[index]:
        sub_dict[i] = (sorted(all_key_frequencies_complete[index][i].items(),key=lambda letters: letters[1], reverse=True))
    all_key_frequencies_complete_sorted[index] = sub_dict

#print(all_key_frequencies_complete_sorted)

all_key_percentages = {}
for i in all_key_frequencies_complete_sorted:
    sub_dict = {}
    for j in all_key_frequencies_complete_sorted[i]:
        percentage_list_2 = []
        if (j-1)<=(len(edit)%i):
            divisor = (len(edit)//i)+1
        else:
            divisor = len(edit)//i
        
        for k in all_key_frequencies_complete_sorted[i][j]:
            tuple_new = (k[0],k[1]/divisor)
            percentage_list_2.append(tuple_new)
        sub_dict[j] = percentage_list_2
    all_key_percentages[i]=sub_dict

print(all_key_percentages)

Cj_dict = {}
for i in all_key_percentages:
    final_list = [0*l for l in range(0,26)]
    for j in all_key_percentages[i]:
        Cj_list = [k[1] for k in all_key_percentages[i][j]]
        final_list = [final_list[n]+Cj_list[n] for n in range(0,len(Cj_list))]
    Cj_dict[i]=final_list

#print(Cj_dict)

twists = {}
for i in Cj_dict:
    twist = 0
    for j in enumerate(Cj_dict[i]):
        if j[0]<=12:
            twist+=j[1]
        else:
            twist-=j[1]
    twist=twist*(100/i)
    twists[i]=twist

#Using the twist+ algorithm
twistplus = {}
twistlist = [x[1] for x in twists.items()]
for i in twistlist:
    subtract = 0
    for j in range(0,twistlist.index(i)):
        subtract+=(twistlist[j]/twistlist.index(i))
    number = i - subtract
    if twistlist.index(i)!=0:
        twistplus[twistlist.index(i)+1]=number

def twist_key(dict):
    mode_value = 0
    for i,j in dict.items():
        if j>mode_value:
            mode = i
            mode_value = j
    return mode

def twistplus_key(dict):
    modevalue = 0
    for i,j in dict.items():
        if j>modevalue:
            mode=i
            modevalue=j
    return mode

print("The twist+ algorithm Key Length is: %d" % twistplus_key(twistplus))
print("The twist algorithm Key Length is: %d" % twist_key(twists))


########################### KAKASHI ###########################

#Produce all repeated n letter segments
n = 3
elements = []
for i in range(0,len(encrypted)):
    if i<(len(encrypted)-n+1):
        j=0
        string = ""
        while j<n:
            string = string + encrypted[i+j]
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
print(filtered)

#Letter frequency analysis

#Guessing Key Length with Kasiski Algorithm
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

numbers = []
for i in range(0,len(filtered)):
    numbers.append(indexes(elements,list(filtered)[i]))

difference =[]
for i in numbers:
    for j in range(0,len(i)-1):
        difference.append(i[j+1]-i[j])
print("The different spaces between %s letter repeated segments are %s" % (n,difference))

#Factorizing Algorithm
def factorize2(number):
    while number>1:
        for i in range(2,number+1):
            if number%i==0:
                number = int(number/i)
                yield i
                break

kas_factors={}
for i in range(2,len(encrypted)):
    counts=0
    for d in difference:
        if d%i==0:
            counts+=1
    if counts!=0:
        kas_factors[i]=counts

kas_mode = 0
for i in kas_factors:
    x = kas_factors[i]
    if x>=kas_mode:
        kas_mode=i
print("The Kasiski Algorithm key length is %s" % kas_mode)
algorithm = "Twist+"
if algorithm=="Twist+":
    mode=twistplus_key(twistplus)
if algorithm=="Twist":
    mode=twist_key(twists)
if algorithm=="Kasiski":
    mode = kas_mode

nth_letter = {}
for i in range(0,mode):
    nth_letter[i] = encrypted[i::mode]

letter_frequencies = {}
for i,j in nth_letter.items():
    letter_counts = {}
    for letter in j:
        if letter not in letter_counts:
            letter_counts[letter]=0
        letter_counts[letter]+=1
    letter_frequencies[i]=letter_counts
    
print(letter_frequencies)


#More complex letter frequency approach
english_frequencies = {'a':8.4966,'b':2.0720,'c':4.5388,'d':3.3844,'e':11.1607,'f':1.8121,'g':2.4705,'h':3.0034,'i':7.5448,'j':0.1965,'k':1.1016,'l':5.4893,'m':3.0129,'n':6.6544,'o':7.1635,'p':3.1671,'q':0.1962,'r':7.5809,'s':5.7351,'t':6.9509,'u':3.6308,'v':1.0074,'w':1.2899,'x':0.2902,'y':1.7779,'z':0.2722}

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
for j in alphabet:
    for i in all_present_letters:
        if j not in all_present_letters[i]:
            position = alphabet.index(j)
            insert_element = (j,0)
            sorted_frequencies_alphabetical_complete[i].insert(position, insert_element)
            
sorted_frequencies_percentages = {}
for i in sorted_frequencies_alphabetical_complete:
    percentage_list = []
    if i<=(len(edit)%mode):
        divisor = (len(edit)//mode)+1
    else:
        divisor = len(edit)//mode
    for j in sorted_frequencies_alphabetical_complete[i]:
        new_tuple = (j[0],j[1]/divisor)
        percentage_list.append(new_tuple)
    sorted_frequencies_percentages[i]=percentage_list

print(sorted_frequencies_percentages)


#Plotting the frequencies
import matplotlib.pyplot as plt

data_percentages = [x[1] for x in sorted_frequencies_percentages[1]]
print(data_percentages)
english_data = [j/100 for i,j in english_frequencies.items()]
print(english_data)

plt.figure(figsize=(10,3))
plt.plot(alphabet, data_percentages, label='Key 6th Letter Frequencies')
plt.plot(alphabet, english_data, label='English Frequencies')
plt.legend()
plt.title('Key Letter Frequencies against English Letter Frequencies')
plt.xlabel(r'Letters')
plt.ylabel(r'Percentages')
plt.show()


#Chi-Squared Test
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
        letter_pair = alphabet[(n.index(sublist))]   #error here, need to get the right index
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

print(statistical_sorted)

for i in range(0,len(statistical_sorted)):
    print("Key Character %s" % i)
    for number in range(0,3):
        print(statistical_sorted[i][number])
        
        
dictoflists ={0:['a','b','c','d','e','f'],1:['g','h','i','j','k','l'],2:['m','n','o','p','q','r']}
statistical_sorted_shortened = {}
for i in range(0,len(statistical_sorted)):
    sublist = []
    for j in range(0,3):
        sublist.append(statistical_sorted[i][j][0])
    statistical_sorted_shortened[i]=sublist

#My combinations function
potential_keys =[]
def combine_test(dictionary,string_in,n):
    for i in range(0,len(dictionary[n])):
        string_out = string_in + dictionary[n][i]
        if n==len(dictionary)-1:
            potential_keys.append(string_out)
        else:
            n+=1
            combine_test(dictionary, string_out,n)
            n-=1
            
#Other Combination Function
def combine(pre, n, m):
    
    result = []
    if len(pre) == n-1:
        for i in range(m):
            result.append(pre + dictoflists[len(pre)][i])
        return result
    for i in range(m):
        result.extend(combine(pre + dictoflists[len(pre)][i], n, m))
    return result
#print(combine("", 6, 5))

combine_test(statistical_sorted_shortened,'',0)
print(len(potential_keys))

decrypted = ""
key = potential_keys[0]

key_matching_string = (len(encrypted)//len(key))*key + key[:(len(encrypted)-(len(encrypted)//len(key)*len(key)))]

for i in range(0,len(encrypted)):
    j = encrypted[i]
    k=key_matching_string[i]
    number = alphabet.index(j) - alphabet.index(k)
    decrypted = decrypted + alphabet[number % 26]
    
print("\nThe text is:\n%s" % decrypted)

print("\n \nThe Key is: %s \n \n" % potential_keys[0])

print("The most likely key characters are: \n")
for i in range(0,len(statistical_sorted)):
    print("Letter %s" % i)
    for number in range(0,3):
        print(statistical_sorted[i][number][0])