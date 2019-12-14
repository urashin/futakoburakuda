import random

jk_dic = {
    "positive": {
    "high": ["{} 最 ＆ 高", "{} 沸いたーー！！", "{} わっしょい!", "{} ドチャクソ最高！", "{} あげぽよ〜", "{}まじ卍", "{}\n卍卍卍卍卍卍", "{} すこすこのすこ！", "{} あげみざわ！", "{}！！ いい波乗ってんね〜〜！！！", "{} だいすきですっ！！！"],
    "mid": ["{}、、、ありがとうなぁ、、、くうぅ、、、", "{} やばい（語彙力）", "{} めちゃよき", "{} 、、、尊い", "{}卍", "{} ほんとすこ", "{}　あげみ", "{}\nあぁぁぁ……(語彙力)", "{}.....神....."],
    "low": ["{}好きンゴ", "{}、、、よき" "{}好き[定期]", "{}、、、すこ", "{} ふぁぼ", "{}みがすごい", "、、、それな", "{} あげ"]
    },
    "negative": {
        "high":["{} さげみざわ．．．"],
        "mid": ["{} マジさげぽよ〜", "{}．．．ダメかも．．．"],
        "low": ["{} んもー", "{} ぴえん"]
        }
}

default_dic = {
    "positive": {
        "high": ["{} マジ最高…人生変わった", "{}，まじさいこう。"],
        "mid": ["{}、ほんと大事。", "{}っていいよね"],
        "low": ["{}…好き…"]
    },
    "negative": {
        "high": ["おい、{}!", "{}、まじ…", ],
        "mid": ["{}がね…", "{}、残念です。","{}とかわかんない" ],
        "low": ["{}かー", "{}、うーん"]
    }
}

class SentenceCreater:
    def __init__(self, ):
        self.jk_dic = jk_dic
        self.default_dic = default_dic

    def _choice_dic(self, mode):
        if mode == "jk":
            return self.jk_dic
        else:
            return self.default_dic
    
    def _judege_tension(self, magnitude):
        if magnitude >= 10:
            return "high"
        elif magnitude >= 5:
            return "mid"
        else:
            return "low"

    def create_sentence(self, phrase, mode, magnitude, isPositive=True):
        dic = self._choice_dic(mode)
        tension = self._judege_tension(magnitude)

        if isPositive:
            dic = dic["positive"][tension]
        else:
            dic = dic["negative"][tension]

        template = random.choice(dic)
        return template.format(phrase)
    
    def _calc_magnitude(self, sentence_magnitude, entity_magnitude):
        print("sentence:{}".format(sentence_magnitude))
        print("entity:{}".format(entity_magnitude))

        if entity_magnitude == 0.0:
            return sentence_magnitude
        else:
            entity_magnitude
    
    def create(self, phrase, mode):
        sentences_dic = {}
        for k, v in phrase.entity_dic.items():
            magnitude = self._calc_magnitude(phrase.magnitude, v.magnitude)
            sentences_dic[k] = self.create_sentence(v.name, mode, magnitude, phrase.is_positive)
        return sentences_dic