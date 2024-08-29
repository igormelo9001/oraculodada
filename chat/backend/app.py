from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)
CORS(app)

# Carregar o modelo e o tokenizer GPT-2 large
model_name = "gpt2-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.json
        pergunta = data.get('pergunta')

        if not pergunta:
            return jsonify({"erro": "Pergunta não fornecida."}), 400

        # Tokenizar a entrada
        inputs = tokenizer(pergunta, return_tensors="pt")

        # Gerar resposta
        outputs = model.generate(inputs['input_ids'], max_length=100, num_return_sequences=1)
        resposta = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({"resposta": resposta})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/')
def index():
    return 'Servidor Flask com GPT-2 Large está rodando!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
