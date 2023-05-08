from typing import Callable, Dict, List, Optional, Union
import json
from difflib import get_close_matches

# knowledge_base_service.py
class KnowledgeBaseService:
 
    def _load_knowledge_base(self, file_name: str) -> List[Dict[str, str]]:
        try:
            with open(file_name, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_knowledge_base(self, file_name: str, knowledge_base: List[Dict[str, str]]) -> None:
        with open(file_name, "w") as f:
            json.dump(knowledge_base, f, indent=2)

    def _ask_question(self, knowledge_base: List[Dict[str, str]], question: str, max_matches: int = 1) -> str:
        questions = [item["question"] for item in knowledge_base]
        close_matches = get_close_matches(
            question, questions, n=max_matches, cutoff=0.6)
        if close_matches:
            matched_question = close_matches[0]
            for item in knowledge_base:
                if item["question"] == matched_question:
                    return item["answer"]
        else:
            return "I don't know the answer to that question. Please provide the answer."

    def _learn_answer(self, knowledge_base: List[Dict[str, str]], question: str, answer: str) -> None:
        knowledge_base.append({"question": question, "answer": answer})

    # can only be used with chatbot_client
    def chat_with_knowledge_base(self, knowledge_base_file: str) -> None:
        knowledge_base = self._load_knowledge_base(knowledge_base_file)

        while True:
            question = input("Ask me a question or type 'exit' to stop: ")
            if question.strip().lower() == 'exit':
                break

            answer = self._ask_question(knowledge_base, question)
            if answer.startswith("I don't know"):
                print(answer)
                new_answer = input("Answer: ")
                self._learn_answer(knowledge_base, question, new_answer)
                self._save_knowledge_base(knowledge_base_file, knowledge_base)
            else:
                print("Answer:", answer)