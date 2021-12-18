import re
from stop_words import get_stop_words
import urllib.request
from bs4 import BeautifulSoup, Comment
from googlesearch import search as google_search
import urllib.error


class PlagiarismChecker():
    stopwords = get_stop_words('en')

    def __init__(self, query, language):
        self.query = query
        self.language = language
        self.urls_details = []

    def get_google_urls(self):
        urls = google_search(self.query, stop=5)  # max_results
        return urls

    def get_urls_text(self):
        for url in self.get_google_urls():
            url_details = {
                'url': url,
                'data': get_page_data(self.query, url),
            }
            self.urls_details.append(url_details)

    def get_plagiat_results(self):
        self.get_urls_text()
        return self.urls_details


def get_page_soup(url):
    if url.endswith(".pdf"):
        return Exception("La  page demandée est  en pdf")
    else:
        req = urllib.request.Request(
            url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req)
        soup = BeautifulSoup(html, features="html.parser")

        # Remove comments in html   <!-- comment content  -->
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        return soup


def get_page_text(url):
    page_html = get_page_soup(url)
    page_html = page_html.findAll(text=True)
    result = filter(visible, page_html)
    return ' '.join(list(result))


def get_page_data(query, url):
    if url.endswith('.pdf'):
        return

    try:
        html = get_page_soup(url)
        html_page = ','.join(str(v) for v in html.find('body').findChildren())
        html = html.findAll(text=True)
    except urllib.error.HTTPError as e:
        print(e.__dict__)
        return
    except urllib.error.URLError as e:
        print(e.__dict__)
        return

    result = filter(visible, html)
    text = ''.join(list(result))

    #text_keywords = text.lower()
    #query = query.lower()

    jaccard_sim = compare(query, text)

    similarity = jaccard_sim['similarity']
    intersection_keywords = jaccard_sim['keywords']
    print(intersection_keywords)

    return {'html': html, 'html_page': html_page, 'text': text, 'keywords': intersection_keywords, 'similarity': similarity}


def get_jaccard_similarity(sentence1, sentence2):
    # You have to do this before calling this method :
    # query = get_text_without_stop_words(query).lower()
    # document = get_text_without_stop_words(document).lower()
    sentence1 = get_text_without_stop_words(sentence1).lower()
    sentence2 = get_text_without_stop_words(sentence2).lower()
    a = set(sentence1.split())
    b = set(sentence2.split())
    c = a.intersection(b)
    # for i in range(len(a)):
    #     for j in range(len(b)):
    #         if (a[i] == b[j]):
    #             c.append(a[i])
    # Document similarity to Query
    #similarity = round((float(len(c)) / (len(a) + len(b) - len(c))), 2)
    #sim2 = round((1 - similarity), 2) * 100

    # jaccard distance ~ similarity
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
            if (get_jaccard_similarity(a[i], b[j]) > 0.5):
                similarity += get_jaccard_similarity(a[i], b[j])
                c.append(b[j])

    similarity = len(c) and similarity * 100 / len(c) or 0

    return {'similarity': similarity, 'keywords': c}


# def get_cosine(vec1, vec2):
#     intersection = set(vec1.keys()) & set(vec2.keys())
#     numerator = sum([vec1[x] * vec2[x] for x in intersection])

#     print(intersection)

#     sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
#     sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
#     denominator = math.sqrt(sum1) * math.sqrt(sum2)

#     print(numerator)
#     print(denominator)

#     if not denominator:
#         return 0.0
#     else:
#         return float(numerator) / denominator


# WORD = re.compile(r'\w+')


# def text_to_vector(text):
#     words = WORD.findall(text)
#     return Counter(words)


# def get_cosine_similarity(query, document):
#     query = get_text_without_stop_words(query)
#     document = get_text_without_stop_words(document)

#     vector1 = text_to_vector(query)
#     vector2 = text_to_vector(document)

#     cosine = get_cosine(vector1, vector2)

#     print('Cosine:' + str(cosine))
#     return cosine


def get_text_without_stop_words(text):
    stopwords = get_stop_words('en')
    querywords = text.split()

    resultwords = [word for word in querywords if word.lower()
                   not in stopwords]
    result = ' '.join(resultwords)

    return result


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

#
# print (list(result))
