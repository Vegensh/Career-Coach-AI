import requests
import logging

class AIAssistant:
    def __init__(self, ollama_url="http://localhost:11434/api/generate", model_name="llama2:7b"):
        """
        Initialize the AI Assistant with the Ollama server URL and the model to use.
        """
        self.ollama_url = ollama_url
        self.model_name = model_name

    def get_smart_response(self, user_input, career_details, user_profile=None):
        """
        Sends a prompt to the Ollama AI model and returns a concise, helpful response.

        Parameters:
            user_input (str): The user's question or message.
            career_details (str): The relevant career info to assist the AI response.
            user_profile (dict): Optional; user profile or context to personalize response.

        Returns:
            str: The AI-generated answer or fallback to career details if error occurs.
        """

        # Build a clear prompt for the AI model
        prompt = (
            f"You are an expert AI career advisor.\n"
            f"User asked: {user_input}\n\n"
            f"Here are relevant career details:\n{career_details}\n\n"
            f"Please provide a clear and concise answer to the user's question based on the facts above."
        )

        # If you want, you could append user_profile info to the prompt here

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False  # Set True if you want streaming responses (handle differently)
        }

        try:
            logging.debug(f"Sending request to Ollama with payload: {payload}")
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            response.raise_for_status()
            res_json = response.json()

            # Expected JSON structure: {"response": "AI answer text"}
            ai_answer = res_json.get("response", "").strip()

            if not ai_answer:
                logging.warning("Received empty response from Ollama AI.")
                return career_details  # fallback

            return ai_answer

        except requests.exceptions.RequestException as e:
            logging.error(f"Ollama server request failed: {e}")
            # Could also return a user-friendly fallback message here
            return f"Sorry, I am having trouble reaching the AI service right now.\nHere is the info I have:\n{career_details}"

        except ValueError as e:
            logging.error(f"Error parsing JSON response from Ollama: {e}")
            return career_details


# ------------------------
# Example usage (for testing only):
# ------------------------
if __name__ == "__main__":
    assistant = AIAssistant()
    user_question = "What is the average salary for a Data Scientist?"
    sample_career_info = "Data Science & AI: Fresher salary ₹4-12 LPA, Experienced ₹12-60 LPA."
    print(assistant.get_smart_response(user_question, sample_career_info))
