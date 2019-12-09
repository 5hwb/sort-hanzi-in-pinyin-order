from bs4 import BeautifulSoup
import re

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
            td_subcontent_string = re.findall("\[(.+?)\]", td_subcontent_string)[0]
        
        row_tuple.append(td_subcontent_string)
        cell_num += 1
    
    intended_content.append(row_tuple)
    row_num += 1

for aa in intended_content:
    #print("===== CONTENTS ({}): =====".format(len(aa)))
    print("{} {} ({})".format(aa[2], aa[1], aa[0]))
