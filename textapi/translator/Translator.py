import codecs
import random
import numpy as np

from translator.KeyPhraseExtractor import KeyPharaseExtractor
from translator.Preprocess import Preprocess
from translator.GoogleExtractor import GoogleExtractor
from translator.SentenceCreater import SentenceCreater

class Translator:
    def __init__(self,):
        self.key_extractor = KeyPharaseExtractor()
        self.google_extractor =  GoogleExtractor()
        self.preprocess = Preprocess()
        self.creater =  SentenceCreater()

    def translate(self, post, type='default'):
        post = self.preprocess.exec(post)
        google_phrase = self.google_extractor.get_phrase(post)
        sentence_dic = self.creater.create(google_phrase, type)
        key_phrase = self.key_extractor.get_phrase(post)
        sentence_dic.update(self.creater.create(key_phrase, type))

        return self.choiceOne(sentence_dic)
    
    def choiceOne(self, sentence_dic):
        """
        magnitudeのスコアを重みとして，ランダムに選択する
        すべてのスコアが0のときはランダムに1つ選択する
        """
        d = [(v, v.magnitude_score) for k, v in sentence_dic.items()]
        a, w = zip(*d)
        if sum(w) == 0:
            print(w)
            return random.choice(a)
        else:
            w2 = np.array(w) / sum(w)
            v = np.random.choice(a, p=w2)
            return v
        
    ###
    # For Test
    ###
    def translate_with_candidates(self, post, type):
        post = self.preprocess.exec(post)
        google_phrase = self.google_extractor.get_phrase(post)
        sentence_dic = self.creater.create(google_phrase, type)
        key_phrase = self.key_extractor.get_phrase(post)
        sentence_dic.update(self.creater.create(key_phrase, type))
    
        return self.choiceOne(sentence_dic), sentence_dic


    def translate_file(self, filename, output, sep="\n"):
        with codecs.open(filename, "r", "utf-8") as f:
            posts = f.read().rstrip(sep).split(sep)
        o = codecs.open(output, "w", "utf-8")

        for i, post in enumerate(posts[5:30], start=5):
            print(i)
            result_dic, candidates = self.translate_with_candidates(post, "jk")
            # テキスト出力
            output = ""
            output += "sentence_id: {}\n".format(i)
            output += "--sentence--\n{}------------\n".format(post)
            output += "--choiced--\n"
            output += "{}\n".format(result_dic)
            output += "--candidates--\n"
            for k, v in candidates.items():
                output += "method:{}:{}\n".format(k, v)
            o.write(output + "==========\n\n")

if __name__ == '__main__':
    t = Translator()
    t.translate("今日の天気は晴れです．")
    #t.translate_file("data/sample.txt", sep="<split>\n")