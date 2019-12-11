# Web scraping experiment - sort most frequent Chinese characters in pinyin order

This is a Python script to extract the list of the 2715 most common Chinese characters (hanzi) from [this site](http://zein.se/patrick/3000char.html) and convert it into a Python list of tuples for further processing, allowing it to be sorted in a different manner (such as by Pinyin reading). It uses the BeautifulSoup library to extract data from the HTML page.

The website's data is contained in a HTML table with this format:

| Number | Character | Pronunciations and explanations |
| --- | --- | --- |
| 1 | 的 | [de] <grammatical particle marking genitive... |
| 2 | 一(A壹) | [yī] one, a little; 第一 dì-yī first, primary... |
| 3 | 是	 | [shì] to be, 是不是? shìbushì? is (it) or is... |
| ... | ... | ... |

The Python script converts the data into the following format internally, extracting only simplified characters and the main pinyin pronunciation:

```
[
    ["1", "的", "de"],
    ["2", "一", "yī"],
    ["3", "是", "shì"],
    ...
]
```

This makes it easy to sort the entries in pinyin order (b, p, m, f, d, t, n, l etc):

```
de 的 (1)
shì 是 (3)
yī 一 (2)
``` 

## Output files

The outputs of the script can be found in _result.txt_, which is the full output of 2715 most common Chinese characters; and _result_100.txt_, _result_250.txt_, _result_500.txt_, and _result_1000.txt_, which contain the 100, 250, 500 and 1000 most common characters respectively, arranged in pinyin order.

### Generating output files (Unix)

Open a terminal and execute the following commands:

```
python3 get_info_from_html.py > result.txt
python3 get_info_from_html.py -l 100 > result_100.txt
python3 get_info_from_html.py -l 250 > result_250.txt
python3 get_info_from_html.py -l 500 > result_500.txt
python3 get_info_from_html.py -l 1000 > result_1000.txt
```

## Note

The script reads a HTML file called 'The most common Chinese characters (Unicode).html', which is not included in this repository. The file can be saved from http://zein.se/patrick/3000char.html and needs to be converted to UTF-8 before the script will work.
