# DeHaDo-AI 
## NCVPRIPG-2025
[Link](https://sites.google.com/view/dehado-ai)

# DeHaDo-AI: Structured Field Extraction from Indian Form Images Using InternVL-Based OCR

This repository contains the implementation for the DeHaDo-AI Challenge (NCVPRIPG-2025), where the objective is to extract structured information from scanned form images.

---

## 🔍 Overview

We leverage **InternVL**, a Vision-Language Model (VLM), for OCR to extract key fields like candidate name, address, date of birth, government ID numbers, etc., from scanned Indian form images. The extracted results are saved in `.txt` files in a structured JSON-compatible format.

---

## 💻 Hardware & Environment

| Component     | Specification     |
|---------------|------------------|
| **GPU**       | NVIDIA RTX A5000 |
| **CUDA**      | 11.6              |
| **Python**    | 3.9.21             |

---

## 📦 Setup Instructions

### 1️⃣ Create Conda Environment

```bash
conda create -n ncvpripg_internvl python=3.9.21
conda activate ncvpripg_internvl
```

### 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### Step 1: Run OCR

- Open `prod_ocr.ipynb`
- Set the `BASE_PATH`

```python
BASE_PATH = <insert your path>
```
Assumption: The dataset follows the original shared folder structure, specifically, DEHADO-AI_TRAINING_DATASET/IMAGES_750 for images and LABELS_750 for labels.

- Set the output folder where `.txt` files should be saved.
- Run the notebook.

It will generate one `.txt` file per image in the output folder.

---

### Step 2: Generate Summary Metrics

- Open `prod_summary.ipynb`
- Set `BASE_PATH` to dataset root
- Set `TAG` to match the OCR output folder name
- Run the notebook

Outputs:

- Word Error Rate (WER)
- Character Error Rate (CER)
- Text Field Accuracy (TFA)
- Document Level Accuracy (DLA)

---

## 📫 Contact

For queries or contributions, feel free to reach out or raise an issue.
