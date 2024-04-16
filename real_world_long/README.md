## Real-World Long-Context Tasks

The following guidance will help you to reproduce our results on real-wordl long-context tasks.
The test prompts and evaluation scripts are modified from [LongBench](https://github.com/THUDM/LongBench).

**Step 1: Extract Data and Inference with vLLM.**

The test data in `./prompts/` have been formatted into the system template for FILM-7B.
The filenames indicate the max output length for different tasks during inference, following the default settings in LongBench.
```bash
# Extract Data
cd ./prompts/
unzip LongBench_output_32_64.zip
unzip LongBench_output_128_512.zip
cd ..

# Inference
export NCCL_IGNORE_DISABLED_P2P=1
python ../vllm_inference/vllm_inference.py --model_path In2Training/FILM-7B \
    --testdata_file LongBench_output_32.jsonl \
    --testdata_folder ./prompts/ \
    --output_folder ./results/FILM-7B/ \
    --max_length 32 \
    --tensor_parallel_size 8

python ../vllm_inference/vllm_inference.py --model_path In2Training/FILM-7B \
    --testdata_file LongBench_output_64.jsonl \
    --testdata_folder ./prompts/ \
    --output_folder ./results/FILM-7B/ \
    --max_length 64 \
    --tensor_parallel_size 8

python ../vllm_inference/vllm_inference.py --model_path In2Training/FILM-7B \
    --testdata_file LongBench_output_128.jsonl \
    --testdata_folder ./prompts/ \
    --output_folder ./results/FILM-7B/ \
    --max_length 128 \
    --tensor_parallel_size 8

python ../vllm_inference/vllm_inference.py --model_path In2Training/FILM-7B \
    --testdata_file LongBench_output_512.jsonl \
    --testdata_folder ./prompts/ \
    --output_folder ./results/FILM-7B/ \
    --max_length 512 \
    --tensor_parallel_size 8
```

We provide our generation results in `./results/`, including FILM-7B, Mistral-7B-Instruct-v0.2, and GPT-4-Turbo.

**Step 2: Evaluation.**

Run `evaluate.py` to calculate evaluation metrics on different tasks.
```bash
python evaluate.py
```




