import json
import os

class FileManager:
    history_path = 'watch-history.json'
    last_processed_history_path = 'last-processed-history.json'
    processed_history_path = 'processed-history.json'

    @staticmethod
    def load_history():
        try:
            with open(FileManager.history_path, 'r') as file:
                return json.load(file)
        except:
            return []
    
    @staticmethod
    def load_last_processed_history():
        try:
            with open(FileManager.last_processed_history_path, 'r') as file:
                return json.load(file)
        except:
            return -1
        
    @staticmethod
    def save_last_processed_history(index):
        with open(FileManager.last_processed_history_path, 'w') as file:
            json.dump(index, file)
    
    @staticmethod
    def load_processed_history():
        try:
            with open(FileManager.processed_history_path, 'r') as file:
                return json.load(file)
        except:
            return []

    @staticmethod
    def save_processed_history(processed_history):
        with open(FileManager.processed_history_path, 'w') as file:
            json.dump(processed_history, file)