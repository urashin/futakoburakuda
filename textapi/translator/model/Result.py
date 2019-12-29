
class Result:
    """
    SentenceCreatorで返すクラス
    抽出したentityのポジネガなどの情報を格納する

    score: float
        magnitudeのスコア
    level: str
        magnitudeのスコアをもとに，テンションを分類したもの(high, mid, low)
    isPositive: boolean
        ポジティブ or ネガティブのフラグ
    summary: str
        変換した結果
    """
    def __init__(self, score, level, isPositive, summary):
        self.magnitude_score = score
        self.magnitude_level = level
        if isPositive:
            self.pn = "Positive"
        else:
            self.pn = "Negative"
        self.summary = summary

    def __str__(self):
        output = ""
        output += "pn: {}\n".format(self.pn)
        output += "magnitude_score: {:.2f}\n".format(self.magnitude_score)
        output += "magnitude_level: {}\n".format(self.magnitude_level)
        output += "summary: {}\n".format(self.summary)

        return output