# This source code is licensed under the MIT license

import json
import os
import pdb

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import numpy as np

from tqdm import tqdm


model_infos = [
    ['FILM-7B', '#E97132', '#F4B898', '-'],
    ['Mistral-7B-Instruct-v0.2', '#7F7F7F', '#BFBFBF', '-'],
    ['gpt4-turbo', '#0F9ED5', '#87CEEA', ':'],
]


fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(30, 10), dpi=200)
fontsize = 20
# fig, ax = plt.subplots(figsize=(10, 7), dpi=200)



####### Document

total_len = 800
span_len = 50
span_num = int(total_len/span_len)

set_ids = ['set_' + str(i) for i in range(4)]

with open('./VaLProbing-32K/document_bi_32k.jsonl', 'r', encoding='utf-8') as f:
    label_infos = []
    for line in tqdm(f.readlines()):
        info = json.loads(line)
        gt = info['completion']
        position_id = info['position_id']
        set_id = info['set_id']
        set_id = 'set_' + str(set_id)
        label_infos.append({'gt': gt, 'position_id': position_id, 'set_id': set_id})

with open('./VaLProbing-32K/document_bi_32k_skip_list.json', 'r', encoding='utf-8') as f:
    skip_list = json.load(f)

for model_name, color_str, ecolor_str, linestyle in model_infos:
    set_ids_position2acc = {}
    for set_id in set_ids:
        set_ids_position2acc[set_id] = {}
        for i in range(total_len):
            set_ids_position2acc[set_id][i] = []

    with open('./VaLProbing-32K/results/' + model_name + '/sample_document_bi_32k.jsonl', 'r', encoding='utf-8') as f:
        pred_infos = [json.loads(line) for line in f.readlines()]
        for idx, (pred_info, label_info) in enumerate(tqdm(zip(pred_infos, label_infos))):

            if idx in skip_list:
                continue

            if 'gpt4' in model_name:
                pred = pred_info['sample']
            else:
                pred = pred_info['samples'][0]

            gt = label_info['gt']
            position_id = label_info['position_id']
            set_id = label_info['set_id']

            gt_words = set(gt.strip().lower().split())
            pred_words = set(pred.strip().lower().split())
            recall_score = len(gt_words & pred_words) / len(gt_words)
            set_ids_position2acc[set_id][position_id].append(recall_score)

            # if recall_score < 0.5:
            #     pdb.set_trace()

    set_ids2span_acc_list = {}
    for set_id in set_ids:
        set_ids2span_acc_list[set_id] = []
        for i in range(span_num):
            span_start = span_len*i
            span_end = span_len*i + span_len - 1
            accs = []
            for position_id in range(span_start, span_end):
                accs += set_ids_position2acc[set_id][position_id]
            acc = sum(accs) / len(accs)
            set_ids2span_acc_list[set_id].append(acc)

    span_acc_list = []
    span_std_list = []
    for i in range(span_num):
        accs = []
        for set_id in set_ids:
            accs.append(set_ids2span_acc_list[set_id][i])
        span_acc_list.append(sum(accs) / len(accs))
        span_std_list.append(np.std(np.array(accs)))

    x = [i for i in range(span_num)]

    legend_label = model_name
    ax1.errorbar(x, span_acc_list, yerr=span_std_list,
                 color=color_str, linewidth=3, marker='o', markersize=10, linestyle=linestyle,
                 ecolor=ecolor_str, elinewidth=3, capsize=6, label=legend_label)

    print(model_name, 'Statistics:')
    long_acc = sum(span_acc_list) / len(span_acc_list)
    print('long avg:', long_acc)
    print('max-min gap:', max(span_acc_list) - min(span_acc_list))
    print('\n')


x = [i for i in range(span_num)]
x_tickets = []
for i in range(span_num):
    span_name = str(span_len * i + span_len)
    x_tickets.append(span_name)


ax1.set_xticks(x)
ax1.set_xticklabels(x_tickets, fontsize=fontsize*0.5, rotation=45)
ax1.set_xlabel('Relative Positions in ' + str(total_len) + ' Sentences', fontsize=fontsize*1.5)

