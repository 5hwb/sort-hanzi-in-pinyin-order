# Web scraping experiment

This is a Python script to extract the list of the 2715 most common Chinese characters from [this site](http://zein.se/patrick/3000char.html) and convert it into a Python list of tuples for further processing, allowing it to be sorted in a different manner (such as by Pinyin reading). It uses the BeautifulSoup library to extract data from the HTML page.

The website's data is contained in a HTML table with this format:

| Number | Character | Pronunciations and explanations |
| --- | --- | --- |
| 1 | 的 | [de] <grammatical particle marking genitive... |
| 2 | 一(A壹) | [yī] one, a little; 第一 dì-yī first, primary... |
| 3 | 是	 | [shì] to be, 是不是? shìbushì? is (it) or is... |
| ... | ... | ... |

The Python script converts the data into the following format, extracting only simplified characters and the main pinyin pronunciation:

```
[
    ["1", "的", "de"],
    ["2", "一", "yī"],
    ["3", "是", "shì"],
    ...
]
```

In this format, it is easy to sort 

## Note

The script reads a HTML file called 'The most common Chinese characters (Unicode).html', which is not included in this repository. The file can be saved from http://zein.se/patrick/3000char.html and needs to be converted to UTF-8 before the script will work.
