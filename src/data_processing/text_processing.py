import re
import sys
from src.logger import *
from src.exception import CustomException
import unicodedata
import contractions

class TextProcessing:
    def __init__(self, text):
        self.text = text

    def text_cleaning(self):
        """
        Data preparation for the T5 transformer model
        """
        try:
            text = ''.join(i for i in unicodedata.normalize('NFD', self.text) if unicodedata.category(i) != 'Mn')
            text = ' '.join([contractions.fix(i) for i in text.split(' ')])
            text = re.sub(r'[" "]+', ' ', text)
            text = re.sub(r'[^a-zA-Z.]+', ' ', text).strip()
            text = re.sub(r'(\\t)|(\\r)|(\\n)|(__+)|(--+)|(~~+)|(\+\++)|(\.\.+)|(\.\s+)|(\-\s+)|(\:\s+)|(\s+.\s+)|(\s+)|(\s+.\s+)', ' ', text)
            text = re.sub(r'[<>()|&©ø\[\]\'\",;?~*!]', ' ', text)
            text = re.sub(r'(mailto:)', ' ', text)
            text = re.sub(r'((https*:\/*)([^\/\s]+))(.[^\s]+)', '', text)
            text = 'summarize: ' + text # text format for the T5 model
            
            return text

        except Exception as e:
            raise CustomException(e, sys) from e