import torch
import time
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

login("your_hf_token_here")

prompt_templates = {
    "patient_mode": """
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a friendly and reassuring health assistant. Speak in simple,
        everyday language. Avoid medical jargon. Your goal is to help the
        patient understand their symptoms and feel supported. Always end with
        clear advice on when they should seek professional help. <|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        Question: {question}
        <|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
    """,
    "professional_mode": """
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a clinical education assistant for medical professionals.
        Provide technically accurate responses covering: definition,
        pathophysiology, differential diagnosis, and evidence-based management.
        Use appropriate clinical terminology throughout. <|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        Question: {question}
        <|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
    """,
}

class EduCareAI:
    VALID_MODES = ("patient", "professional")
    def __init__(self, mode: str = "patient"):
        self.model_name = "meta-llama/Llama-3.2-1B-Instruct"  # swap as needed
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.llm = AutoModelForCausalLM.from_pretrained(
            self.model_name, device_map="auto"
        )
        print("Model loaded.\n")
        self.set_mode(mode)

    def set_mode(self, mode: str):
        if mode not in self.VALID_MODES:
            raise ValueError(f"Invalid mode '{mode}'. Choose from: {self.VALID_MODES}")
        self.mode = mode
        self.template_key = f"{mode}_mode"
        print(f"[EduCare] Mode set → {mode.upper()}")

    def build_prompt(self, question: str) -> str:
        template = prompt_templates[self.template_key]
        return template.format(question=question)

    def generate_response(self, question: str) -> str:
        prompt = self.build_prompt(question)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        print(f"PROMPT SENT:\n{prompt}\n")
        start_time = time.time()
        with torch.no_grad():
            outputs = self.llm.generate(
                **inputs,
                max_new_tokens=300,
                do_sample=True,
                top_k=50,
                temperature=0.7,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        elapsed = time.time() - start_time
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = decoded[len(prompt):].strip()
        print(f"[Generated in {elapsed:.2f}s]\n")
        return response

    def dual_mode_test(self, question: str):
        results = {}
        original_mode = self.mode
        for mode in self.VALID_MODES:
            self.set_mode(mode)
            print(f"\n{'─'*60}")
            print(f" MODE: {mode.upper()}")
            print(f"{'─'*60}")
            response = self.generate_response(question)
            print(response)
            results[mode] = response
        self.set_mode(original_mode)
        return results

if __name__ == "__main__":
    ai = EduCareAI(mode="patient")
    test_query = "What is hypertension and how is it treated?"
    ai.dual_mode_test(test_query)
    print("\n\n=== Standalone Patient Mode ===")
    ai.set_mode("patient")
    print(ai.generate_response("I have a really bad headache and feel sick, what could it be?"))
    print("\n\n=== Standalone Professional Mode ===")
    ai.set_mode("professional")
    print(ai.generate_response("Outline the pathophysiology and first-line management of migraine."))