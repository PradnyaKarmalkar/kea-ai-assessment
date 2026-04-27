import google.generativeai as genai

genai.configure(api_key="AIzaSyCnfdmIg7R3nb6qXTX2yQ3Pbm2cFH4LFGk")

models = genai.list_models()

for m in models:
    print(m.name, "→", m.supported_generation_methods)