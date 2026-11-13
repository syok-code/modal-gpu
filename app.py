"""Free cloud GPU for Syok AI, running on Modal.

Serves an OpenAI-compatible endpoint (vLLM) that is protected by a password.
UNTESTED TEMPLATE: written from Modal's public docs, not yet run on a real Modal account.

Deploy:  modal deploy app.py
"""
import os
import subprocess

import modal

MODEL = "Qwen/Qwen2.5-7B-Instruct"   # 7B model; fits an L4 (24 GB) in fp16
GPU = ["L4", "A10"]  # tries L4 first, then A10 when no L4 is free (both fit this model)
SCALEDOWN_SECONDS = 300               # sleep after 5 idle minutes to save your free credit
PORT = 8000

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("vllm==0.10.1.1", "transformers==4.55.4", "huggingface_hub[hf_transfer]")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
)

hf_cache = modal.Volume.from_name("syok-hf-cache", create_if_missing=True)

app = modal.App("syok-gpu")


@app.function(
    image=image,
    gpu=GPU,
    scaledown_window=SCALEDOWN_SECONDS,
    timeout=60 * 60,
    volumes={"/root/.cache/huggingface": hf_cache},
    secrets=[modal.Secret.from_name("syok-gpu-key")],  # holds SYOK_GPU_KEY, your password
)
@modal.concurrent(max_inputs=16)
@modal.web_server(PORT, startup_timeout=10 * 60)
def serve():
    cmd = [
        "vllm", "serve", MODEL,
        "--host", "0.0.0.0", "--port", str(PORT),
        "--served-model-name", MODEL,
        "--api-key", os.environ["SYOK_GPU_KEY"],
        "--max-model-len", "16384",
        "--gpu-memory-utilization", "0.90",
    ]
    subprocess.Popen(cmd)
