from bs4 import BeautifulSoup
import re

# Pinyin sort order

pinyin_initials = \
["","b","p","f","m","d","t","n","l",
"g","k","h","j","q","x",
"zh","ch","sh","r","z","c","s",
"y","w"]

pinyin_rimes = \
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

def create_dict_from_list(list_values):
    '''
    Create a dictionary that maps the list values with their indices. 
    '''
    dict = {}
    index = 0
    for value in list_values:
        dict[value] = index
        index += 1
    return dict

def get_pinyin_tuple(syl):
    #TODO Check first 2 chars
    pass    

# TODO: parse a Pinyin syllable and convert it into a tuple of numbers.
# e.g. 'you' = [3, 65] where y = 3 and ou = 65.

# Read HTML file and show contents
with open("The most common Chinese characters (Unicode).html", "r+") as file:
    html_doc = file.read()           # reads a string from a file

soup = BeautifulSoup(html_doc, 'html.parser')
#print(soup.prettify())

intended_content = []

# Go thru each table row (limit to 10 for now)
row_num = 0
for tr_content in soup.body.blockquote.table.tbody.find_all('tr'):
    
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
        
        # Process the hanzi string - get only the simplified form
        if (cell_num == 1):
            td_subcontent_string = td_subcontent_string[:1]
        
        # Process the 'Pronunciations' string - get only the main pinyin reading
        if (cell_num == 2):
            td_subcontent_string = re.findall("\[(.+?)\]", td_subcontent_string)[0].lower()
        
        row_tuple.append(td_subcontent_string)
        cell_num += 1
    
    intended_content.append(row_tuple)
    row_num += 1


# Sort by pinyin reading
intended_content = sorted(intended_content, key=lambda row: row[2])

for aa in intended_content:
    #print("===== CONTENTS ({}): =====".format(len(aa)))
    print("{} {} ({})".format(aa[2], aa[1], aa[0]))
