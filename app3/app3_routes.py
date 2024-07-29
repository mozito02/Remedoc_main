from flask import Flask, render_template, request,Blueprint
import textwrap
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, trim_messages
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from operator import itemgetter
import markdown
import os
from dotenv import load_dotenv


load_dotenv()


app3 = Blueprint('app3', __name__, template_folder='templates')

#set your groq api key
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    raise ValueError("No GROQ API Key found. Set the GROQ_API_KEY environment variable.")
chat_model = ChatGroq(model_name='llama3-70b-8192', api_key=groq_api_key)

# Prompt Template
generic_template = '''
    You are a medical assistant. Help the user with medical queries. Give proper suggestions.
'''

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", generic_template),
        ("user", "{message}")
    ]
)

trimmer = trim_messages(
    max_tokens=10000,
    strategy='last',
    token_counter=chat_model,
    include_system=True,
    start_on="human"
)

# Create a chain
chain = (
    RunnablePassthrough.assign(message=itemgetter('messages') | trimmer)
    | prompt
    | chat_model
)

def to_markdown(text):
    text = text.replace('-', '')
    text = text.replace('**', '')
    return textwrap.indent(text, '\n', predicate=lambda _: True)

def chatbot(message):
    messages = [SystemMessage(content='You are a medical assistant. Help the user with medical queries. Give proper suggestions.')]
    res = chain.invoke(
        {'messages': messages + [HumanMessage(content=message)]}
    )
    return to_markdown(res.content)

@app3.route('/')
def medbot():
    return render_template('index4.html')

@app3.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['messageText']
    bot_response = chatbot(user_message)
    return render_template('index4.html', user_message=user_message, bot_response=bot_response)


