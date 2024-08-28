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
text = """
A Ascensão da China e suas Implicações Geopolíticas Globais

Introdução

Nas últimas décadas, a China emergiu como uma das potências globais mais influentes, transformando-se de uma economia relativamente fechada e isolada para uma superpotência econômica e militar. Este fenômeno não é apenas um evento econômico, mas também geopolítico, com implicações profundas para a ordem global, relações internacionais, e a balança de poder mundial.

1. O Crescimento Econômico Chinês

A ascensão da China começou com as reformas econômicas iniciadas por Deng Xiaoping no final da década de 1970. Ao abrir a economia chinesa ao investimento estrangeiro, promover a privatização de setores estatais, e incentivar a inovação tecnológica, a China conseguiu alcançar um crescimento econômico sem precedentes. Nas décadas seguintes, o país tornou-se a segunda maior economia do mundo, superando potências tradicionais como o Japão e se aproximando cada vez mais dos Estados Unidos.

Este crescimento econômico deu à China uma enorme influência global. O país é agora um dos maiores exportadores e importadores do mundo, o que lhe confere um papel central no comércio internacional. Além disso, a China investiu pesadamente em infraestrutura global através da Iniciativa do Cinturão e Rota (BRI), um ambicioso projeto que visa construir redes de transporte, energia, e telecomunicações em dezenas de países, solidificando ainda mais a sua posição geopolítica.

2. Expansão Militar e Estratégica

O crescimento econômico da China também possibilitou uma expansão significativa de suas capacidades militares. A modernização das forças armadas chinesas, incluindo o desenvolvimento de tecnologias avançadas, como mísseis hipersônicos, drones, e capacidades cibernéticas, fez com que o país se tornasse uma das forças militares mais poderosas do mundo.

O Mar do Sul da China tornou-se um ponto focal da estratégia militar chinesa. A construção de ilhas artificiais e a militarização dessas áreas têm gerado tensões com países vizinhos e com os Estados Unidos, que veem as ações da China como uma ameaça à liberdade de navegação e à estabilidade regional. Essa assertividade militar reflete a ambição da China de controlar suas rotas marítimas estratégicas e proteger seus interesses econômicos e territoriais.

3. A Política Externa Chinesa e a Diplomacia

A política externa da China passou por uma transformação significativa desde o final do século XX. De uma postura mais defensiva e cautelosa, o país evoluiu para uma abordagem mais assertiva e, em alguns casos, agressiva em suas relações internacionais.

A diplomacia da China é amplamente baseada em princípios como a soberania nacional, não intervenção, e o respeito à integridade territorial. No entanto, a China também tem sido acusada de usar sua influência econômica para exercer pressão sobre outros países, especialmente aqueles que dependem de seus investimentos e comércio.

A questão de Taiwan é um exemplo claro dessa abordagem. A China considera Taiwan uma província rebelde e tem pressionado continuamente a comunidade internacional para não reconhecer a independência da ilha. A recente escalada de tensões entre a China e Taiwan, incluindo exercícios militares e retórica agressiva, demonstra a disposição da China em usar todos os meios à sua disposição para alcançar seus objetivos geopolíticos.

4. Relações com os Estados Unidos e o Ocidente

As relações entre a China e os Estados Unidos são talvez o aspecto mais crítico da geopolítica global contemporânea. As duas nações estão envolvidas em uma competição multifacetada, que abrange economia, tecnologia, ideologia e influência global.

Nos últimos anos, essa relação se deteriorou, com disputas comerciais, sanções, e uma crescente rivalidade em áreas como 5G, inteligência artificial, e biotecnologia. A chamada "guerra comercial" entre os Estados Unidos e a China revelou as profundas desconfianças mútuas e a luta por supremacia tecnológica.

Além disso, a China tem buscado alternativas ao sistema financeiro dominado pelos EUA, promovendo o uso do yuan em transações internacionais e criando instituições financeiras próprias, como o Banco Asiático de Investimento em Infraestrutura (AIIB). Isso reflete uma tentativa de diminuir a dependência do dólar americano e criar uma ordem financeira global mais multipolar.

5. A Iniciativa do Cinturão e Rota (BRI)

Uma das peças centrais da estratégia geopolítica da China é a Iniciativa do Cinturão e Rota (BRI), lançada em 2013. Este projeto ambicioso visa conectar a Ásia, Europa, África e além através de redes de infraestrutura, comércio e investimentos. O BRI não é apenas um projeto econômico; é uma ferramenta de poder brando que permite à China expandir sua influência em regiões-chave.

Os críticos da BRI argumentam que ela pode levar à armadilha da dívida para os países participantes, criando dependências econômicas e políticas da China. Por outro lado, os defensores veem o BRI como uma oportunidade para o desenvolvimento de infraestrutura em regiões carentes e uma maneira de integrar a economia global de maneira mais equitativa.

6. Desafios Internos e Limitações da Ascensão Chinesa

Apesar de seu crescimento impressionante, a China enfrenta uma série de desafios internos que podem limitar sua ascensão geopolítica. Problemas como a desigualdade social, a corrupção, a degradação ambiental, e o envelhecimento da população representam obstáculos significativos para o futuro do país.

Além disso, o modelo de governança autoritário da China, sob a liderança do Partido Comunista, tem gerado tensões tanto internas quanto externas. A repressão em Xinjiang, Hong Kong, e contra dissidentes internos levanta questões sobre os direitos humanos e a estabilidade social.

7. Implicações Globais da Ascensão Chinesa

A ascensão da China tem implicações globais que vão além de suas fronteiras. Ela desafia a ordem internacional estabelecida, liderada pelos Estados Unidos e baseada em princípios como democracia, direitos humanos, e livre mercado.

Países ao redor do mundo estão ajustando suas políticas para lidar com uma China mais assertiva. Na Ásia, nações como o Japão, a Índia, e a Austrália têm reforçado suas alianças, particularmente com os Estados Unidos, para conter o avanço chinês. Na Europa, há um debate crescente sobre como equilibrar os interesses econômicos com a necessidade de proteger valores democráticos frente à influência chinesa.

Conclusão

A ascensão da China é um dos eventos geopolíticos mais significativos do século XXI. Sua transformação de uma economia em desenvolvimento para uma superpotência global está remodelando a ordem internacional de maneiras complexas e imprevisíveis. À medida que a China continua a expandir sua influência, o mundo deve se adaptar a uma nova realidade em que o equilíbrio de poder global é cada vez mais multipolar e contestado.
"""


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

@app.route('/')
def index():
    return 'Servidor Flask com LSTM está rodando!'

if __name__ == '__main__':
    # Treina o modelo ao iniciar o servidor
    treinar_modelo(text)
    app.run(host='0.0.0.0', debug=True)
