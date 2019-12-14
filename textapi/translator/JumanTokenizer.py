from pyknp import Juman
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

class JumanTokenizer():
    _trans_tables = str.maketrans({"\"": "", "@": "＠", "#": "＃"})

    def __init__(self,):
        self.juman = Juman()

    def _preprocess(self, sentences):
        return sentences.replace(" ", "").replace("\n", "").translate(self._trans_tables)

    def tokenize(self, text):
        result = self.juman.analysis(text)
        return [mrph.midasi for mrph in result.mrph_list()]

    def _preprocess_list(self, datas):
        return [[x, self._preprocess(x)] for x in datas]
    
    def _tokenize_for_multi(self, datas):
        try:
            return [datas[0], self.tokenize(datas[1])]
        except:
            return []
    
    def tokenize_multi(self, datas, thread=cpu_count()):
        datas = self._preprocess_list(datas)
        num_of_datas = len(datas) 

        with Pool(thread) as pool:
            imap = pool.imap_unordered(self._tokenize_for_multi, datas)
            result = list(tqdm(imap, total = num_of_datas))
        return result

if __name__ == '__main__':
    tokenizer = JumanTokenizer()
    datas = ["今日の天気は晴れです" for x in range(1000)]
    result = tokenizer.tokenize_multi(datas)
    print(result[0])