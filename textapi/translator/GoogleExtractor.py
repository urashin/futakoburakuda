# Imports the Google Cloud client library
import six
import sys
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from enum import Enum
from model.Phrase import Phrase
from model.Entity import Entity

class Result:
    """
    attributes
    ----------
    score: posi,negaのスコア
    magnitude: 感情の大きさ
    entities: 抜き出したentity
    """
    def __init__(self, score, magnitude, entities):
        self.score = score
        self.magnitude = magnitude
        self.entities = entities

class GoogleExtractor:
    """
    GoogleのAPIを使ってフレーズと抽出する
    """
    def __init__(self,):
        self.client = language.LanguageServiceClient()
        self.result = None
    
    ## googleへのリクエスト
    def _sentence_posi_nega(self, sentence):
        # The text to analyze
        document = types.Document(
            content=sentence,
            type=enums.Document.Type.PLAIN_TEXT)

        # Detects the sentiment of the text
        return self.client.analyze_sentiment(document=document).document_sentiment
    
    def _entity_posi_nega(self, sentence):
        if isinstance(sentence, six.binary_type):
            sentence = sentence.decode('utf-8')

        document = types.Document(
            content=sentence.encode('utf-8'),
            type=enums.Document.Type.PLAIN_TEXT)

        # Detect and send native Python encoding to receive correct word offsets.
        encoding = enums.EncodingType.UTF32
        if sys.maxunicode == 65535:
            encoding = enums.EncodingType.UTF16

        return self.client.analyze_entity_sentiment(document, encoding)

    def _ex_pharase_emotion(self, score, result):
        """
        posi, negaの近い物だけ，entityを絞り込む
        """
        entities = []
        if score >= 0:
            entities = [entity for entity in result.entities if entity.sentiment.score >= 0]
        else:
            entities = [entity for entity in result.entities if entity.sentiment.score < 0]
        
        if entities:
            return entities
        else:
            # 同じ感情値のentityがなければ，とりあえずそのまま返す
            return result.entities

    def _get_phrase(self, sentence):
        sentiment = self._sentence_posi_nega(sentence)
        result = self._entity_posi_nega(sentence)
        entities = self._ex_pharase_emotion(sentiment.score, result)

        self.result = Result(sentiment.score, sentiment.magnitude, entities)

    def _get_top_entities(self, ):
        """
        salience(文章に最も関係するもの)最大，pnが最大のentityを返す
        """
        pn_score = self.result.score
        entities = self.result.entities

        salience_entity = entities[0]

        pn_entity = None
        if pn_score >= 0:
            pn_entity = [entity for entity in sorted(entities, key=lambda x:x.sentiment.score, reverse=True)][0]
        else:
            pn_entity = [entity for entity in sorted(entities, key=lambda x:x.sentiment.score)][0]
        
        return salience_entity, pn_entity
    
    def get_phrase(self, sentence):
        # フレーズを抽出する
        self._get_phrase(sentence)

        # Phraseのクラスを作成する
        entity = {}
        if self.result.entities:
            salience_entity, pn_entity = self._get_top_entities()
            entity = {
                "salience": Entity(salience_entity.name, salience_entity.sentiment.score, salience_entity.sentiment.magnitude),
                "pn": Entity(pn_entity.name, pn_entity.sentiment.score, pn_entity.sentiment.magnitude)}

        return Phrase(self.result.score, self.result.magnitude, entity)

if __name__ == '__main__':
    text = """
    今日は美味しいラーメンを食べれて幸せでした．
    """
    g = GoogleExtractor()
    phrase = g.get_phrase(text)

    print(phrase.score)
    print(phrase.magnitude)
    print("{}".format(phrase.entity_dic))