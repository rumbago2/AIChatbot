from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Check if self.item is set (Anvil sets this automatically for each row)
    if self.item:
      self.label_session.text = self.item.get('session_name', 'N/A')
      self.label_llm.text = self.item.get('llm_name', 'N/A')
      self.label_prompt.text = self.item.get('first_prompt', 'N/A')

