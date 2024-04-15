# This source code is licensed under the MIT license

import json
from datasets import load_dataset
import os
from tqdm import tqdm

dataset = load_dataset("In2Training/VaLProbing-32K")

categories = list(dataset.keys())

if not os.path.exists('./ValProbing-32K/'):
    os.mkdir('./ValProbing-32K/')

for cate in categories:
    with open('./ValProbing-32K/' + cate + '.jsonl', 'w', encoding='utf-8') as f_write:
        for info in tqdm(dataset[cate]):
            for key in list(info.keys()):
                if info[key] == ' ':
                    info.pop(key)
            f_write.write(json.dumps(info) + '\n')
