import os
import openai
import json

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")

def write_message_to_file(file_path, role, content):
    with open(file_path, "a") as file:
        message = {"role": role, "content": content.replace('"', '\\"')}
        file.write(json.dumps(message) + "\n")

def read_messages_from_file(file_path):
    with open(file_path, "r") as file:
        return [json.loads(line) for line in file]

def reset_file(file_path):
    with open(file_path, "w") as file:
        file.truncate(0)

file_path = "file.txt"
reset_file(file_path)
total_tokens = 0
exit_loop = False

while not exit_loop:
    user_input = input("输入对话：")
    write_message_to_file(file_path, "user", user_input)

    if user_input == "q":
        exit_loop = True
        continue

    if user_input == "op":
        with open(file_path, "r") as file:
            history = file.read().strip()
        print(history)
        continue

    messages = read_messages_from_file(file_path)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    total_tokens += response['usage']['total_tokens']
    finish_reason = response['choices'][0]['finish_reason']

    if finish_reason == "stop":
        print(f"正常返回，目前总共花费{total_tokens}字节")
    elif finish_reason == "length":
        print("字符最高上限，重开吧")
        exit_loop = True
        continue
    elif finish_reason == "content_filter":
        print("输入了逆天玩意儿被屏蔽了（流汗黄豆）")
        exit_loop = True
        continue
    elif finish_reason == "null":
        print("未知错误")
        exit_loop = True
        continue

    assistant_output = response['choices'][0]['message']['content']
    print(assistant_output)
    write_message_to_file(file_path, "assistant", assistant_output)
