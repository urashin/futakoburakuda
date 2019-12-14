import zenhan
import re

class Preprocess():
    def exec(self, sentence):
        sentence = zenhan.z2h(sentence, mode=3)
        sentence = self._normalize_re(sentence)
        return sentence.replace("\n\n", "\n").replace("!", "")
    
    def _normalize_re(self, sentence):
        sentence = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "" ,sentence)
        return sentence

if __name__ == "__main__":
    p = Preprocess()
    result = p.exec("。少し前ですがhttp://lite-ra.com/2014/11/post-605_2.htmlってどういうことなのでしょうか？カタカナ")
    print(result)