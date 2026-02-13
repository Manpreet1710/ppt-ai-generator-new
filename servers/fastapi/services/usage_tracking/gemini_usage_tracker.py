from os import getenv
import os
from fastapi.responses import JSONResponse
from constants import TOKEN_FOR_DEVELOP
from services.usage_tracking.firestore_usage_service import get_total_available_tokens
from services.usage_tracking.llm_usage_tracker import LLMUsageTracker
from firebase_admin import firestore
from services.usage_tracking.firestore_usage_service import usage_log
from main import get_firestore_client

db = get_firestore_client()


class GeminiUsageTracker(LLMUsageTracker):

    
    def check_usage_limit(input_token_count: int, output_token_count: int,plan,uid) -> bool:
        """
        Check if the user has enough available tokens for the request.

        Returns:
            bool: True if usage is within limit, False otherwise.
        """
        try:
            total_tokens = input_token_count + output_token_count
            mode = "test"
            if mode != "test" :
                available_tokens = get_total_available_tokens(uid,plan,doc_name="user_usage")
                return total_tokens <= available_tokens
            else:
                return TOKEN_FOR_DEVELOP
        except LookupError:
            # Context not set properly
            return False
        except Exception as e:
            # Optional: log the error
            return False

   
    def update_llm_usage_from_response(doc_name, uid, response, llm_name, model_name,email,plan):
        model_name = model_name.replace(".", "-")  # Replace dots to avoid nesting issues
        try:
            # --- Extract tokens ---
            if llm_name.lower() == "openai":
                input_tokens = response["usage"]["prompt_tokens"]
                output_tokens = response["usage"]["completion_tokens"]
            elif llm_name.lower() == "gemini":
                usage_meta = response.usage_metadata
                input_tokens = usage_meta.get("input_tokens")
                output_tokens = usage_meta.get("output_tokens")
            elif llm_name.lower() == "claude":
                input_tokens = response["usage"]["input_tokens"]
                output_tokens = response["usage"]["output_tokens"]
            else:
                raise ValueError(f"LLM '{llm_name}' not supported")

            total_tokens = input_tokens + output_tokens

            # --- Get Firestore document ---
            user_ref = db.collection(doc_name).document(uid)
            user_doc = user_ref.get()
            user_data = user_doc.to_dict() or {}

            # Check if llm_usage.llm_name.model_name exists
            llm_models = user_data.get("llm_usage", {}).get(llm_name, {})
            model_exists = model_name in llm_models

            if model_exists:
                # ✅ Safe to use update
                user_ref.update({
                    f"llm_usage.{llm_name}.{model_name}.requests": firestore.Increment(1),
                    f"llm_usage.{llm_name}.{model_name}.tokens_used": firestore.Increment(total_tokens)
                })
            else:
                # ❌ Fallback: initialize model and set merge=True
                user_ref.set({
                    "llm_usage": {
                        llm_name: {
                            model_name: {
                                "requests": 1,
                                "tokens_used": total_tokens
                            }
                        }
                    }
                }, merge=True)

            usage_log(uid,email,llm_name,model_name,total_tokens,input_tokens,output_tokens,plan,"success","usage_logs")

        except Exception as e:
            print(f"Error updating usage for {uid}: {e}")
            return JSONResponse(content={"error": str(e)}, status_code=500)