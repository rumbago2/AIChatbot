from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server


class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print(self.item)  # Should print your dictionary to console for each row
    if self.item:
      self.repeating_panel_1.items = [{'session_name': 'TEST12', 'llm_name': 'deepseek', 'first_prompt': 'what is the model name and ID answering this prompt?'}]
