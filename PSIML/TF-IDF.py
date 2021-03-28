from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import string
import glob
import math

import sys


def tfk(files):
    stem = dict()
    for path in files:
        with open(path, "r", encoding="UTF8") as f:
            lines = f.readlines()
            f.close()
            stem_set = set()
            for line in lines:
                terms = word_tokenize(line)
                for term in terms:
                    # term = [s for s in term if s.isalnum()]
                    # str = ""
                    # term = str.join(term)
                    term = term.lower()
                    if ((not term.isalnum()) or term in not_term):
                        continue
                    st = ss.stem(term)
                    if (st in not_term):
                        continue
                    stem_set.add(st)
            for st in stem_set:
                if (st in stem.keys()):
                    stem[st] += 1
                else:
                    stem[st] = 1
    # for key in stem.keys():
    #     print(key, " : {}\n".format(stem[key]))
    return stem


def tfc(path):
    with open(path, "r", encoding="UTF8") as f:
        lines = f.readlines()
        f.close()
        stem = dict()
        for line in lines:
            terms = word_tokenize(line)
            for term in terms:
                # term = [s for s in term if s.isalnum()]
                # str = ""
                # term = str.join(term)
                term = term.lower()
                if ((not term.isalnum()) or term in not_term):
                    continue
                st = ss.stem(term)
                if (st in not_term):
                    continue
                if (st in stem.keys()):
                    stem[st] += 1
                else:
                    stem[st] = 1
    return stem


class SentenceScore:
    def __init__(self, sentence, score, index):
        self.sentence = sentence
        self.score = score
        self.index = index


def callScore(sentence):
    score = 0
    words = word_tokenize(sentence)
    stem_list = []
    for term in words:
        term = term.lower()
        if ((not term.isalnum()) or term in not_term):
            continue
        st = ss.stem(term)
        if (st in not_term):
            continue
        stem_list.append([st, dir3[st]])
    stem_list = sorted(stem_list, key=lambda x: (-x[1], x[0]))
    end = 10
    if (len(stem_list) < 10):
        end = len(stem_list)
    stem_list = stem_list[:end]
    for val in stem_list:
        score += val[1]
    return score


def summary(path):
    res = []
    all = []
    with open(path, "r", encoding="UTF8") as f:
        lines = f.readlines()
        f.close()
        str = ""
        lines = str.join(lines)
        sentences = sent_tokenize(lines)
        ind = 0
        for sentence in sentences:
            all.append(SentenceScore(sentence, callScore(sentence), ind))
            ind += 1
    all.sort(key=lambda x: x.score, reverse=True)
    end = 5
    if (len(all) < 5):
        end = len(all)
    for i in range(0, end):
        res.append(all[i])
    res.sort(key=lambda x: x.index)
    return res


if __name__ == "__main__":
    # words_to_remove = stopwords.words('english')
    not_term = set(string.punctuation)
    sys.stdout.reconfigure(encoding='utf-8')
    ss = SnowballStemmer("english")
    path = input()
    filepath = input()
    text_files = glob.glob(path + "/**/*.txt", recursive=True)
    dir1 = tfk(text_files)
    dir2 = tfc(filepath)
    l = []
    dir3 = dict()
    for stem in dir2.keys():
        dir3[stem] = dir2[stem] * math.log(len(text_files) / dir1[stem])
    l = sorted(dir3.items(), key=lambda x: (-x[1], x[0]))
    end = 10
    if (len(l) < 10):
        end = len(l)
    for i in range(0, end - 1):
        print(l[i][0],dir2[l[i][0]],dir1[l[i][0]],dir3[l[i][0]], end=", ")
    print(l[end - 1][0])
    l = summary(filepath)
    end = 5
    if (len(l) < 5):
        end = len(l)
    str = ""
    for i in range(0, end - 1):
        str += l[i].sentence
        str += " "
    str += l[end - 1].sentence
    print(str, end="")
