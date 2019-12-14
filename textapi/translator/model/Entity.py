
class Entity:
    """
    attributes
    ----------
    name: str
        抽出したフレーズ
    score: float
        抽出したフレーズの感情値
    magnitude: float
        感情の大きさ
    """
    def __init__(self, name, score, magnitude):
        self.name = name
        self.score = score
        self.magnitude = magnitude