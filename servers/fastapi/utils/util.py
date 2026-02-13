 
# import hashlib
# import hmac
# import json
# import os
# import re
# # from langchain_google_genai import ChatGoogleGenerativeAI
# # from langchain.chat_models import ChatOpenAI
# from models.seo_tools.people_also_ask_tool_schema import PeopleAlsoAskResponse
# from langchain_core.language_models import BaseLanguageModel
# import json
# import re
# from fastapi import Header, HTTPException
# from dotenv import load_dotenv
# load_dotenv()
# import tiktoken

# CRON_SECRET_KEY=os.getenv("CRON_SECRET_KEY","default_secret")
# _llm_cache = {}
# def parse_model_response(response_content: str) -> PeopleAlsoAskResponse:
#     # Step 1: Strip triple backticks and optional `json` label
#     cleaned = re.sub(r"^```json\s*|\s*```$", "", response_content.strip(), flags=re.IGNORECASE)
#     try:
#         data = json.loads(cleaned)
#         return data
#     except json.JSONDecodeError as e:
#         raise ValueError(f"Failed to decode JSON: {e}")

# def format_list_string(response_content: any) -> list[str]:
#     """
#     Extracts and cleans list items from a string, removing leading numbers and whitespace.
#     """
#     return [
#         re.sub(r'^\d+\.\s*', '', line.strip())
#         for line in response_content.splitlines()
#         if line.strip()
#     ]
     
# # def get_Gemini_llm(self, model_name: str,api_key:str) -> ChatGoogleGenerativeAI:
# #         """
# #         Get or create LLM instance for the specified model.
# #         Uses caching to avoid recreating the model multiple times.
# #         """
# #         if model_name not in self._llm_cache:
# #             self._llm_cache[model_name] = ChatGoogleGenerativeAI(
# #                 model=model_name,
# #                 google_api_key=api_key
# #             )
# #         return self._llm_cache[model_name]


# # def get_openai_llm(api_key: str, model_name: str, temperature: float = 0.7) -> ChatOpenAI:
# #     """
# #     Reusable function to get a cached ChatOpenAI instance.

# #     Args:
# #         api_key (str): OpenAI API key
# #         model_name (str): Model name (e.g., 'gpt-4', 'gpt-3.5-turbo')
# #         temperature (float): Sampling temperature (0.0–1.0). Default: 0.7

# #     Returns:
# #         ChatOpenAI: Cached or newly created instance
# #     """
# #     cache_key = f"{model_name}:{temperature}"
# #     if cache_key not in _llm_cache:
# #         _llm_cache[cache_key] = ChatOpenAI(
# #             model_name=model_name,
# #             openai_api_key=api_key,
# #             temperature=temperature
# #         )
# #     return _llm_cache[cache_key]


# def clean_and_parse_result(raw_result):
#     # Remove markdown code block wrapper
#     cleaned = re.sub(r"^```json\n|```$", "", raw_result.strip(), flags=re.MULTILINE)
#     return json.loads(cleaned)



# def get_token_count(prompt: str, llm: BaseLanguageModel, model_name: str = "") -> int:
#     """
#     Generic function to get input token count for a given prompt and LLM.
#     Tries to use model-specific tokenizer if available, otherwise falls back to estimation.
    
#     Args:
#         prompt (str): The input text prompt.
#         llm (BaseLanguageModel): The LLM instance.
#         model_name (str): Optional model name string for manual tokenizer selection.
        
#     Returns:
#         int: Estimated number of tokens in the prompt.
#     """
    
#     # ✅ 1. If Langchain LLM has native tokenizer support
#     if hasattr(llm, "get_num_tokens") and callable(getattr(llm, "get_num_tokens")):
#         try:
#             return llm.get_num_tokens(prompt)
#         except Exception:
#             pass  # Fallback below if tokenizer fails

#     # ✅ 2. Fallback based on model_name
#     model_name = model_name.lower()

#     # -- OpenAI GPT models --
#     if "gpt" in model_name:
#         try:
#             encoding = tiktoken.encoding_for_model(model_name)
#             return len(encoding.encode(prompt))
#         except Exception:
#             return int(len(prompt.split()) * 1.3)  # fallback

#     # -- Claude (Anthropic) models --
#     elif "claude" in model_name:
#         return len(prompt.split())  # Claude token ~= word

#     # -- Gemini or PaLM --
#     elif "gemini" in model_name or "palm" in model_name:
#         return int(len(prompt.split()) * 1.3)

#     # -- Mistral, LLaMA, or other tiktoken-compatible open models --
#     elif any(x in model_name for x in ["mistral", "llama", "mixtral", "zephyr"]):
#         try:
#             encoding = tiktoken.get_encoding("cl100k_base")
#             return len(encoding.encode(prompt))
#         except:
#             return int(len(prompt.split()) * 1.3)

#     # ✅ 3. Universal fallback
#     return int(len(prompt.split()) * 1.3)

# def get_estimated_output_token(input_tokens: int, ratio: float = 1.5) -> int:
#         """
#         Estimate output token count based on input tokens.
        
#         Args:
#             input_tokens: Number of input tokens
#             ratio: Estimated output-to-input ratio (default 1.5)
            
#         Returns:
#             int: Estimated output token count
#         """
#         return int(input_tokens * ratio)


# def verify_hmac(secret: str, token: str, message: str = "fixed-api-key") -> bool:
#     """Verify HMAC token against expected signature."""
#     expected = hmac.new(
#         secret.encode(),
#         message.encode(),
#         hashlib.sha256
#     ).hexdigest()
#     return hmac.compare_digest(expected, token)

# def authenticate(x_api_token: str = Header(None)):
#     if not x_api_token:
#         raise HTTPException(status_code=401, detail="Missing token or timestamp")
    
#     if not verify_hmac(CRON_SECRET_KEY, x_api_token):
#         print("CRON SECRET KEY"+CRON_SECRET_KEY)
#         raise HTTPException(status_code=401, detail="Invalid token")

#     return "authorized"

