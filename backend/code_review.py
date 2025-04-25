from transformers.models.roberta import RobertaTokenizer, RobertaForMaskedLM
import torch

# Load model and tokenizer
tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
model = RobertaForMaskedLM.from_pretrained("microsoft/codebert-base")
model.eval()

# Set your code file here
file_path = "test.js"  # Change this if needed

# Read code
with open(file_path, 'r') as f:
    code_lines = f.readlines()

print("🔍 Reviewing code line by line...\n")

# Line-by-line analysis
for i, line in enumerate(code_lines, 1):
    if not line.strip():
        continue  # skip empty lines

    inputs = tokenizer(line, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        loss_fn = torch.nn.CrossEntropyLoss()
        shift_logits = outputs.logits[..., :-1, :].contiguous()
        shift_labels = inputs.input_ids[..., 1:].contiguous()
        loss = loss_fn(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
        score = torch.exp(loss)  # Perplexity

    print(f"Line {i}: {line.strip()}")
    print(f"🧠 Model Perplexity Score: {score.item():.2f} {'⚠️' if score.item() > 50 else ''}\n")
# 🧾 Optional: Save results to an HTML file for visualization
html_lines = []

for i, line in enumerate(code_lines, 1):
    if not line.strip():
        continue
    inputs = tokenizer(line, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        loss_fn = torch.nn.CrossEntropyLoss()
        shift_logits = outputs.logits[..., :-1, :].contiguous()
        shift_labels = inputs.input_ids[..., 1:].contiguous()
        loss = loss_fn(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
        score = torch.exp(loss)
        color = "red" if score.item() > 50 else "green"
        html_lines.append(
            f"<p><b>Line {i}:</b> <code>{line.strip()}</code><br><span style='color:{color}; font-weight:bold'>Perplexity: {score.item():.2f}</span></p>"
        )

with open("report.html", "w", encoding="utf-8") as report_file:
    report_file.write("<html><body><h2>📋 CodeBERT Line-by-Line Review</h2>" + "\n".join(html_lines) + "</body></html>")

print("✅ HTML report generated as: report.html")
