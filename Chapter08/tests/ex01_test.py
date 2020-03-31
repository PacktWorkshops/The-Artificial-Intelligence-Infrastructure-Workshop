import requests
import string
from collections import Counter

class Scraper:

    def fetch_news(self, urls):
        article_contents = []
        for url in urls:
            try:
                contents = requests.get(url).text
                article_contents.append(contents)
            except Exception as e:
                print(e)
        return article_contents

def is_clean(word):
    blacklist = {"var", "img", "e", "void"}
    if not word:
        return False
    if word in blacklist:
        return False
    for i, letter in enumerate(word):
        if i > 0 and letter in string.ascii_uppercase:
            return False
        if letter not in string.ascii_letters:
            return False
    return True

class Cleaner:

    def clean_articles(self, articles):
        clean_articles = []

        for article in articles:
            clean_words = []
            try:
                for word in article.split(" "):
                    if is_clean(word):
                        clean_words.append(word)
            except Exception as e:
                print(e)
            clean_articles.append(' '.join(clean_words))
        return clean_articles


class Deduplicator:

    def deduplicate_articles(self, articles):
        seen_articles = set()
        deduplicated_articles = []
        for article in articles:
            if hash(article) in seen_articles:
                continue
            else:
                seen_articles.add(hash(article))
                deduplicated_articles.append(article)

        return deduplicated_articles


class Analyzer:
    good_words = {"unveiled", "available", "faster", "stable"}
    bad_words = {"sued", "defiance", "violation"}

    def extract_entities_and_sentiment(self, articles):
        entity_score_pairs = []
        for article in articles:
            score = 0
            entities = []
            for word in article.split(" "):
                if word[0] == word[0].upper():
                    entities.append(word)
                if word.lower() in self.good_words:
                    score += 1
                elif word.lower() in self.bad_words:
                    score -= 1
            main_entities = [i[0] for i in Counter(entities).most_common(2)]
            entity_score_pair = (main_entities, score)
            entity_score_pairs.append(entity_score_pair)
        return entity_score_pairs

class DecisionMaker:
    target_companies = set(['Apple', 'Uber', 'Google'])

    def make_decisions(self, entity_score_pairs):
        decisions = []
        for entities, score in entity_score_pairs:
            for entity in entities:
                if entity in self.target_companies:
                    quantity = abs(score)
                    order = "Buy" if score > 0 else "Sell"
                    decision = (order, quantity, entity)
                    decisions.append(decision)
        return decisions

def test_scraper():
    scraper = Scraper()
    assert scraper.fetch_news(["https://asdfsdfsfsdkklzhfgarefsdfsfasdfasdf2232323f.com"]) == []
    assert len(scraper.fetch_news(["https://google.com", "https://amazon.com"])) == 2

def test_is_clean():
    print(is_clean(""))
    assert not is_clean("")
    assert not is_clean("{}34")
    assert not is_clean("snakeCase")
    assert is_clean("word")


def test_cleaner():
    cleaner = Cleaner()
    article = "this is anArticle test"
    assert cleaner.clean_articles([article])[0] == "this is test"


def test_dedup():
    dedup = Deduplicator()
    articles = ["one", "one", "two"]
    assert dedup.deduplicate_articles(articles) == ["one", "two"]

def test_analzer():
    analyzer = Analyzer()
    articles = ["Uber unveiled self driving car"]

    assert analyzer.extract_entities_and_sentiment(articles) == [(['Uber'], 1)]


