# This script launches U-Net training in FP32 on 1 GPUs using 2 batch size
# Usage ./unet_TRAIN_BENCHMARK_FP32_1GPU.sh <path to this repository> <path to dataset> <path to results directory> <batch size>

 python $1/main.py \
     --data_dir $2 \
     --model_dir $3 \
     --warmup_steps 200 \
     --log_every 100 \
     --max_steps 320000 \
     --batch_size 2 \
     --benchmark \
     --exec_mode train_and_predict \
     --augment
