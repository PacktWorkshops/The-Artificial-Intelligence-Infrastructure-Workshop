import spacy
nlp = spacy.load('en_core_web_lg')


def polarity_good_vs_bad(word):
    """Returns a positive number if a word is closer to good than it is to bad, or a negative number if vice versa
    IN: word (str): the word to compare
    OUT: diff (float): positive if the word is closer to good, otherwise negative
    """

    good = nlp("good")
    bad = nlp("bad")
    word = nlp(word)
    if word and word.vector_norm:
        sim_good = word.similarity(good)
        sim_bad = word.similarity(bad)
        diff = sim_good - sim_bad
        diff = round(diff * 100, 2)
        return diff
    else:
        return None


def test_polarity_good_vs_bad():
    # Test that good is close to good (positive), bad is close to bad (negative), and out of vocabulary words return None
    assert polarity_good_vs_bad("good") > 0
    assert polarity_good_vs_bad("bad") < 0
    assert polarity_good_vs_bad("asdfaasdfasdfasdf") == None


