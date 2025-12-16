import os
import json
import re
from llama_cpp import Llama


# -----------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------

MODEL_PATH = f"./model/"
INPUT_DIR = "./data/"
OUTPUT_DIR = "./results/output_llm"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("[INFO] Loading model from:", MODEL_PATH)

# -----------------------------------------------------------
# LOAD MODEL (GPU MULTI-GPU ENABLED)
# -----------------------------------------------------------

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=131072,
    n_gpu_layers=-1,
    tensor_parallel_size=4,
    f16_kv=True,
    flash_attn=True,
    verbose=False
)



# -----------------------------------------------------------
# ROBUST JSON EXTRACTOR
# -----------------------------------------------------------

def extract_json(raw_text):
    """
    Remove markdown fences and extract only the JSON { ... } block.
    """

    text = raw_text.strip()

    # Remove code fences like ```json or ```
    text = re.sub(r"^```[a-zA-Z]*\\s*", "", text)
    text = re.sub(r"\\s*```$", "", text)

    # Extract JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found in model output")

    json_str = text[start:end+1]
    return json.loads(json_str)

# -----------------------------------------------------------
# PROMPT TEMPLATE
# -----------------------------------------------------------

PROMPT_TEMPLATE = """
Extract structured data from the obituary text.

Required fields:
- First Name
- Middle Name
- Last Name
- Birth Date
- Death Date
- Location
- Age

Rules:
- Return null if a field is missing.
- Do not guess.
- Do not wrap output in code fences.
- Return ONLY valid JSON.

JSON format:
{{
  "fname": null,
  "mname": null,
  "lname": null,
  "dob": null,
  "dod": null,
  "death_location": null,
  "age": null
}}

Obituary Text:
<<<
{obit}
>>>
"""

# -----------------------------------------------------------
# EXTRACT FIELDS
# -----------------------------------------------------------

def extract_fields(text):
    prompt = PROMPT_TEMPLATE.format(obit=text)

    out = llm(
        prompt,
        max_tokens=300,
        temperature=0.0,
        top_p=1.0,
        repeat_penalty=1.0
    )

    raw = out["choices"][0]["text"].strip()

    try:
        return extract_json(raw)
    except Exception as e:
        print("JSON Parse Error:", e)
        print("Raw output:", raw)
        return {
            "fname": None,
            "mname": None,
            "lname": None,
            "dob": None,
            "dod": None,
            "death_location": None,
            "age": None
        }

# -----------------------------------------------------------
# PROCESS ALL FILES
# -----------------------------------------------------------

def process_all():
    files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")])

    print("[INFO] Processing", len(files), "files")

    for fname in files:
        case_id = fname.replace(".txt", "")

        with open(os.path.join(INPUT_DIR, fname), "r", encoding="utf-8") as f:
            text = f.read()

        result = extract_fields(text)

        out_path = os.path.join(OUTPUT_DIR, f"{case_id}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print("Processed:", case_id)

    print("Completed processing all files")

# -----------------------------------------------------------

if __name__ == "__main__":
    process_all()
