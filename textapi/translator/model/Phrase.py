class Phrase:
    """
    それぞれのextractorからのフレーズを格納するクラス

    attributes
    ----------
    score: float
        ポジネガスコア(-1 ~ 1)
    magnitude: float
        感情の大きさ
    entity_dic: dic
        key: entityの種類, value: GoogleのEntityクラス
    """
    def __init__(self, score, magnitude, entity):
        self.score = score
        self.magnitude = magnitude
        self.entity_dic = entity

        if self.score >= 0:
            self.is_positive = True
        else:
            self.is_positive = False