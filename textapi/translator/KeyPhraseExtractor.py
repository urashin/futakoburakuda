import nltk
import pke
import ginza
import nltk

class KeyPharaseExtractor:
    def __init__(self, ex_type="multi"):
        ## pkeを使うための初期化処理
        nltk.download('stopwords')
        pke.base.ISO_to_language['ja_ginza'] = 'japanese'
        stopwords = list(ginza.STOP_WORDS)
        nltk.corpus.stopwords.words_org = nltk.corpus.stopwords.words
        nltk.corpus.stopwords.words = lambda lang : stopwords if lang == 'japanese' else nltk.corpus.stopwords.words_org(lang)

        ## attributes
        self.ex_type = ex_type
    
    def create_extractor(self, sentence):
        if self.ex_type == "multi":
            extractor = pke.unsupervised.MultipartiteRank()
            extractor.load_document(input=sentence, language='ja_ginza', normalization=None)
            # 抽出する品詞の指定
            # propn: 固有名詞
            extractor.candidate_selection(pos={'NOUN', 'PROPN'})
            # 重みの指定(デフォルト値になっている)
            extractor.candidate_weighting(threshold=0.74, method='average', alpha=1.1)
            return extractor
        elif self.ex_type == "position":
            extractor = pke.unsupervised.PositionRank()
            extractor = pke.unsupervised.PositionRank()
            # extractorにテキストをロードさせる
            extractor.load_document(input=sentence, language='ja_ginza', normalization=None)
            extractor.candidate_selection(pos={'NOUN', 'PROPN'})
            extractor.candidate_weighting(window=5)
            return extractor
        else:
            raise TypeError("存在しないextractorを指定しています")

    def get_phrases(self, sentence):
        """
        returns
        -------
        result: List[Tuple(str, float)]
            抽出結果上位のリスト
            ex) [(フレーズ，スコア), ...]
        """
        try:
            # extractorにテキストをロードさせる
            extractor = self.create_extractor(sentence)
            return extractor.get_n_best(n=10)
        except ValueError:
            return [(sentence, 0.0)]
    
    def filter_phrase(self, phrases):
        """
        フレーズの中から最もらしいものを抜き出す処理
        """
        # とりあえずスコアが最大値のもの1つを返す
        return phrases[0][0].replace(" ", "")
    
    def extract_sentence(self, phrase, sentence):
        """
        フレーズが含まれる文を抽出する
        """
        output = ""
        for line in sentence.splitlines():
            if phrase in line:
                output += line + "\n"
        return output

    def translate(self, sentence):
       phrases = self.get_phrases(sentence) 
       phrase = self.filter_phrase(phrases)
       self.extract_sentence(phrase, sentence)

if __name__ == '__main__':
    k =KeyPharaseExtractor(ex_type="multi")
    k.translate("パンおいしい")