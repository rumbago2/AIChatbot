from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server


class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    print(self.item)  # Should print your dictionary to console for each row
    if self.item:
      self.label_session.text = self.item.get('session_name', 'N/A')
      self.label_llm.text = self.item.get('llm_name', 'N/A')
      self.label_prompt.text = self.item.get('first_prompt', 'N/A')
