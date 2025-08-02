from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    print("🌐 Client: Form initialized.")

  def submitllm_click(self, **event_args):
    """Called when the button is clicked."""

    try:
      # Read and validate inputs
      user_prompt = self.user_prompt.text.strip()
      llm_name = self.llm_name.selected_value.strip()
      pl = float(self.petal_length.text) if self.petal_length.text else 0.0
      pw = float(self.petal_width.text) if self.petal_width.text else 0.0

      if not user_prompt or not llm_name:
        raise ValueError("Prompt and LLM model must not be empty.")

      print(f"📤 Sending to Colab: prompt='{user_prompt}', model='{llm_name}', extras={pl}, {pw}")
    except Exception as e:
      self.species_label.visible = True
      self.species_label.text = f"Input error: {e}"
      print(f"⚠️ Input error: {e}")
      return

    self.species_label.visible = True
    self.species_label.text = "Generating response, please wait..."

    try:
      result = anvil.server.call('ask_llm', user_prompt, llm_name, pl, pw)
      print("✅ Received response from backend:", result)

      if "error" in result:
        self.species_label.text = f"Error: {result['error']}"
      else:
        response_text = result["response"]
        tokens = result["tokens_used"]
        model = result["model"]

        self.species_label.text = f"LLM ({model}) response:\n\n{response_text}\n\nTokens used: {tokens}"

    except Exception as e:
      self.species_label.text = f"❌ Error during backend call: {e}"
      print(f"❌ Exception: {e}")
