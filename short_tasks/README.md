## Short-Context Tasks

The following guidance will help you to reproduce our results on short-context tasks.

### Results on GSM8K, MATH and CSQA

We leverage the evaluation data scripts in [LEMA](https://github.com/microsoft/LEMA/).
The few-shot examples for GSM8K and MATH are chosen from their training set according to the input similarity.

**Step 1: Inference with vLLM.**

The test data in `./prompts/` have been formatted into the system template for FILM-7B.
```bash
# Extract Data

# Inference
export NCCL_IGNORE_DISABLED_P2P=1
python ../vllm_inference/vllm_inference.py --model_path In2Training/FILM-7B \
    --testdata_file gsm8k_8shot.jsonl \
    --testdata_folder ./prompts/ \
    --output_folder ./results/FILM-7B/ \
    --max_length 2048 \
    --tensor_parallel_size 8

python ../vllm_inference/vllm_inference.py --model_path In2Training/FILM-7B \
    --testdata_file math_4shot.jsonl \
    --testdata_folder ./prompts/ \
    --output_folder ./results/FILM-7B/ \
    --max_length 2048 \
    --tensor_parallel_size 8

python ../vllm_inference/vllm_inference.py --model_path In2Training/FILM-7B \
    --testdata_file csqa_0shot.jsonl \
    --testdata_folder ./prompts/ \
    --output_folder ./results/FILM-7B/ \
    --max_length 128 \
    --tensor_parallel_size 8
```

We provide our generation results in `./results/`, including FILM-7B and Mistral-7B-Instruct-v0.2.

**Step 2: Evaluation.**

Run `evaluation.py` to calculate evaluation metrics on different tasks.
```bash
python evaluation.py
```


### Results on Other Tasks

We utilize the [lm_eval](https://github.com/EleutherAI/lm-evaluation-harness) for the evaluation on MMLU, BoolQ, RACE-H, ARC-C, and HellaSwag.
The results could have slight variances with different versions of lm_eval.

