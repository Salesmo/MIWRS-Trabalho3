from flask import Flask, render_template, request
from scraper import get_info
from gemini_api import get_relatorio

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    relatorio = None

    if request.method == 'POST':
        codigo_aeroporto = request.form.get('airport')
        if codigo_aeroporto:
            dados = get_info(codigo_aeroporto.lower())
            relatorio = get_relatorio(dados)

        return render_template('index.html', relatorio=relatorio)
    return render_template('index.html', relatorio=relatorio)



if __name__ == '__main__':
    app.run(debug=True)
