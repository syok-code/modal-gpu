# Syok free cloud GPU (Modal)

Gives you your own password-protected AI model on a free cloud GPU.
Modal's Starter plan includes about US$30 of free compute a month. Set a spending limit in Modal's billing settings first.

1. `pip install modal`
2. `modal token new` (sign in in the browser tab it opens)
3. `modal secret create syok-gpu-key SYOK_GPU_KEY=make-up-a-long-password`
4. `modal deploy app.py`

The last command prints an address ending in `.modal.run`. In Syok choose "Free cloud GPU (Modal)", type that address (without https://), the model name `Qwen/Qwen2.5-7B-Instruct`, and your password, then press Test.

After idle time the GPU sleeps; the first reply afterwards takes 1 to 2 minutes while it wakes. Syok answers from your next provider meanwhile.

If Modal has no L4 GPU free, the template automatically tries an A10 instead.