ax1.set_yticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax1.set_yticklabels([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], fontsize=fontsize)
ax1.set_ylabel('Performance (%)', fontsize=fontsize*1.5)

ax1.set_title('Document Sentence Retrieval (Bi-Direction)', fontsize=fontsize*1.5)

ax1.legend(loc='lower left', fontsize=fontsize)



####### Code

total_len = 800
span_len = 50
span_num = int(total_len/span_len)

set_ids = ['set_' + str(i) for i in range(4)]

with open('./VaLProbing-32K/code_backward_32k.jsonl', 'r', encoding='utf-8') as f:
    label_infos = []
    for line in tqdm(f.readlines()):
        info = json.loads(line)
        gt = info['completion']
        position_id = info['position_id']
        set_id = info['set_id']
        set_id = 'set_' + str(set_id)
        label_infos.append({'gt': gt, 'position_id': position_id, 'set_id': set_id})

with open('./VaLProbing-32K/code_backward_32k_skip_list.json', 'r', encoding='utf-8') as f:
    skip_list = json.load(f)

for model_name, color_str, ecolor_str, linestyle in model_infos:
    set_ids_position2acc = {}
    for set_id in set_ids:
        set_ids_position2acc[set_id] = {}
        for i in range(total_len):
            set_ids_position2acc[set_id][i] = []

    with open('./VaLProbing-32K/results/' + model_name + '/sample_code_backward_32k.jsonl', 'r', encoding='utf-8') as f:
        pred_infos = [json.loads(line) for line in f.readlines()]
        for idx, (pred_info, label_info) in enumerate(tqdm(zip(pred_infos, label_infos))):

            if idx in skip_list:
                continue

            if 'gpt4' in model_name:
                pred = pred_info['sample']
            else:
                pred = pred_info['samples'][0]

            gt = label_info['gt']
            position_id = label_info['position_id']
            set_id = label_info['set_id']
            if gt.strip('.') in pred:
                set_ids_position2acc[set_id][position_id].append(1)
            else:
                set_ids_position2acc[set_id][position_id].append(0)


    set_ids2span_acc_list = {}
    for set_id in set_ids:
        set_ids2span_acc_list[set_id] = []
        for i in range(span_num):
            span_start = span_len*i
            span_end = span_len*i + span_len - 1
            accs = []
            for position_id in range(span_start, span_end):
                accs += set_ids_position2acc[set_id][position_id]
            acc = sum(accs) / len(accs)
            set_ids2span_acc_list[set_id].append(acc)

    span_acc_list = []
    span_std_list = []
    for i in range(span_num):
        accs = []
        for set_id in set_ids:
            accs.append(set_ids2span_acc_list[set_id][i])
        span_acc_list.append(sum(accs) / len(accs))
        span_std_list.append(np.std(np.array(accs)))


    x = [i for i in range(span_num)]


    legend_label = model_name
    ax2.errorbar(x, span_acc_list, yerr=span_std_list,
                 color=color_str, linewidth=3, marker='o', markersize=10, linestyle=linestyle,
                 ecolor=ecolor_str, elinewidth=3, capsize=6, label=legend_label)

    print(model_name, 'Statistics:')
    long_acc = sum(span_acc_list) / len(span_acc_list)
    print('long avg:', long_acc)
    print('max-min gap:', max(span_acc_list) - min(span_acc_list))
    print('\n')



x = [i for i in range(span_num)]
x_tickets = []
for i in range(span_num):
    span_name = str(span_len * i + span_len)
    x_tickets.append(span_name)



ax2.set_xticks(x)
ax2.set_xticklabels(x_tickets, fontsize=fontsize*0.5, rotation=45)
ax2.set_xlabel('Relative Positions in ' + str(total_len) + ' Functions', fontsize=fontsize*1.5)

ax2.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax2.set_yticklabels([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], fontsize=fontsize)
# ax1.set_ylabel('Accuracy (%)')

ax2.set_title('Code Function Retrieval (Backward)', fontsize=fontsize*1.5)

# ax2.legend(loc='lower left', fontsize=fontsize*0.8)






####### Structure-Data

