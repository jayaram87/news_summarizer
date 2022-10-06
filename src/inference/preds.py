import sys
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
from src.exception import CustomException
from src.utils.util import read_yaml
from src.constants import *

class Inference:
    def __init__(self, model_path=MODEL_PATH, tokenizer_path=TOKENIZER_PATH):
        self.tokenizer = T5Tokenizer.from_pretrained(tokenizer_path)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = self.__model_load(model_path).to(self.device)

    def __model_load(self, model_path):
        try:
            config = T5Config.from_pretrained("t5-small")
            return T5ForConditionalGeneration.from_pretrained(model_path, config=config)
        except Exception as e:
            raise CustomException(e, sys) from e

    def inference(self, text):
        """
        Generates the summary text of the news article
        """
        try:
            params = read_yaml(MODEL_CONFIG_PATH)[PARAMS]
            tensors = self.tokenizer.batch_encode_plus(
                [text], 
                max_length=int(params[TEXT_LEN]), 
                pad_to_max_length=True)

            summary = self.model.generate(
                        input_ids=torch.tensor(tensors['input_ids']).to(dtype=torch.long),
                        attention_mask=torch.tensor(tensors['attention_mask']).to(dtype=torch.long),
                        max_length=int(params[TEXT_LEN]),
                        num_beams=int(params[NUM_BEAMS]),
                        repetition_penalty=float(params[REPETITION_PENALTY]),
                        length_penalty=float(params[LEN_PENALTY]),
                        early_stopping=True
                    )
            return ' '.join([self.tokenizer.decode(id, skip_special_tokens=True, clean_up_tokenization_spaces=True) for id in summary])

        except Exception as e:
            raise CustomException(e, sys) from e