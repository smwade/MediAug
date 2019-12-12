# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script launches U-Net inference in TF-AMP on 1 GPUs using 2 batch size
# Usage ./unet_INFER_BENCHMARK_TF-AMP.sh <path to this repository> <path to dataset> <path to results directory> <batch size>

python $1/main.py --data_dir $2 --model_dir $3 --batch_size $4 --benchmark --use_amp --exec_mode predict --augment --warmup_steps 200 --log_every 100 --max_steps 300
