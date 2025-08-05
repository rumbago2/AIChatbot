from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    # Inicializa chat y estado
    self.chat_history = []
    self.chat_display.content = ""
    self.status_label.text = ""
    self.status_label.visible = False

  def submitllm_click(self, **event_args):
    self._handle_prompt_submission()

  def user_prompt_pressed_enter(self, **event_args):
    self._handle_prompt_submission()

  def llm_name_change(self, **event_args):
    """Borra el historial de chat al cambiar de modelo"""
    self.chat_history = []
    self.chat_display.content = ""
    self.status_label.text = f"🧠 Switched model to: {self.llm_name.selected_value}"
    print(f"🔄 Model changed to: {self.llm_name.selected_value}")

  def _handle_prompt_submission(self):
    """Envía el prompt al LLM y actualiza el historial."""
    try:
      user_prompt = self.user_prompt.text.strip()
      llm_name = self.llm_name.selected_value

      if not user_prompt or not llm_name:
        alert("The prompt and LLM model cannot be empty.", title="Input Error")
        return

      pl = int(self.petal_length.text) if self.petal_length.text else 0
      pw = self.petal_width.text if self.petal_width.text else ""

    except ValueError:
      alert("Option should be integer and session name text.", title="Input Error")
      return

    self.status_label.visible = True
    self.status_label.text = "🤖 Generating response, please wait..."
    self.submitllm.enabled = False

    try:
      result = anvil.server.call('ask_llm', user_prompt, llm_name, pl, pw, self.chat_history)

      if "error" in result:
        self.status_label.text = f"❌ Error from backend: {result['error']}"
      else:
        self.chat_history = result['updated_chat_history']
        self._update_chat_display()
        self.status_label.text = f"✅ Response received. Tokens used: {result['tokens_used']}"
        self.user_prompt.text = ""

    except Exception as e:
      self.status_label.text = f"❌ Unexpected error: {e}"
      print(f"❌ Exception during server call: {e}")

    finally:
      self.submitllm.enabled = True
      self.user_prompt.focus()

  def _update_chat_display(self):
    """Renderiza el historial de conversación en el componente RichText."""
    formatted_chat = ""
    for turn in self.chat_history:
      role = turn['role'].capitalize()
      content = "\n".join(turn['parts'])
      if role == 'User':
        formatted_chat += f"**You:**\n{content}\n\n"
      else:
        formatted_chat += f"**🤖 Model:**\n{content}\n\n"

    self.chat_display.content = formatted_chat
    self.call_js('scrollRichTextToBottom', self.chat_display)

  def clear_button_click(self, **event_args):
    """Reinicia la conversación."""
    self.chat_history = []
    self.user_prompt.text = ""
    self.chat_display.content = ""
    self.status_label.text = "🗑️ Chat cleared."
    print("Chat history cleared.")

  def show_history_button_click(self, **event_args):
    """This method is called when the user clicks the 'Show History' button."""
    self.status_label.visible = True
    self.status_label.text = "⏳ Fetching history from database..."
    try:
    # Call the backend function with action_flag = 2
      result = anvil.server.call('ask_llm',
                               user_prompt=None,
                               llm_name=None,
                               action_flag=2,
                               session_name=None,
                               chat_history=None)

      if result and "error" in result:
       print(f"CLIENT: Server returned error: {result['error']}")
       self.status_label.text = f"❌ Error: {result['error']}"
       alert(f"Could not load history: {result['error']}")
      else:
        #self.history_grid.items = result['data']
        #self.history_grid.items = [{'session_name': 'TEST12', 'llm_name': 'deepseek', 'first_prompt': 'what is the model name and ID answering this prompt?'}]
        #self.history_grid.items = [{'session_name': 'sesion1', 'llm_name': 'mistral','first_prompt': 'my prompt'}, {'session_name': 'sesion2', 'llm_name': 'deepseek','first_prompt': 'my prompt 2'}]
        print("CLIENT: Data assigned to grid:")
        for row in result['data']:
         print(row)
      self.status_label.text = f"✅ Loaded {len(result['data'])} records."
      self.status_label.text = "✅ Chat history:\n" + "\n".join(
        [f"- {row['session_name']} | {row['llm_name']} | {row['first_prompt']}" for row in result["data"]]
      )
    except Exception as e:
      print(f"CLIENT: Exception during server call: {e}")
      self.status_label.text = f"❌ Failed to load data: {e}"
      alert(f"An error occurred: {e}")
    except Exception as e:
      # --- TRACKING LINE 5 (The one that's likely firing) ---
      print(f"CLIENT: The 'anvil.server.call' failed entirely. Exception: ")
      # This is the line that generates your error message
      self.status_label.text = f"❌ Anvil connection error." 
      alert(f"A connection error occurred while communicating with the server. Please check the App Logs for server-side errors. Exception: ")

  # --- BEGIN: Botón para cargar sesión previa por nombre ---
  def load_session_button_click(self, **event_args):
    session_name = self.petal_width.text.strip()  # Cambia esto si usas otro campo para el nombre de sesión
    if not session_name:
      alert("Please enter a session name to load.")
      return
    self.status_label.visible = True
    self.status_label.text = f"⏳ Loading chat history for session: {session_name}..."
    try:
      result = anvil.server.call(
      'ask_llm',
      user_prompt=None,
      llm_name=None,
      action_flag=3,
      session_name=session_name,
      chat_history=None
    )
      #print("CLIENT: Full result from backend:", result)
      if result and "error" in result:
       self.status_label.text = f"❌ Error: {result['error']}"
       alert(f"Could not load chat: {result['error']}")
       return
      if "chat_history" in result:
        self.chat_history = result['chat_history']
        self._update_chat_display()
        self.status_label.text = f"✅ Loaded context with {len(self.chat_history)} turns."
        print("CLIENT: Chat history loaded successfully.")
      else:
        self.status_label.text = "⚠️ No chat history found."
        alert("Session found, but no chat history available.")
    except Exception as e:
      print(f"CLIENT: Exception loading chat history: {e}")
      self.status_label.text = f"❌ Failed to load saved chat: {e}"
      #alert(f"An error occurred while loading the saved session.")
# --- END: Botón para cargar sesión previa ---

  def save_chat_click(self, **event_args):
    session_name = self.petal_width.text.strip()  # O usa otro campo de tu formulario si prefieres
    llm_name = self.llm_name.selected_value

    if not session_name or not llm_name:
      alert("You must enter a session name and select an LLM model before saving.")
      return

    if not self.chat_history:
      alert("There is no chat history to save.")
      return

    self.status_label.visible = True
    self.status_label.text = f"💾 Saving chat session '{session_name}'..."

    try:
      result = anvil.server.call(
      'ask_llm',
      user_prompt=None,
      llm_name=llm_name,
      action_flag=1,
     session_name=session_name,
      chat_history=self.chat_history
      )

      if result and "error" in result:
        self.status_label.text = f"❌ Save failed: {result['error']}"
        alert(f"Could not save chat: {result['error']}")
      else:
        self.status_label.text = f"✅ Chat saved successfully as '{session_name}'"
        print("CLIENT: Chat saved to database.")

    except Exception as e:
      print(f"CLIENT: Exception saving chat history: {e}")
      self.status_label.text = f"❌ Error saving chat: {e}"
      alert("An unexpected error occurred while saving the chat.")