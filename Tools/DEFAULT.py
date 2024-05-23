DEFAULT_General_Congig = """
font = "DejaVu Sans"
font_size = 12
current_process_mode = "Pop"
current_listen_mode = "Mixed"
current_mode = "Smart"
lang=en_US
"""

DEFAULT_LLM_Congig = """
APIKEY = ""
llm_model = "llama3"
max_tokens = 4000
temperature = 0.3
endpoint = "http://localhost:11434/v1/chat/completions"
proxies = {}
timeout = 60
max_retry = 3
"""

DEFAULT_Prompts = {
    "Smart": "1# Your responses should be accurate and logical.\n2#When the input is code, you should explain the code in detail using {lang}.\n3#In other cases you should make it accurate, keep the original format, don't leave out any information, and directly output its {lang} translation\n4#If it is already {lang}, the given text is interpreted correctly in detail.",
    "Explain": "Take the input text exactly as it is, keep the original formatting, don't leave out any information, and output its {lang} translation directly.",
    "Translate": "Your response should be accurate and logical, explaining the given text in detail using {lang}.",
}
