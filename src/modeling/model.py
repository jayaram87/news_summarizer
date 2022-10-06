import torch
import numpy as np
from transformers import T5Tokenizer, T5ForConditionalGeneration
from src.modeling.data_loader import CustomDataLoader
from src.exception import CustomException
from src.utils.util import read_yaml
from src.constants import *
import sys

torch.manual_seed(SEED)
np.random.seed(SEED)

class Train:
    def __init__(self, epochs, val_epochs, dataloader, val_dataloader):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.trainloader = dataloader
        self.valloader = val_dataloader
        self.model = T5ForConditionalGeneration.from_pretrained('t5-small').to(self.device)
        self.tokenizer = T5Tokenizer.from_pretrained('t5-small')
        self.optimizer = torch.optim.Adam(params=self.model.parameters(), lr=LR)
        self.train_epochs = epochs
        self.val_epochs = val_epochs

    def model_train(self, epoch, tokenizer, model, device, dataloader, optimizer):
        try:
            model.train(mode=True)
            for _, data in enumerate(dataloader):
                y = data['target_ids'].to(device, dtype=torch.long)
                y_ids = y[:, :-1].contiguous() # skipping the last word for the decoder model, copying the tensors n memory
                labels = y[:, 1:].clone().detach() # actual targets
                labels[y[:,1:] == tokenizer.pad_token_id] = -100 # setting the pad id 0 as -100 so that it skips model training
                ids = data['source_ids'].to(device, dtype=torch.long)
                masks = data['source_mask'].to(device, dtype=torch.long)

                outputs = model(input_ids=ids, attention_mask=masks, decoder_input_ids=y_ids, labels=labels)
                loss = outputs[0]

                if epoch % 100 == 0:
                    print(f'Train loss: {loss.item()} at epoch {epoch}')

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        except CustomException as e:
            raise CustomException(e, sys) from e

    def model_evaluate(self, tokenize, model, device, data_loader):
        try:
            model.train(mode=False)
            predictions, txts = [], []

            with torch.no_grad():
                for _, data in enumerate(data_loader):
                    y = data['target_ids'].to(device, dtype=torch.long)
                    ids = data['source_ids'].to(device, dtype=torch.long)
                    mask = data['source_mask'].to(device, dtype=torch.long)

                    # num of beams = 4, prob of 4 words
                    pred_ids = model.generate(input_ids=ids, attention_mask=mask, max_length=250, num_beams=4, repetition_penalty=2.0, length_penalty=1.0, early_stopping=True)
      
                    preds = [tokenize.decode(id, skip_special_tokens=True, clean_up_tokenization_spaces=True) for id in pred_ids]
                    target = [tokenize.decode(id, skip_special_tokens=True, clean_up_tokenization_spaces=True) for id in y]

                    predictions.extend(preds)
                    txts.extend(target)

                return predictions, txts
        
        except Exception as e:
            raise CustomException(e, sys) from e

    def training(self):
        try:
            for epoch in range(self.train_epochs):
                self.model_train(epoch, self.tokenizer, self.model, self.device, self.trainloader, self.optimizer)
        except Exception as e:
            raise CustomException(e, sys) from e

    def evaluate(self):
        try:
            for _ in range(self.val_epochs):
                predictions, summary = self.model_evaluate(self.tokenizer, self.model, self.device, self.valloader)
        except Exception as e:
            raise CustomException(e, sys) from e