import os
import pandas as pd
import torch.utils
from transformers import AutoTokenizer, AutoModelForMaskedLM , DataCollatorForLanguageModeling
from datasets import Dataset
import time
import numpy as np
import json
from tqdm import tqdm
from transformers import (
    set_seed,
    DataCollatorForLanguageModeling,
)
import torch 
import  random
from sklearn.model_selection import train_test_split
def seed_everything(seed):
    set_seed(seed)
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True

class MyDataset(torch.utils.data.Dataset):
    def __init__(self,texts,tokenizer:AutoTokenizer):
        self.texts = texts
        self.tokenizer = tokenizer
    def __len__(self):
        return len(self.texts)
    def __getitem__(self,index):
        text = self.texts[index]
        input_dict = self.tokenizer(text,padding='max_length',max_length=156,return_tensors='pt',truncation=True)
        input_dict = {k:v.squeeze(0) for k,v in input_dict.items()}
        return input_dict


if __name__ == '__main__':
    seed_everything(0)
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    BATCH_SIZE = 16
    EPOCH = 5
    LEARNING_RATE = 4e-5
    # 加载模型和tokenizer
    tokenizer = AutoTokenizer.from_pretrained('bert_base_chinese')
    model = AutoModelForMaskedLM.from_pretrained('bert_base_chinese')
    model.to(DEVICE)

    # 加载数据集
    with open('data/clean_sentence_v2.txt','r',encoding='utf-8') as file:
        lines = [line.strip().split(',')[1] for line in file.readlines()]
    train , test = train_test_split(lines,test_size=0.2,random_state=0)
    train = MyDataset(train,tokenizer)
    test = MyDataset(test,tokenizer)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=0.15)
    # DataLoaders 
    train_dataloader = torch.utils.data.DataLoader(train ,  
        shuffle=True , collate_fn = data_collator , batch_size = BATCH_SIZE, num_workers=4)
    test_dataloader = torch.utils.data.DataLoader(test , 
        shuffle=False , collate_fn = data_collator , batch_size = BATCH_SIZE , num_workers=4)

    print(f'数据集加载完成 训练集 {len(train)} 测试集 {len(test)}')

    # 设置优化器和学习率调度器
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
    best_loss = float('inf')
    print(f'开始训练')
    train_loss_list = []
    test_loss_list = []
    for epoch in range(EPOCH):
        # train
        model.train()
        progress_bar = tqdm(train_dataloader)
        train_loss = 0.
        cnt = 0
        for batch in progress_bar:
            progress_bar.set_description(f'Ep {epoch} Training...')
            # 获取输入数据和标签
            batch = {key: val.to(DEVICE) for key, val in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_loss+=loss.item()
            cnt += batch['input_ids'].shape[0]
        train_loss = train_loss / cnt
        train_loss_list.append(train_loss)
        # eval
        model.eval()
        test_loss = 0.
        cnt = 0
        with torch.no_grad():
            for batch in progress_bar:
                progress_bar.set_description(f'Ep {epoch} Testing...')
                # 获取输入数据和标签
                batch = {key: val.to(DEVICE) for key, val in batch.items()}
                outputs = model(**batch)
                loss = outputs.loss
                test_loss+=loss.item()
                cnt += batch['input_ids'].shape[0]
        test_loss = test_loss / cnt
        test_loss_list.append(test_loss)

        if test_loss < best_loss:
            best_loss = test_loss
            torch.save(model.state_dict() ,'sentence_transformer/mlm_chkpt.pth')
        print(f'Ep {epoch} train_loss {train_loss:.5f} test_loss {test_loss:.5f}')
    print(f'训练完毕')
    with open('sentence_transformer/record.json','w') as file:
        json.dump({'train_loss':train_loss_list,'test_loss':test_loss_list},file,indent=4,ensure_ascii=False)
