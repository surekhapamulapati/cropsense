from flask import Flask, render_template, request, jsonify
import json, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

LANG_DIR = os.path.join(os.path.dirname(__file__), 'translations')

def load_language(lang):
    path = os.path.join(LANG_DIR, f"{lang}.json")
    if not os.path.exists(path):
        path = os.path.join(LANG_DIR, "en.json")  # Fallback to English
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Market prices for crops
MARKET_PRICES = {
    'en': {
        'rice': {'fresh': '₹40/kg', 'moderate': '₹25/kg', 'spoiled': '₹8/kg'},
        'wheat': {'fresh': '₹35/kg', 'moderate': '₹20/kg', 'spoiled': '₹7/kg'},
        'corn': {'fresh': '₹30/kg', 'moderate': '₹18/kg', 'spoiled': '₹5/kg'},
        'potato': {'fresh': '₹25/kg', 'moderate': '₹15/kg', 'spoiled': '₹5/kg'},
        'tomato': {'fresh': '₹30/kg', 'moderate': '₹20/kg', 'spoiled': '₹7/kg'},
        'onion': {'fresh': '₹20/kg', 'moderate': '₹12/kg', 'spoiled': '₹4/kg'},
        'cabbage': {'fresh': '₹18/kg', 'moderate': '₹12/kg', 'spoiled': '₹5/kg'},
        'carrot': {'fresh': '₹28/kg', 'moderate': '₹18/kg', 'spoiled': '₹6/kg'},
        'brinjal': {'fresh': '₹22/kg', 'moderate': '₹14/kg', 'spoiled': '₹5/kg'},
        'cauliflower': {'fresh': '₹35/kg', 'moderate': '₹22/kg', 'spoiled': '₹8/kg'},
        'default': {'fresh': '₹30/kg', 'moderate': '₹18/kg', 'spoiled': '₹6/kg'}
    },
    'te': {
        'rice': {'fresh': '₹40/kg', 'moderate': '₹25/kg', 'spoiled': '₹8/kg'},
        'wheat': {'fresh': '₹35/kg', 'moderate': '₹20/kg', 'spoiled': '₹7/kg'},
        'corn': {'fresh': '₹30/kg', 'moderate': '₹18/kg', 'spoiled': '₹5/kg'},
        'potato': {'fresh': '₹25/kg', 'moderate': '₹15/kg', 'spoiled': '₹5/kg'},
        'tomato': {'fresh': '₹30/kg', 'moderate': '₹20/kg', 'spoiled': '₹7/kg'},
        'onion': {'fresh': '₹20/kg', 'moderate': '₹12/kg', 'spoiled': '₹4/kg'},
        'cabbage': {'fresh': '₹18/kg', 'moderate': '₹12/kg', 'spoiled': '₹5/kg'},
        'carrot': {'fresh': '₹28/kg', 'moderate': '₹18/kg', 'spoiled': '₹6/kg'},
        'brinjal': {'fresh': '₹22/kg', 'moderate': '₹14/kg', 'spoiled': '₹5/kg'},
        'cauliflower': {'fresh': '₹35/kg', 'moderate': '₹22/kg', 'spoiled': '₹8/kg'},
        'default': {'fresh': '₹30/kg', 'moderate': '₹18/kg', 'spoiled': '₹6/kg'}
    },
    'hi': {
        'rice': {'fresh': '₹40/kg', 'moderate': '₹25/kg', 'spoiled': '₹8/kg'},
        'wheat': {'fresh': '₹35/kg', 'moderate': '₹20/kg', 'spoiled': '₹7/kg'},
        'corn': {'fresh': '₹30/kg', 'moderate': '₹18/kg', 'spoiled': '₹5/kg'},
        'potato': {'fresh': '₹25/kg', 'moderate': '₹15/kg', 'spoiled': '₹5/kg'},
        'tomato': {'fresh': '₹30/kg', 'moderate': '₹20/kg', 'spoiled': '₹7/kg'},
        'onion': {'fresh': '₹20/kg', 'moderate': '₹12/kg', 'spoiled': '₹4/kg'},
        'cabbage': {'fresh': '₹18/kg', 'moderate': '₹12/kg', 'spoiled': '₹5/kg'},
        'carrot': {'fresh': '₹28/kg', 'moderate': '₹18/kg', 'spoiled': '₹6/kg'},
        'brinjal': {'fresh': '₹22/kg', 'moderate': '₹14/kg', 'spoiled': '₹5/kg'},
        'cauliflower': {'fresh': '₹35/kg', 'moderate': '₹22/kg', 'spoiled': '₹8/kg'},
        'default': {'fresh': '₹30/kg', 'moderate': '₹18/kg', 'spoiled': '₹6/kg'}
    }
}

