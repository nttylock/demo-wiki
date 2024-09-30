from flask import Flask, request, jsonify, render_template
import cohere
from weaviate import Client
from weaviate.auth import AuthApiKey

app = Flask(__name__)

# Добавьте ваш Cohere API ключ
cohere_api_key = "UT5M7dUrk6ZHAYCxsSQ5AoLLXNtjuAxNrIIHshGt"

co = cohere.Client(cohere_api_key)

# Подключаемся к демонстрационной базе данных Weaviate, содержащей 10 млн векторов Википедии
auth_config = AuthApiKey(api_key="76320a90-53d8-42bc-b41d-678647c6672e")
client = Client(
    url="https://cohere-demo.weaviate.network/",
    auth_client_secret=auth_config,
    additional_headers={
        "X-Cohere-Api-Key": cohere_api_key,
    }
)

def keyword_search(query, results_lang='en', num_results=3):
    """
    Выполняет поиск по базе данных Википедии с использованием векторного поиска и фильтрации по языку.
    """
    properties = ["title", "url", "lang", "text", "_additional {distance}"]

    # Фильтр по языку
    where_filter = {
        "path": ["lang"],
        "operator": "Equal",
        "valueText": results_lang
    }

    # Запрос с использованием векторного поиска
    response = (
        client.query.get("Articles", properties)
        .with_near_text({
            "concepts": [query],
            "distance": 0.2  # Чем меньше значение, тем ближе результаты к запросу
        })
        .with_where(where_filter)
        .with_limit(num_results)
        .do()
    )

    if 'errors' in response:
        print("Ошибка в ответе:", response['errors'])
        return []

    result = response['data']['Get']['Articles']
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')
    results = keyword_search(query)
    return jsonify(results)

@app.route('/api/search', methods=['POST'])
def api_search():
    data = request.json
    query = data.get('query')
    results_lang = data.get('results_lang', 'en')
    num_results = data.get('num_results', 3)
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    results = keyword_search(query, results_lang, num_results)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)