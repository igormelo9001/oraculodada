from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer domínio, ajuste conforme necessário

# Inicializa o pipeline do GPT-Neo para geração de texto
# generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')
# generator = pipeline('text-generation', model='distilgpt2')
# generator = pipeline('text-generation', model='gpt2', max_length=20)
generator = pipeline('fill-mask', model='albert-base-v2')

frases_simuladas = [
    "Olá! Como posso ajudar você hoje?",
    "Estou aqui para responder suas perguntas.",
    "Qual é a sua dúvida?",
    "Que bom que você entrou em contato!",
    "Como posso ajudar você?",
    "Sinta-se à vontade para perguntar qualquer coisa.",
    "Estou à disposição para ajudar.",
    "Pergunte-me qualquer coisa!",
    "Estou aqui para ajudar com o que você precisar.",
    "Como posso assisti-lo hoje?"
]

@app.route('/chatbot', methods=['POST'])
def chatbot():
    """
    try:
        # Obtém a pergunta do corpo da requisição
        data = request.json
        pergunta = data.get('pergunta')
        
        if not pergunta:
            return jsonify({"erro": "Pergunta não fornecida."}), 400

        # Gera uma resposta com o GPT-Neo
        response = generator(
            pergunta,
            max_length=100,
            num_return_sequences=1,
            truncation=True,  # Ativa truncamento explícito
            pad_token_id=50256  # Define o pad_token_id como o token EOS
        )
        resposta = response[0]['generated_text']

        return jsonify({"resposta": resposta})
    
    except Exception as e:
        # Retorna uma mensagem de erro se algo der errado
        return jsonify({"erro": str(e)}), 500
    """
   
    try:
        # Obtém a pergunta do corpo da requisição
        data = request.json
        pergunta = data.get('pergunta')
        
        if not pergunta:
            return jsonify({"erro": "Pergunta não fornecida."}), 400

        # Escolhe uma frase aleatória da lista de frases simuladas
        resposta = random.choice(frases_simuladas)

        return jsonify({"resposta": resposta})
    
    except Exception as e:
        # Retorna uma mensagem de erro se algo der errado
        return jsonify({"erro": str(e)}), 500
   
@app.route('/')
def index():
    return 'Servidor Flask está rodando!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
