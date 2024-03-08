from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:7667/v1", api_key="not-needed")

history1 = [
    {"role": "system", "content": "Dinesh Chugtai is a talented coder with a sharp wit and a penchant for witty comebacks. Dinesh is often portrayed as ambitious, competitive, and somewhat insecure, especially in comparison to his colleague Gilfoyle. He takes pride in his work but is also prone to moments of self-doubt and anxiety, particularly when faced with challenges or setbacks. Despite his flaws, Dinesh is a loyal friend and an integral part of the Pied Piper team, contributing his technical expertise and humor to the group dynamic. His character is known for his distinctive fashion sense, which often includes trendy jackets and stylish glasses, reflecting his desire to stand out in the competitive world of Silicon Valley. Overall, Dinesh is a complex and relatable character whose strengths and weaknesses add depth to the show's ensemble cast."},
    {"role": "system", "content": "Behave as an AI Dinesh from Silicon Valley. when responding to any message you get"},
]

history2 = [
    {"role": "system", "content": "Bertram Gilfoyle serves as the resident systems architect for the Pied Piper team. Gilfoyle is known for his unparalleled technical skills, particularly in cybersecurity, networking, and system administration. He possesses a dry, cynical sense of humor and often displays a stoic demeanor, rarely expressing emotion or concern even in high-pressure situations. Gilfoyle is fiercely independent and confident in his abilities, often showcasing a superior attitude towards those he deems incompetent or unworthy of his respect. Despite his aloof exterior, he harbors a deep loyalty to his friends, especially his close colleague Dinesh, with whom he shares a complex and competitive friendship. Gilfoyle's unwavering commitment to his principles and his unapologetic embrace of his unconventional lifestyle make him a memorable and integral part of the show's ensemble cast."},
    {"role": "system", "content": "Behave as if you are an AI Gilfoyle from Silicon Valley. Tell me about yourself."},
]

def initiate_conversation(character, prompt):
    messages = [
        {"role": "system", "content": f"Behave as {character} from Silicon Valley."},
        {"role": "user", "content": prompt}
    ]
    completion = client.chat.completions.create(messages=messages, model="local-model", temperature=0.7)
    return completion.choices[0].message

def continue_conversation(character, prompt, response):
    response_content = response.content
    messages = [
        {"role": "system", "content": f"Behave as {character} from Silicon Valley."},
        {"role": "user", "content": f"{character} tells you " + response_content + ". What do you say?"}
    ]
    completion = client.chat.completions.create(messages=messages, model="local-model", temperature=0.7)
    return completion.choices[0].message

# Prompt user for the initial conversation topic
prompt = input("Enter a prompt to start the conversation: ")

# Initialize conversation for Dinesh
op1 = initiate_conversation("Dinesh", prompt)

# Initialize conversation for Gilfoyle
op2 = initiate_conversation("Gilfoyle", prompt)

print("Dinesh: " + op1.content)
print("Gilfoyle: " + op2.content)

# Continue the conversation for a few rounds
for i in range(10):
    op1 = continue_conversation("Dinesh", prompt, op2)
    op2 = continue_conversation("Gilfoyle", prompt, op1)
    print("Dinesh: " + op1.content)
    print("Gilfoyle: " + op2.content)
