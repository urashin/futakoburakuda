import six
import sys, path, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from translator.GoogleApiClient import GoogleApiClient
from translator.model.Phrase import Phrase
from translator.model.Entity import Entity

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
    Natural Language APIを使ってフレーズを抽出する
    """

    def __init__(self,):
        self.client = GoogleApiClient()
        self.result = None

    def _ex_pharase_emotion(self, score, result):
        """
        投稿文と同じ傾向の感情値(posi, negaが同じもの)だけ，entityを絞り込む
        """
        entities = []
        if score >= 0:
            entities = [
                entity for entity in result.entities if entity.sentiment.score >= 0]
        else:
            entities = [
                entity for entity in result.entities if entity.sentiment.score < 0]

        if entities:
            return entities
        else:
            # 同じ感情値のentityがなければ，とりあえずそのまま返す
            return result.entities

    def _get_phrase(self, sentence):
        sentiment = self.client.sentence_posi_nega(sentence)
        result = self.client.entity_posi_nega(sentence)
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
            pn_entity = [entity for entity in sorted(
                entities, key=lambda x:x.sentiment.score, reverse=True)][0]
        else:
            pn_entity = [entity for entity in sorted(
                entities, key=lambda x:x.sentiment.score)][0]

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
