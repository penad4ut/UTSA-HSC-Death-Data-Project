import os
import json

BASE_DIR = f"data/curation"
JSON_FILENAME = "CURATION_USER.json"

TARGETS = {
    "First_Name": "fname",
    "Middle_Name": "mname",
    "Last_Name": "lname",
    "Birth_Date": "dob",
    "Death_Date": "dod",
    "Location": "death_location",
    "Age": "age"
}

def extract_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract full obituary text
    sofaString = ""
    for obj in data["%FEATURE_STRUCTURES"]:
        if obj.get("%TYPE") == "uima.cas.Sofa":
            sofaString = obj.get("sofaString", "")
            break

    # Prepare JSON-friendly nested structure
    extracted = {v: None for v in TARGETS.values()}

    # Scan for custom.Span annotations
    for obj in data["%FEATURE_STRUCTURES"]:
        if obj.get("%TYPE") != "custom.Span":
            continue

        label = obj.get("label")
        start = obj.get("begin")
        end = obj.get("end")

        if label in TARGETS:
            out_key = TARGETS[label]

            # Only set first occurrence
            if extracted[out_key] is None:
                extracted[out_key] = {
                    "value": sofaString[start:end],
                    "start": start,
                    "end": end
                }

    return extracted


def process_all_cases(base_dir):
    results = {}

    for entry in os.listdir(base_dir):
        case_path = os.path.join(base_dir, entry)
        if not os.path.isdir(case_path):
            continue

        case_id = entry.replace(".txt", "")

        json_path = os.path.join(case_path, JSON_FILENAME)
        if not os.path.exists(json_path):
            print(f"Warning: Missing JSON in {case_path}")
            continue

        results[case_id] = extract_from_json(json_path)

    return results


# Run everything
all_results = process_all_cases(BASE_DIR)
output_file = "./results/ref_data_obituary.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

print("DONE ? obituary_gold_reference.json created.")
