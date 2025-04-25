import click
import requests

@click.command()
@click.option('--rules', default="../RULES.md")
@click.option('--file', help='File to review')
def review(rules, file):
    with open(file, "rb") as f:
        files = {"file": f}
        response = requests.post("http://localhost:8000/analyze", files=files)
        print("Full Response JSON:\n", response.json())  # Debug print
        if "output" in response.json():
            print("Analysis Result:\n", response.json()["output"])
        else:
            print("Error: 'output' key not found in response.")

if __name__ == '__main__':
    review()