from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Check if self.item is set (Anvil sets this automatically for each row)
    if self.item is not None:
      self.label_session.text = self.item['session_name']
      self.label_llm.text = self.item['llm_name']
      self.label_prompt.text = self.item['first_prompt']

