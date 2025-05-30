import requests
import base64
from config import MATHPIX_APP_ID, MATHPIX_APP_KEY
from sympy import sympify, latex
import matplotlib.pyplot as plt
import io

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def send_to_mathpix(image_path):
    image_b64 = image_to_base64(image_path)
    headers = {
        "app_id": MATHPIX_APP_ID,
        "app_key": MATHPIX_APP_KEY,
        "Content-type": "application/json"
    }
    data = {
        "src": f"data:image/png;base64,{image_b64}",
        "formats": ["latex_simplified"]
    }
    response = requests.post("https://api.mathpix.com/v3/text", json=data, headers=headers)
    return response.json().get("latex_simplified", "")

def evaluate_latex(latex_expr):
    try:
        return sympify(latex_expr)
    except Exception as e:
        return str(e)

def save_result_image(expr, result, output_path):
    fig, ax = plt.subplots()
    ax.axis('off')
    latex_str = f"${latex(expr)} = {latex(result)}$"
    ax.text(0.1, 0.5, latex_str, fontsize=20)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
