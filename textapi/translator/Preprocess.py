import zenhan
import re
import emoji

class Preprocess():
    def exec(self, sentence):
        sentence = zenhan.z2h(sentence, mode=3)
        sentence = self._remove_emoji(sentence)
        sentence = self._normalize_re(sentence)
        return sentence.replace("\n\n", "\n").replace("!", "")

    def _remove_emoji(self, sentence):
        return ''.join(c for c in sentence if c not in emoji.UNICODE_EMOJI)
    
    def _normalize_re(self, sentence):
        # urlを削除
        sentence = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "" ,sentence)
        # 複数改行を削除
        sentence = re.sub(r"\n{2,}", "", sentence)
        # ハッシュタグを削除
        sentence = re.sub(r"#.*$\n", "", sentence, flags=re.MULTILINE)
        return sentence

if __name__ == "__main__":
    text = """
    おはようございます
    手が冷たい午前5時
    ハッシュタグで朝ランと打つと朝ラン久しぶりと予測変換
    まあ当ってるから文句言えない
    少し前ですがhttp://lite-ra.com/2014/11/post-605_2.htmlってどういうことなのでしょうか？カタカナ

    #朝ラン
    #ハシリマスタグラム
    #熊本城マラソン2020
    #熊本
    #手が冷たい
    (｀ヘ´) 🤗⭕🤓🤔🤘🦁⭐🆗🆖🈲🤐🤗🤖🤑🆙⏩

    #朝ラン久しぶり
    """
    p = Preprocess()
    result = p.exec(text)
    print(result)