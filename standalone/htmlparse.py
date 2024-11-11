# Enter your code here. Read input from STDIN. Print output to STDOUT
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start :", tag)

        for attr in attrs:
            print(f"-> {attr[0]} > {attr[1]}")
    def handle_endtag(self, tag):
        print("End   :", tag)
    def handle_startendtag(self, tag, attrs):
        print("Empty :", tag)

parser = MyHTMLParser()

html = ""
lines = int(input().strip())

for i in range(lines):
    html += input().strip()

parser.feed(html)

