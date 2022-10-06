import torch
from torch.utils.data import Dataset, DataLoader
from src.exception import CustomException
import sys

class CustomDataset(Dataset):
    def __init__(self, tokenizer, text, headline, text_len, headline_len):
        self.text = text
        self.headline = headline
        self.tokenizer = tokenizer # T5TOkenizer
        self.text_len = text_len
        self.headline_len = headline_len

    def __len__(self):
        return len(self.text)

    def __getitem__(self, index):
        text = str(self.text[index])
        text = ' '.join(text.split())

        htext = str(self.headline[index])
        htext = ' '.join(htext.split())

        src_tokens = self.tokenizer.batch_encode_plus([text], max_length=self.src_len, pad_to_max_length=True, return_tensors='pt')
        target_tokens = self.tokenizer.batch_encode_plus([htext], max_length=self.sum_len, pad_to_max_length=True, return_tensors='pt')

        src_ids = src_tokens['input_ids'].squeeze().to(dtype=torch.long) # reducing to a 1d vector
        src_mask = src_tokens['attention_mask'].squeeze().to(dtype=torch.long)
        target_ids = target_tokens['input_ids'].squeeze().to(dtype=torch.long)
        target_mask = target_tokens['attention_mask'].squeeze().to(dtype=torch.long)

        return {
            'source_ids': src_ids,
            'source_mask': src_mask,
            'target_ids': target_ids
        }

class CustomDataLoader:
    def __init__(self, tokenizer, text, healine, text_len, headline_len, batch_size, shuffle=False):
        self.tokenizer = tokenizer
        self.text = text
        self.headline = healine
        self.text_len = text_len
        self.headline_len = headline_len
        self.batch_size = batch_size
        self.shuffle = shuffle

    def dataloader(self):
        try:
            data = CustomDataset(tokenizer=self.tokenizer, text=self.text, headline=self.headline, text_len=self.text_len, headline_len=self.headline_len)
            data_loader = DataLoader(data, batch_size=self.batch_size, shuffle=self.shuffle, num_workers=0)
            return data_loader
        except Exception as e:
            raise CustomException(e, sys) from e