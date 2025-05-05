import google.generativeai as geneai

print("Configurando API do Gemini...")
GOOGLE_GEMINI_API_KEY = "AIzaSyB2G_ZKM1cefh4o7YO0vvx0WRxStgxhKHw"
geneai.configure(api_key=GOOGLE_GEMINI_API_KEY)
model = geneai.GenerativeModel("gemini-2.0-flash-lite")
chat = model.start_chat(history=[])
print("API do Gemini configurado com sucesso!")


def get_relatorio(json_texto):
    prompt = f"""Baseado nos dados abaixo em formato JSON, gere um relatório completo sobre o desempenho dos
    voos de chegada, incluindo análises sobre *atrasos, **companhias aéreas e **aeronaves. Utilize os dados para
    identificar padrões, analisar a performance das companhias aéreas e sugerir melhorias operacionais. Além
    disso, identifique padrões na sua análise e forneça sugestões com base no que notou. Explicações dos campos:
    time -> horario previsto,
    flight -> codigo do voo,
    time-status -> horario real de chegada.
    O resto dos campos sao auto explicativos.

    JSON:
    {json_texto}
"""
    resposta = model.generate_content(prompt)
    return resposta.text.strip()
