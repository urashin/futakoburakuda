import codecs
import random

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
        ランダムで１つ返す
        """
        return random.choice([v for k, v in sentence_dic.items()])

    def translate_file(self, filename="", sep="\n"):
        with codecs.open(filename, "r", "utf-8") as f:
            posts = f.read().rstrip(sep).split(sep)
        o = codecs.open("result/summarize.txt", "w", "utf-8")

        for i, post in enumerate(posts, start=0):
            print(i)
            result_dic = self.translate(post)
            # テキスト出力
            output = ""
            output += "sentence_id: {}\n".format(i)
            output += "--sentence--\n{}------------\n".format(post)
            output += "summarize\n"
            output += "{}\n".format(result_dic)
            o.write(output + "==========\n\n")

if __name__ == '__main__':
    t = Translator()
    t.translate("今日の天気は晴れです．")
    #t.translate_file("data/sample.txt", sep="<split>\n")