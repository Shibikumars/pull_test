import os

def review_directory(directory, output_format="console"):
    from transformers import RobertaTokenizer, RobertaForMaskedLM
    import torch
    tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
    model = RobertaForMaskedLM.from_pretrained("microsoft/codebert-base")
    model.eval()

    results = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".java", ".cpp")):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                for i, line in enumerate(lines, 1):
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
                    
                    results.append({
                        "file": filepath,
                        "line": i,
                        "code": line.strip(),
                        "score": float(score.item())
                    })

    if output_format == "json":
        import json
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"[{r['file']}:{r['line']}] {r['code']}")
            print(f"→ Perplexity: {r['score']:.2f} {'⚠️' if r['score'] > 50 else ''}\n")
