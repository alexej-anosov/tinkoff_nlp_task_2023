from fastapi import FastAPI, Request, Form, File, UploadFile, Response, Body
import uvicorn
import torch
from transformers import AutoTokenizer, AutoModelWithLMHead
import os



if not os.path.exists('model'):
    model = AutoModelWithLMHead.from_pretrained('aanosov/tb_001')
    model.save_pretrained('model')
else:
    model = AutoModelWithLMHead.from_pretrained('model')

if not os.path.exists('tokenizer'):
    tokenizer = AutoTokenizer.from_pretrained('tinkoff-ai/ruDialoGPT-small')
    tokenizer.save_pretrained('tokenizer')
else:
    tokenizer = AutoTokenizer.from_pretrained('tokenizer')


app = FastAPI()


@app.post("/tinkoffbot_api")
async def form_post(input_text: str = Body(..., embed=True)) -> dict:
    inputs = tokenizer(f'@@ПЕРВЫЙ@@ {input_text} @@ВТОРОЙ@@', return_tensors='pt')
    generated_token_ids = model.generate(
        **inputs,
        top_k=10,
        top_p=0.95,
        num_beams=3,
        num_return_sequences=3,
        do_sample=True,
        no_repeat_ngram_size=2,
        temperature=1.2,
        repetition_penalty=1.2,
        length_penalty=1.0,
        eos_token_id=50257,
        max_new_tokens=40
    )
    context_with_response = [tokenizer.decode(sample_token_ids) for sample_token_ids in generated_token_ids]
    return {'output': context_with_response[0]}



if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)