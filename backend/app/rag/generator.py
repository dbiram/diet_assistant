from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

print("Loading TinyLlama 1.1B Chat...")

# Load TinyLlama tokenizer & model
tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")

# Load text generation pipeline (global)
generator_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)

def generate_text(prompt: str, max_length=512):
    outputs = generator_pipeline(prompt, max_length=max_length, do_sample=False)
    return outputs[0]["generated_text"]