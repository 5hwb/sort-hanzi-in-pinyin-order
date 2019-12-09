from bs4 import BeautifulSoup

# Read HTML file and show contents
with open("The most common Chinese characters (Unicode).html", "r+") as file:
    html_doc = file.read()           # reads a string from a file

soup = BeautifulSoup(html_doc, 'html.parser')
#print(soup.prettify())

# Go thru each table row (limit to 10 for now)
for tr_content in soup.body.blockquote.table.tbody.find_all('tr')[:10]:
    print("===== CONTENTS: =====")
    # Go thru each cell in the row
    for td_content in tr_content.find_all('td'):
        # Go thru each sub-tag in the cell, and create a string out of their contents
        td_subcontent = td_content.contents
        td_subcontent_string = ";;;;;"
        for subcontent in td_subcontent:
            td_subcontent_string += subcontent.string
        td_subcontent_string += ",,,,,"
        print(td_subcontent_string)