# AI responses
AI_RESPONSES = {
    'en': {
        'greeting': "Hello! How can I assist you today with your crops or farming?",
        'info_fresh': "Fresh crops are in optimal condition. Keep good storage practices.",
        'info_moderate': "Moderate freshness suggests you should check storage or sell soon.",
        'info_spoiled': "Spoiled crops should be discarded immediately to avoid contamination.",
        'default': "I can provide information on crop freshness, market prices, or general farming queries.",
        'market_intro': "Here are the current market prices for crops based on their status"
    },
    'te': {
        'greeting': "నమస్కారం! ఈ రోజు మీ పంటల లేదా వ్యవసాయంతో నేను మీకు ఎలా సహాయం చేయగలను?",
        'info_fresh': "తాజా పంటలు అత్యుత్తమ పరిస్థితిలో ఉన్నాయి. మంచి నిల్వ పద్ధతులను కొనసాగించండి.",
        'info_moderate': "మధ్యస్థ తాజాదనం అంటే నిల్వ పరిస్థితులను తనిఖీ చేయండి లేదా త్వరలో విక్రయించండి.",
        'info_spoiled': "కలుషితం కాకుండా ఉండటానికి చెడిపోయిన పంటలను వెంటనే పారవేయాలి.",
        'default': "నేను పంట తాజాదనం, మార్కెట్ ధరలు లేదా సాధారణ వ్యవసాయ సమాచారాన్ని అందించగలను.",
        'market_intro': "పంటల స్థితి ఆధారంగా మార్కెట్ ధరలు ఇవి"
    },
    'hi': {
        'greeting': "नमस्ते! मैं आज आपकी फसल या खेती से संबंधित किसी भी प्रश्न में कैसे मदद कर सकता हूँ?",
        'info_fresh': "ताज़ी फसलें इष्टतम स्थिति में हैं। अच्छी भंडारण प्रथाओं को बनाए रखें।",
        'info_moderate': "मध्यम ताज़गी का मतलब है कि भंडारण की स्थिति जाँचें या जल्द बेचें।",
        'info_spoiled': "खराब हुई फसल को तुरंत त्याग दें।",
        'default': "मैं फसल की ताज़गी, बाज़ार कीमतों या सामान्य खेती से संबंधित प्रश्नों की जानकारी प्रदान कर सकता हूँ।",
        'market_intro': "प_Status_ के आधार पर फसलों के वर्तमान बाज़ार मूल्य ये हैं"
    }
}

@app.route('/')
def home():
    lang = request.args.get('lang', 'en')
    content = load_language(lang)
    return render_template('index.html', content=content, lang=lang)

@app.route('/dashboard')
def dashboard():
    lang = request.args.get('lang', 'en')
    content = load_language(lang)

    # Get Firebase config from environment variables
    firebase_config = {
        "apiKey": os.environ.get("FIREBASE_API_KEY"),
        "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN"),
        "databaseURL": os.environ.get("FIREBASE_DB_URL"),
        "projectId": os.environ.get("FIREBASE_PROJECT_ID"),
        "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.environ.get("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.environ.get("FIREBASE_APP_ID"),
        "measurementId": os.environ.get("FIREBASE_MEASUREMENT_ID")
    }

    return render_template('dashboard.html', content=content, lang=lang, firebase_config=firebase_config)

# AI Query Route (general queries)
@app.route('/api/ai_query', methods=['POST'])
def ai_query():
    data = request.json
    user_query = data.get('query', '').lower()
    lang = data.get('lang', 'en')
    status = data.get('status', 'fresh').capitalize()

    response = AI_RESPONSES[lang]['default']

    if any(greet in user_query for greet in ["hello", "hi", "hey"]):
        response = AI_RESPONSES[lang]['greeting']
    elif "freshness" in user_query or "status" in user_query:
        if status == "Fresh":
            response = AI_RESPONSES[lang]['info_fresh']
        elif status == "Moderate":
            response = AI_RESPONSES[lang]['info_moderate']
        elif status == "Spoiled":
            response = AI_RESPONSES[lang]['info_spoiled']
    elif "market" in user_query or "price" in user_query:
        lines = []
        for crop, price_dict in MARKET_PRICES[lang].items():
            if crop == 'default':
                continue
            price_for_status = price_dict.get(status.lower(), price_dict.get('fresh', 'N/A'))
            lines.append(f"{crop.capitalize()} ({status}): {price_for_status}")
        response = f"{AI_RESPONSES[lang]['market_intro']} ({status}):\n" + "\n".join(lines)

    return jsonify({'response': response})

# Market prices API
@app.route('/api/market_prices', methods=['POST'])
def get_market_prices():
    data = request.json
    lang = data.get('lang', 'en')
    status = data.get('status', 'fresh').lower()

    all_prices = {}
    response_lines = []

    for crop, price_dict in MARKET_PRICES[lang].items():
        if crop == 'default':
            continue
        price_for_status = price_dict.get(status, price_dict.get('fresh', 'N/A'))
        all_prices[crop] = price_for_status
        response_lines.append(f"{crop.capitalize()} ({status.capitalize()}): {price_for_status}")

    response_text = f"{AI_RESPONSES[lang]['market_intro']} ({status.capitalize()}):\n" + "\n".join(response_lines)
    return jsonify({'prices': all_prices, 'response_text': response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
