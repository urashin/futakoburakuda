import six
import sys
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

class GoogleApiClient:
    def __init__(self,):
        self.client = language.LanguageServiceClient()

    def sentence_posi_nega(self, sentence):
        """
        文章のポジネガ判定apiへリクエスト
        """
        # The text to analyze
        document = types.Document(
            content=sentence,
            type=enums.Document.Type.PLAIN_TEXT)

        # Detects the sentiment of the text
        return self.client.analyze_sentiment(document=document).document_sentiment
    
    def entity_posi_nega(self, sentence):
        """
        entityのポジネガ判定apiへリクエスト
        """
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