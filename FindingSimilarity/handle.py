import re
from googlesearch import search
from stop_words import get_stop_words
from bs4 import BeautifulSoup, Comment
import urllib.request
import urllib.error


def get_text_without_stop_words(text):
    stopwords = get_stop_words('en')
    querywords = text.split()

    resultwords = [word for word in querywords if word.lower()
                   not in stopwords]
    result = ' '.join(resultwords)

    return result


class FindingSimilarity():
    def __init__(self, query):
        self.query = query
        self.urls_details = []

    def get_urls_text(self):
        for url in search(self.query, stop=5):
            url_details = {
                'url': url,
                'data': get_page_data(self.query, url),
            }
            self.urls_details.append(url_details)

    def get_results(self):
        self.get_urls_text()
        return self.urls_details


def get_html(url):
    req = urllib.request.Request(
        url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req)
    page = BeautifulSoup(html, features="html.parser")
    # remove comment in HTML
    comments = page.findAll(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    return page


def is_visible(element):  # check that whether the html page is visible or not
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


def get_page_text(url):
    page_html = get_html(url)
    page_html = page_html.findAll(text=True)
    result = filter(is_visible, page_html)
    return ' '.join(list(result))


def get_page_data(query, url):
    try:
        html = get_html(url)
        html_page = ','.join(str(v) for v in html.find('body').findChildren())
        html = html.findAll(text=True)
    except urllib.error.HTTPError as e:
        print(e.__dict__)
        return
    except urllib.error.URLError as e:
        print(e.__dict__)
        return

    result = filter(is_visible, html)
    text = ''.join(list(result))

    jaccard = compare(query, text)

    similarity = jaccard['similarity']
    sentences = jaccard['sentences']

    return {'html': html, 'html_page': html_page, 'text': text, 'sentences': sentences, 'similarity': similarity}


def jaccard_similarity(sentence1, sentence2):
    sentence1 = get_text_without_stop_words(sentence1).lower()
    sentence2 = get_text_without_stop_words(sentence2).lower()
    a = set(sentence1.split())
    b = set(sentence2.split())
    c = a.intersection(b)
    # prevent divide by zero
    deno = len(a) + len(b) - len(c)
    similarity = deno and (len(c) / (len(a) + len(b) - len(c))) or 0

    return similarity


def compare(query, document):
    a = query.split(".")
    b = document.split(".")
    c = []
    similarity = 0
    for i in range(len(a)):
        for j in range(len(b)):
            if (jaccard_similarity(a[i], b[j]) > 0.5):
                similarity += jaccard_similarity(a[i], b[j])
                c.append(b[j])

    similarity = len(c) and similarity * 100 / len(c) or 0

    return {'similarity': similarity, 'sentences': c}
