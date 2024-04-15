## VaL Probing

The following guidance will help you to reproduce our results on VaL Probing mentioned in the paper or construct your own probing data.

### To Reproduce Our Results

**Step 1: Download Data.**

Our synthesized data for the three probing tasks mentioned in the paper are contained in [VaLProbing-32K](https://huggingface.co/datasets/In2Training/VaLProbing-32K/).
Download the data locally for the later inference and plotting stage.
```bash
python download.py
```
The data will be downloaded into the folder `./VaLProbing-32K/`.
Each line in the data files contains an input prompt and a ground-truth completion (label/description)

**Step 2: Inference with vLLM.**

You can directly use the downloaded data for inference without pre-processing, as these data has been formatted into the system template for FILM-7B.
**To inference with other LLMs, please change the system message and the tempelate format.**
```bash
export NCCL_IGNORE_DISABLED_P2P=1
python ../vllm_inference/vllm_inference.py --model_path In2Training/FILM-7B \
    --testdata_file document_bi_32k.jsonl \
    --testdata_folder ./VaLProbing-32K/ \
    --output_folder ./VaLProbing-32K/results/FILM-7B/ \
    --max_length 128 \
    --tensor_parallel_size 8
    
python ../vllm_inference/vllm_inference.py --model_path In2Training/FILM-7B \
    --testdata_file code_backward_32k.jsonl \
    --testdata_folder ./VaLProbing-32K/ \
    --output_folder ./VaLProbing-32K/results/FILM-7B/ \
    --max_length 128 \
    --tensor_parallel_size 8

python ../vllm_inference/vllm_inference.py --model_path In2Training/FILM-7B \
    --testdata_file database_forward_32k.jsonl \
    --testdata_folder ./VaLProbing-32K/ \
    --output_folder ./VaLProbing-32K/results/FILM-7B/ \
    --max_length 128 \
    --tensor_parallel_size 8
```

We provide our generation results in `./VaLProbing-32K/results/`.

**Step 3: Plot.**

Run `plot.py` to reproduce the Figure 1 in our paper.
Note that the examples in `*_32k_skip_list.json` are skipped during evaluation due to the ambiguity in the context (i.e., the retrieval keyword is mentioned more than one time in the context).
The figure is saved under the `./VaLProbing-32K/figures/`.
```bash
python plot.py
```



### To Construct Your Own Val Probing

We provide the [raw data](./pieces) for constructing the three probing tasks.
You can use it to construct longer context and change the retrieval pattern.
Note that you should check the ambiguity before evaluation.




