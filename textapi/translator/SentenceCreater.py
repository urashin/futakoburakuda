import random

class SentenceCreater:
    def __init__(self, ):
        self.p_template = [
        "{}、まじさいこう。",
        "{}、ほんと大事。",
        "{}っていいよね",
        "{}…好き…"]

        self.n_template = [
            "{}、まじ…",
            "{}がね…",
            "{}かー",
            "{}、うーん",
            "おい、{}！",
            "{}、残念です。",
            "{}とかよくわかんない"]
    
    def create_sentence(self, phrase, isPositive=True):
        if isPositive:
            template = random.choice(self.p_template)
            return template.format(phrase)
        else:
            template = random.choice(self.n_template)
            return template.format(phrase)
    
    def create(self, phrase):
        sentences_dic = {}
        sentence_score = phrase.score
        sentence_magnitude = phrase.magnitude
        for k, v in phrase.entity_dic.items():
            entity_score = v.score
            entity_magnitude = v.magnitude
            sentences_dic[k] = self.create_sentence(v.name, phrase.is_positive)
        return sentences_dic

if __name__ == '__main__':
    c = SentenceCreater()
    print(c.create_sentence("猫"))
    print(c.create_sentence("猫", isPositive = False))