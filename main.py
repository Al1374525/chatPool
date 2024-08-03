import json
from difflib import get_close_matches

#loadd the knowledge base
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


#Next we want to save the dictionary into the knowledge base
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


#we want to have a function that finds the best
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

#we want to get the best answer available
def get_best_answer(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]


#main script
def chat_bot():
    knowledge_base: dict = load_knowledge_base("knowledge_base.json")

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

       # Corrected list comprehension
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])


        if best_match:
            answer: str = get_best_answer(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Thank you! i've learned a new response! ")

if __name__=='__main__':
    chat_bot()