from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app)


def normalize_text(text: str) -> str:
    return (
        text.lower()
        .replace('ç', 'c')
        .replace('ã', 'a')
        .replace('á', 'a')
        .replace('â', 'a')
        .replace('é', 'e')
        .replace('ê', 'e')
        .replace('í', 'i')
        .replace('ó', 'o')
        .replace('ô', 'o')
        .replace('õ', 'o')
        .replace('ú', 'u')
        .replace('ü', 'u')
    )


def direct_answer(text: str):
    normalized = normalize_text(text)
    if 'presidente do brasil' in normalized:
        return 'O presidente do Brasil é Luiz Inácio Lula da Silva (Lula).'
    if 'capital do brasil' in normalized:
        return 'A capital do Brasil é Brasília.'
    if 'capital de portugal' in normalized:
        return 'A capital de Portugal é Lisboa.'
    if 'capital da franca' in normalized or 'capital da francia' in normalized:
        return 'A capital da França é Paris.'
    if 'quantos dias' in normalized and 'ano' in normalized:
        return 'Um ano tem 365 dias. Em anos bissextos, tem 366 dias.'

    ia_keywords = ['chatbot', 'chatbots', 'copilot', 'chatgpt', 'bing', 'api', 'apis',
                   'assistente virtual', 'assistentes virtuais', 'dialogflow', 'bot framework', 'low-code', 'low code']
    for k in ia_keywords:
        if k in normalized:
            return (
                'Existem quatro caminhos comuns para usar IA hoje:\n\n'
                '1. Chatbots prontos: plataformas como Microsoft Copilot, ChatGPT e Bing Chat já funcionam como IA de perguntas e respostas; você só precisa acessar e usar.\n\n'
                '2. APIs de IA: serviços como OpenAI, Azure AI e Hugging Face oferecem APIs. Você cria uma chave de acesso e integra em um site ou aplicativo sem treinar nada.\n\n'
                '3. Assistentes virtuais: ferramentas como Dialogflow (Google) ou Bot Framework (Microsoft) permitem montar um chatbot pronto em poucas etapas, sem precisar programar modelos de linguagem.\n\n'
                '4. Plataformas low-code: existem soluções que permitem criar IA com interface gráfica, arrastando blocos de lógica, sem precisar escrever código complexo.'
            )

    return None


def build_general_answer(text: str) -> str:
    # resposta sintetizada genérica
    summary = 'Entendi sua pergunta.'
    return f"{summary} Posso buscar mais detalhes se você quiser."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json() or {}
    message = data.get('message', '')
    if not message:
        return jsonify({'reply': 'Envie uma pergunta no campo "message".'}), 400

    reply = direct_answer(message)
    if not reply:
        reply = build_general_answer(message)

    return jsonify({'reply': reply})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