total_len = 750
span_len = 50
span_num = int(total_len/span_len)

set_ids = ['set_' + str(i) for i in range(4)]

with open('./VaLProbing-32K/database_forward_32k.jsonl', 'r', encoding='utf-8') as f:
    label_infos = []
    for line in tqdm(f.readlines()):
        info = json.loads(line)
        gt_label = info['label']
        gt_description = info['description']
        position_id = info['position_id']
        set_id = info['set_id']
        set_id = 'set_' + str(set_id)
        label_infos.append({'gt_label': gt_label, 'gt_description': gt_description, 'position_id': position_id, 'set_id': set_id})

with open('./VaLProbing-32K/database_forward_32k_skip_list.json', 'r', encoding='utf-8') as f:
    skip_list = json.load(f)

for model_name, color_str, ecolor_str, linestyle in model_infos:
    set_ids_position2acc = {}
    for set_id in set_ids:
        set_ids_position2acc[set_id] = {}
        for i in range(total_len):
            set_ids_position2acc[set_id][i] = []

    with open('./VaLProbing-32K/results/' + model_name + '/sample_database_forward_32k.jsonl', 'r', encoding='utf-8') as f:
        pred_infos = [json.loads(line) for line in f.readlines()]
        for idx, (pred_info, label_info) in enumerate(tqdm(zip(pred_infos, label_infos))):

            if idx in skip_list:
                continue

            if 'gpt4' in model_name:
                pred = pred_info['sample']
            else:
                pred = pred_info['samples'][0]

            gt_label = label_info['gt_label']
            gt_description = label_info['gt_description']
            position_id = label_info['position_id']
            set_id = label_info['set_id']
            if gt_label.strip('.').lower() in pred.lower() or gt_description.strip('.').lower() in pred.lower():
                set_ids_position2acc[set_id][position_id].append(1)
            else:
                set_ids_position2acc[set_id][position_id].append(0)


    set_ids2span_acc_list = {}
    for set_id in set_ids:
        set_ids2span_acc_list[set_id] = []
        for i in range(span_num):
            span_start = span_len*i
            span_end = span_len*i + span_len - 1
            accs = []
            for position_id in range(span_start, span_end):
                accs += set_ids_position2acc[set_id][position_id]
            acc = sum(accs) / len(accs)
            set_ids2span_acc_list[set_id].append(acc)

    span_acc_list = []
    span_std_list = []
    for i in range(span_num):
        accs = []
        for set_id in set_ids:
            accs.append(set_ids2span_acc_list[set_id][i])
        span_acc_list.append(sum(accs) / len(accs))
        span_std_list.append(np.std(np.array(accs)))


    x = [i for i in range(span_num)]

    legend_label = model_name
    ax3.errorbar(x, span_acc_list, yerr=span_std_list,
                 color=color_str, linewidth=3, marker='o', markersize=10, linestyle=linestyle,
                 ecolor=ecolor_str, elinewidth=3, capsize=6, label=legend_label)

    print(model_name, 'Statistics:')
    long_acc = sum(span_acc_list) / len(span_acc_list)
    print('long avg:', long_acc)
    print('max-min gap:', max(span_acc_list) - min(span_acc_list))
    print('\n')



x = [i for i in range(span_num)]
x_tickets = []
for i in range(span_num):
    span_name = str(span_len * i + span_len)
    x_tickets.append(span_name)


ax3.set_xticks(x)
ax3.set_xticklabels(x_tickets, fontsize=fontsize*0.5, rotation=45)
ax3.set_xlabel('Relative Positions in ' + str(total_len) + ' Entities', fontsize=fontsize*1.5)

ax3.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax3.set_yticklabels([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], fontsize=fontsize)
# ax1.set_ylabel('Accuracy (%)')

ax3.set_title('Database Entity Retrieval (Forward)', fontsize=fontsize*1.5)

# ax3.legend(loc='lower left', fontsize=fontsize*0.8)




plt.gcf().subplots_adjust(left=0.05, right=0.97, bottom=0.1, top=0.95)
# plt.show()
pp = PdfPages('./figures/probing_fig.pdf')
pp.savefig(fig)
pp.close()


