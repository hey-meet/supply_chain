import os
import json

class KnowledgeBaseManager:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(current_dir, "knowledge_base.json")

    def get_all_assets(self):
        with open(self.file_path, "r") as file:
            return json.load(file)

kb_manager = KnowledgeBaseManager()