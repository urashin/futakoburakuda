import codecs
from KeyPhraseExtractor import KeyPharaseExtractor
from Preprocess import Preprocess
from GoogleExtractor import GoogleExtractor
from SentenceCreater import SentenceCreater

class Translator:
    def __init__(self,):
        # self.extractor = KeyPharaseExtractor(ex_type="position")
        self.extractor =  GoogleExtractor()
        self.preprocess = Preprocess()
        self.creater =  SentenceCreater()

    def translate(self, post):
        post = self.preprocess.exec(post)
        phrase = self.extractor.get_phrase(post)
        sentence_dic = self.creater.create(phrase)

        return sentence_dic

    def translate_file(self, filename="", sep="\n"):
        with codecs.open(filename, "r", "utf-8") as f:
            posts = f.read().rstrip(sep).split(sep)
        o = codecs.open("result/summarize.txt", "w", "utf-8")

        for i, post in enumerate(posts, start=0):
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
    t.translate_file("data/sample_for_test.txt", sep="<split>\n")