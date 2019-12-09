from bs4 import BeautifulSoup

# Read HTML file and show contents
with open("someFairyTale.html", "r+") as file:
    html_doc = file.read()           # reads a string from a file

soup = BeautifulSoup(html_doc, 'html.parser')
#print(soup.prettify())

for aa in soup.find_all('a'):
    print(aa.contents)
    

