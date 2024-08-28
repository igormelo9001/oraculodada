from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding
import numpy as np

app = Flask(__name__)
CORS(app)
# Textos fixos para treinamento
text = ""
# Inicializa o Tokenizer
tokenizer = Tokenizer()

# Variáveis globais para armazenar o modelo e os parâmetros
total_words = 0
max_sequence_len = 0
model = None

def treinar_modelo(texts):
    global tokenizer, total_words, max_sequence_len, model
    
    # Tokenização dos textos
    tokenizer.fit_on_texts(texts)
    total_words = len(tokenizer.word_index) + 1

    # Preparação das sequências de entrada e saída
    input_sequences = []
    for text in texts:
        token_list = tokenizer.texts_to_sequences([text])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i+1]
            input_sequences.append(n_gram_sequence)

    # Padronização do comprimento das sequências
    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

    # Divisão das sequências em inputs e labels
    X, y = input_sequences[:,:-1], input_sequences[:,-1]
    y = np.eye(total_words)[y]

    # Criação do modelo LSTM
    model = Sequential()
    model.add(Embedding(total_words, 10, input_length=max_sequence_len-1))
    model.add(LSTM(100))
    model.add(Dense(total_words, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')
    model.fit(X, y, epochs=100)

def gerar_texto(seed_text, next_words=3):
    global tokenizer, model, max_sequence_len
    
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
        predicted = np.argmax(model.predict(token_list), axis=-1)
        output_word = tokenizer.index_word[predicted[0]]
        seed_text += " " + output_word
    
    return seed_text

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.json
        pergunta = data.get('pergunta')
        
        if not pergunta:
            return jsonify({"erro": "Pergunta não fornecida."}), 400

        resposta = gerar_texto(pergunta)
        #resposta = gerar_texto(text)
        return jsonify({"resposta": resposta})
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/upload-text', methods=['POST'])
def upload_text():
    try:
        data = request.json
        new_text = data.get('text')
        
        if not new_text:
            return jsonify({"erro": "Texto não fornecido."}), 400

        # Atualize a variável global `text` com o novo conteúdo
        global text
        text = new_text

        # Treine o modelo com o novo texto
        treinar_modelo([text])
        
        return jsonify({"mensagem": "Texto atualizado e modelo treinado."})
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500    

@app.route('/')
def index():
    return 'Servidor Flask com LSTM está rodando!'

if __name__ == '__main__':
    # Treina o modelo ao iniciar o servidor
    treinar_modelo(text)
    app.run(host='0.0.0.0', debug=True)
