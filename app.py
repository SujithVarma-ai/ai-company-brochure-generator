from openai import OpenAI
from dotenv import load_dotenv
import os
import gradio as gr

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

load_dotenv(override=True)

google_api_key = os.getenv("GOOGLE_API_KEY")

if google_api_key:
    print("Google API Key loaded successfully")
else:
    print("Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")

gemini = OpenAI(
    base_url=GEMINI_BASE_URL,
    api_key=google_api_key
)     

system_message = "You are a helpful assistant that provides information about the Gemini models."
def message_gemini(prompt):
    response = gemini.chat.completions.create(
        model="gemini-2.5-flash-lite",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
print(message_gemini("What is today's date?"))  


# website
from scraper import fetch_website_contents

system_message = """
You are an assistant that analyzes the contents of a company website landing page
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
"""
def stream_brochure(company_name, url, model):
    yield ""
    prompt = f"Please generate a company brochure for {company_name}. Here is their landing page:\n"
    prompt += fetch_website_contents(url)
    if model=="Gemini":
        result = message_gemini(prompt)
    else:
        raise ValueError("Unknown model")
    yield result

name_input = gr.Textbox(label="Company name:")
url_input = gr.Textbox(label="Landing page URL including http:// or https://")
model_selector = gr.Dropdown(["Gemini"], label="Select model", value="Gemini")
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=stream_brochure,
    title="Brochure Generator", 
    inputs=[name_input, url_input, model_selector], 
    outputs=[message_output], 
    examples=[
            ["Edward Donner", "https://edwarddonner.com", "Gemini"],
            ["TCS", "https://www.tcs.com", "Gemini"],
            ["Deloitte", "https://www2.deloitte.com/global/en.html", "Gemini"]
        ], 
    )
view.launch()    
