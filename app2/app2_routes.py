from flask import render_template, request, jsonify, Blueprint
import google.generativeai as genai
import markdown,os
from dotenv import load_dotenv

load_dotenv()

app2 = Blueprint('app2', __name__, template_folder='templates')

# Configure Generative AI
generation_config = {
    "temperature": 0.3,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Set your API key for Generative AI


genai.configure(api_key=os.getenv('GEMINI_API_KEY'))



model = genai.GenerativeModel('gemini-1.0-pro', generation_config=generation_config, safety_settings=safety_settings)

def generate(prompt):
    template = [
        f'''Act like a psychiatrist and insomnia specialist. Create a proper sleep schedule based on the daily lifestyle pattern provided here:
        {prompt}

        Create an efficient sleep schedule based on the daily lifestyle pattern provided. Keep in mind that the person needs at least 6-8 hours of sleep every day. It is good if the sleep time is mostly at night, and without break. If not possible, then suggest slightly different schedule but keep the key points in mind and try to maximize the health benefits. If the pattern provided is not likely a lifestyle pattern of something out of context, say "I am here to provide you your healthy trip to your sleep. Please provide me your lifestyle so that I can make it easy for you." From the pattern provided also try to detect if the person has any kind of Insomnia or not. If there is any, explain what kind of Insomnia the person has and what are the remedies. And if not, then suggest the healthy lifestyle.
        '''
    ]
    response = model.generate_content(template)
    return markdown.markdown(response.text)

@app2.route('/')
def sleeptrip():
    return render_template('index3.html')

@app2.route('/upload', methods=['POST'])
def upload():
    schedule = request.form.get('lifestyle-pattern')
    if schedule:
        res = generate(schedule)
        return render_template('index3.html', result=res)
    return render_template('index3.html', result="Error: Not Generated")
