from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

print("Loading Mistral 7B...")

# Load tokenizer & model
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.1",
    torch_dtype="auto",
    device_map="auto"
)

# Load text generation pipeline (global)
generator_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)

def generate_text(prompt: str, max_length=512):
    outputs = generator_pipeline(prompt, max_length=max_length, do_sample=False)
    return outputs[0]["generated_text"]