# This source code is licensed under the MIT license

import os
import json
import pdb

from metrics import (
    qa_f1_score,
    rouge_score,
)

datasets = [
    "narrativeqa", "qasper", "multifieldqa_en",
    "hotpotqa", "2wikimqa", "musique",
    "gov_report", "qmsum", "multi_news",
]

dataset2metric = {
    "narrativeqa": qa_f1_score,
    "qasper": qa_f1_score,
    "multifieldqa_en": qa_f1_score,
    "hotpotqa": qa_f1_score,
    "2wikimqa": qa_f1_score,
    "musique": qa_f1_score,
    "gov_report": rouge_score,
    "qmsum": rouge_score,
    "multi_news": rouge_score,
}

def scorer(dataset, predictions, answers, all_classes):
    total_score = 0.
    for (prediction, ground_truths) in zip(predictions, answers):
        score = 0.
        if dataset == "samsum":
            prediction = prediction.lstrip('\n').split('\n')[0]
        for ground_truth in ground_truths:
            score = max(score, dataset2metric[dataset](prediction, ground_truth, all_classes=all_classes))
        total_score += score
    return round(100 * total_score / len(predictions), 2)

model_names = ['FILM-7B', 'Mistral-7B-Instruct-v0.2', 'gpt4-turbo']

label_filenames = [
    'LongBench_output_32.jsonl',
    'LongBench_output_64.jsonl',
    'LongBench_output_128.jsonl',
    'LongBench_output_512.jsonl',
]

pred_filenames = [
    'sample_LongBench_output_32.jsonl',
    'sample_LongBench_output_64.jsonl',
    'sample_LongBench_output_128.jsonl',
    'sample_LongBench_output_512.jsonl',
]

for model_name in model_names:
    print(model_name)

    detaset2infos = {}
    for dataset in datasets:
        detaset2infos[dataset] = {'predictions': [],
                                  'answers': [],
                                  'all_classes': None}

    for pred_filename, label_filename in zip(pred_filenames, label_filenames):
        with open(os.path.join('results', model_name, pred_filename), 'r', encoding='utf-8') as f_read:
            pred_infos = [json.loads(line) for line in f_read.readlines()]

        with open(os.path.join('prompts', label_filename), 'r', encoding='utf-8') as f_read:
            label_infos = [json.loads(line) for line in f_read.readlines()]

        assert len(pred_infos) == len(label_infos)

        for pred_info, label_info in zip(pred_infos, label_infos):
            if 'gpt4' in model_name:
                pred = pred_info['sample']
            else:
                pred = pred_info['samples'][0]

            if pred is None:
                pred = ''
                continue

            answers = label_info['answers']
            dataset = label_info['dataset']

            detaset2infos[dataset]['predictions'].append(pred)
            detaset2infos[dataset]['answers'].append(answers)

            all_classes = label_info['all_classes']
            if all_classes:
                detaset2infos[dataset]['all_classes'] = all_classes


    for dataset in datasets:
        score = scorer(dataset, detaset2infos[dataset]['predictions'], detaset2infos[dataset]['answers'], detaset2infos[dataset]['all_classes'])
        print(dataset, score)

