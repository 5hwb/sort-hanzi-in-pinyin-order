from bs4 import BeautifulSoup
import re
import argparse

##################################################
#          Pinyin sort order lists
##################################################
list_initials = \
["","b","p","f","m","d","t","n","l",
"g","k","h","j","q","x",
"zh","ch","sh","r","z","c","s",
"y","w"]

list_rimes = \
["", "a", "ā", "á", "ǎ", "à", "o", "ō", "ó", "ǒ", "ò", 
"e", "ē", "é", "ě", "è", "i", "ī", "í", "ǐ", "ì", 
"u", "ū", "ú", "ǔ", "ù", "ü", "ǖ", "ǘ", "ǚ", "ǜ", 
"ai", "āi", "ái", "ǎi", "ài", "ei", "ēi", "éi", "ěi", "èi",
"ui", "uī", "uí", "uǐ", "uì", "ao", "āo", "áo", "ǎo", "ào",
"ou", "ōu", "óu", "ǒu", "òu", "iu", "iū", "iú", "iǔ", "iù",
"ie", "iē", "ié", "iě", "iè", "ue", "uē", "ué", "uě", "uè",
"üe", "üē", "üé", "üě", "üè", "er", "ēr", "ér", "ěr", "èr",
"an", "ān", "án", "ǎn", "àn", "ang", "āng", "áng", "ǎng", "àng",
"en", "ēn", "én", "ěn", "èn", "eng", "ēng", "éng", "ěng", "èng",
"in", "īn", "ín", "ǐn", "ìn", "ing", "īng", "íng", "ǐng", "ìng",
"ong", "ōng", "óng", "ǒng", "òng", "un", "ūn", "ún", "ǔn", "ùn",
"ia", "iā", "iá", "iǎ", "ià", "iao", "iāo", "iáo", "iǎo", "iào",
"ian", "iān", "ián", "iǎn", "iàn", "iang", "iāng", "iáng", "iǎng", "iàng",
"iong", "iōng", "ióng", "iǒng", "iòng",
"ua", "uā", "uá", "uǎ", "uà", "uo", "uō", "uó", "uǒ", "uò",
"uai", "uāi", "uái", "uǎi", "uài", "uan", "uān", "uán", "uǎn", "uàn",
"uang", "uāng", "uáng", "uǎng", "uàng"]

##################################################
#      Functions to make sorting easier
##################################################

def create_dict_from_list(list_entries):
    '''
    Create a dictionary that maps entries in a list with their indices, which makes it faster to look up the contents of a list. 
    Example: list_entries is ["p", "b", "f", "v"]. The list index of the entry "p" is 0, "b" is 1, and so on. 
    '''
    dict = {}
    index = 0
    for value in list_entries:
        dict[value] = index
        index += 1
    return dict

def get_pinyin_tuple(syl):
    '''
    Given a Pinyin syllable string, convert it into a list tuple where the 1st number represents the initial and the 2nd number represents the rime.
    e.g. 'dang' -> (5, 86) where the initial 'd' -> 5 and the rime 'ang' -> 86, for example.
    This makes it easy to sort Pinyin syllables according to the traditional pinyin order (b, p, m, f, etc).
    Note: dict_initials and dict_rimes need to be created before running this function.
    '''
    pinyin_tuple = [-1, -1]
    
    # Get the index of initial 
    initial_len = 2
    while initial_len > 0:
        initial = syl[:initial_len]
        #print("initial_len={} initial={}".format(initial_len, initial))
        if initial in dict_initials:
            pinyin_tuple[0] = dict_initials[initial]
            #print("Initial found in dict! {}".format(pinyin_tuple[0]))
            break
        initial_len -= 1
    
    # Get the index of rime
    rime = syl[initial_len:]
    #print("rime={}".format(rime))
    if rime in dict_rimes:
        pinyin_tuple[1] = dict_rimes[rime]
        #print("Rime found in dict! {}".format(pinyin_tuple[1]))
    else:
        rime = 0
    
    return pinyin_tuple

#=============================
# Key functions for sorting
#=============================
def key_pinyin(content):
    '''
    Key function for sort function.
    Sort by pinyin pronunciation (3rd cell) in tuple form
    '''
    return get_pinyin_tuple(content[2])

def key_hanzi(content):
    '''
    Key function for sort function.
    Sort by hanzi (2nd cell)
    '''
    return content[1]

##################################################
# Parse a single argument (limit to n most frequent characters)
##################################################
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--limit", help="Limit output to n most frequent characters", type=int)
args = parser.parse_args()

##################################################
# Code
##################################################

#=============================
# Create dictionary to get the list index, given a value
#=============================
dict_initials = create_dict_from_list(list_initials)
dict_rimes = create_dict_from_list(list_rimes)

#=============================
# Read HTML file and show contents
#=============================
with open("The most common Chinese characters (Unicode).html", "r+") as file:
    html_doc = file.read()           # reads a string from a file

soup = BeautifulSoup(html_doc, 'html.parser')
#print(soup.prettify())

intended_content = []

#=============================
# Go thru the table data
#=============================
row_num = 0
find_all_tr = soup.body.blockquote.table.tbody.find_all('tr')

# Get the limit from args, if provided
limit = len(find_all_tr)
if (args.limit != None and args.limit + 1 < len(find_all_tr)):
    limit = args.limit + 1

# Go thru each table row
for tr_content in find_all_tr[:limit]:
    
    # Skip 1st row - not useful info
    if (row_num == 0):
        row_num += 1
        continue
    
    row_tuple = []
    #print("===== ROW {} CONTENTS: =====".format(row_num))
    
    # Go thru each cell in the row
    cell_num = 0
    for td_content in tr_content.find_all('td'):
        # Go thru each sub-tag in the cell, and create a string out of their contents
        
        td_subcontent = td_content.contents
        td_subcontent_string = ""
        for subcontent in td_subcontent:
            td_subcontent_string += subcontent.string
        
        # Process the 'Character' string - get only the simplified form
        if (cell_num == 1):
            td_subcontent_string = td_subcontent_string[:1]
        
        # Process the 'Pronunciations and explanations' string - get only the main pinyin reading
        if (cell_num == 2):
            td_subcontent_string = re.findall("\[(.+?)\]", td_subcontent_string)[0].lower()
        
        row_tuple.append(td_subcontent_string)
        cell_num += 1
    
    intended_content.append(row_tuple)
    row_num += 1

#=============================
# Sort by pinyin reading and print output
#=============================
intended_content = sorted(intended_content, key=key_pinyin)

for aa in intended_content:
    #print("===== CONTENTS ({}): =====".format(len(aa)))
    print("{} {} ({})".format(aa[2], aa[1], aa[0]))
