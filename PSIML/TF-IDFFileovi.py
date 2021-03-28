from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import string
import glob
import math
import sys


def tfk(files):
    stem = dict()
    for path in files:
        with open(path, "r", encoding="UTF8") as f:
            lines = f.readlines()
            stem_set = set()
            for line in lines:
                terms = word_tokenize(line)
                for term in terms:
                    # term = [s for s in term if s.isalnum()]
                    # str = ""
                    # term = str.join(term)
                    term = term.lower()
                    if ((not term.isalnum()) or term in words_to_remove):
                        continue
                    st = ss.stem(term)
                    if (st in words_to_remove):
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
        stem = dict()
        for line in lines:
            terms = word_tokenize(line)
            for term in terms:
                # term = [s for s in term if s.isalnum()]
                # str = ""
                # term = str.join(term)
                term = term.lower()
                if ((not term.isalnum()) or term in words_to_remove):
                    continue
                st = ss.stem(term)
                if (st in words_to_remove):
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
        if ((not term.isalnum()) or term in words_to_remove):
            continue
        st = ss.stem(term)
        if (st in words_to_remove):
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
        str = ""
        lines = str.join(lines)
        sentences = sent_tokenize(lines)
        ind = 0
        for sentence in sentences:
            all.append(SentenceScore(sentence, callScore(sentence), ind))
            ind += 1
    all.sort(key=lambda x: x.score, reverse=True)
    end = 10
    if (len(all) < 10):
        end = len(all)
    for i in range(0, end):
        res.append(all[i])
    # res.sort(key=lambda x: x.index)
    return res


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == "__main__":
    # words_to_remove = stopwords.words('english')
    words_to_remove = set(string.punctuation)
    sys.stdout.reconfigure(encoding='utf-8')
    ss = SnowballStemmer("english")
    path = "dataTF-IDF/public/corpus"
    if ("Before" in words_to_remove):
        print("da")
    else:
        print("ne")
    for ind in range(0, 10):
        print("Primer {}".format(ind))
        with open("dataTF-IDF/public/inputs/{}.in".format(ind), encoding="UTF8") as f:
            filepath = f.readlines()
            f.close()
            filepath = filepath[1][:-1]
            text_files = glob.glob(path + "/**/*.txt", recursive=True)
            dir1 = tfk(text_files)
            dir2 = tfc(filepath)
            l = []
            dir3 = dict()
            for stem in dir2.keys():
                dir3[stem] = dir2[stem] * math.log(len(text_files) / dir1[stem])
            l = sorted(dir3.items(), key=lambda x: (-x[1], x[0]))
            with open("dataTF-IDF/public/outputs/{}.out".format(ind), encoding="UTF8") as out:
                words = word_tokenize(out.readline())
                end = 10
                if (len(l) < 10):
                    end = len(l)
                for i in range(0, end):
                    # print(l[i][0], dir3[l[i][0]], dir2[l[i][0]], len(text_files), dir1[l[i][0]])
                    if (l[i][0] != words[i * 2]):
                        print(f"{bcolors.WARNING}GRESKAA{bcolors.ENDC}")
                    print(l[i][0], words[i * 2], l[i][0] == words[i * 2])
                text = out.readlines()
                str = ""
                text = str.join(text)
                sentences = sent_tokenize(text)
                l = summary(filepath)
                end = 10
                if (len(l) < 10):
                    end = len(l)
                for i in range(0, end):
                    # if (l[i].sentence != sentences[i]):
                    #     print(f"{bcolors.WARNING}GRESKAA{bcolors.ENDC}")
                    print(l[i].sentence, l[i].score)
                    # print(sentences[i])
                    # print(l[i].sentence == sentences[i])
                print("\n\n///////////////////////////////////////////////\n\n")
