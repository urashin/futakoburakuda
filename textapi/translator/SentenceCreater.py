import random
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from translator.model import Result, Phrase, Entity

jk_dic = {
    "positive": {
    "high": ["{}、、、ありがとうなぁ、、、くうぅ、、、", "{} 最 ＆ 高", "{} 沸いたーー！！", "{} ドチャクソ最高！", "{} すこすこのすこ！", "{} あげみざわ！", "{}っ~~!!!!!!!!!!!"],
    "mid": ["今日も！ {}！！ いい波乗ってんね〜〜！！！", "{} やばい（語彙力）", "{} めちゃよき！", "{} 、、、尊い", "{} ほんとすこ", "{}\nあぁぁぁ……(語彙力)", "{}.....神....."],
    "low": ["{}、、、よき", "{}、、、すこ", "{}、、、それな", "{} あげ"]
    },
    "negative": {
        "high":["{} さげみざわ．．．", "{} さげみぽよ．．．ぴぇぇぇぇえん", "{}とかマジ無理"],
        "mid": ["{} マジさげぽよ〜", "{}．．．ダメかも．．．", "{}とか辛みある"],
        "low": ["{} んもー", "{} ぴえん"]
        }
}

default_dic = {
    "positive": {
        "high": ["{} マジ最高…人生変わった", "{}，まじさいこう。", "{}知らないのは人生半分損してる"],
        "mid": ["{}、ほんと大事。", "{}っていいよね", "{}好きだよ", "さすが{}"],
        "low": ["{}…好き…", "{}ってのもありかも", "あー、{}ね！"]
    },
    "negative": {
        "high": ["おい、{}!", "{}、まじ…", "{}だけは許さない。", "{}嫌いだわー", "{}だけはないわ"],
        "mid": ["{}がね…", "{}、残念です。","{}とかわかんない", "{}はあんまり好きじゃない", "{}は苦手"],
        "low": ["{}かー", "{}、うーん", "{}も悪くないんだけどね", "{}ってのもなくはない"]
    }
}


tomnishi_dic = {
    "positive": {
        "high": ["さいこーさ{}", "近年稀に見る良{}"],
        "mid": ["{} 3150", "これはいい{}", "いい{}だ", "{}はアリ"],
        "low": ["{}ね、好きよ。", "{}ハマった"]
    },
    "negative": {
        "high": ["ふざけんな、{}", "ひどい{}だ", "始めて{}で悲しくなったわ"],
        "mid": ["{}がね…", "{}、残念です。","{}とかわかんない", "{}はあんまり好きじゃない", "{}は苦手"],
        "low": ["また{}か", "{}はもう飽きた", "{}ってのもなくはない"]
    }
}

class SentenceCreater:
    def __init__(self, ):
        self.jk_dic = jk_dic
        self.default_dic = default_dic

    def _choice_dic(self, mode):
        if mode == "jk":
            return self.jk_dic
        elif mode == "tomnishi":
            return self.tomnishi_dic
        else:
            return self.default_dic
    
    def _judege_tension(self, magnitude):
        if magnitude >= 1: 
            return "high"
        elif magnitude >= 0.5:
            return "mid"
        else:
            return "low"

    def _create_sentence(self, phrase, mode, tension, isPositive=True):
        dic = self._choice_dic(mode)

        if isPositive:
            dic = dic["positive"][tension]
        else:
            dic = dic["negative"][tension]

        template = random.choice(dic)
        return template.format(phrase)
    
    def _calc_magnitude(self, sentence_magnitude, entity_magnitude):
        if entity_magnitude == 0.0:
            return sentence_magnitude
        else:
            return entity_magnitude
    
    def create(self, phrase, mode):
        sentences_dic = {}
        for k, v in phrase.entity_dic.items():
            magnitude = self._calc_magnitude(phrase.magnitude, v.magnitude)
            tension = self._judege_tension(magnitude)
            summary = self._create_sentence(v.name, mode, tension, phrase.is_positive)
            sentences_dic[k] = Result(magnitude, tension, phrase.is_positive, summary)
        return sentences_dic

if __name__ == "__main__":
    creator = SentenceCreater()
    phrase_type = "key"
    entity_dic = {
        phrase_type: Entity("ラーメン", 0.0, 1.0)
    }
    phrase = Phrase(0.0, 0.0, entity_dic)
    print("default")
    print(creator.create(phrase, "default")[phrase_type])
    print("jk")
    print(creator.create(phrase, "jk")[phrase_type])
    print("tomnish")
    print(creator.create(phrase, "tomnish")[phrase_type])