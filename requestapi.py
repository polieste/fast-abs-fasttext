import os
import json
 
def find_txt_files(path):
    txt_files = []
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isdir(file_path):
            # nếu đường dẫn là một thư mục, đệ quy tìm kiếm các file .txt bên trong
            txt_files.extend(find_txt_files(file_path))
        elif filename.endswith('.txt'):
            # nếu đường dẫn là một file và có đuôi là .txt, mở
            txt_files.append(file_path)
    return txt_files

# sử dụng hàm find_txt_files để tìm các file .txt trong thư mục hiện tại
txt_files = find_txt_files('/content/drive/MyDrive/KLTN/result')

def read_file(file_path):
  with open(file_path, 'r') as file:
      content = file.read()
  return content

import jsonlines

filename = "/content/drive/MyDrive/KLTN/jsonl/example_requests_to_parallel_process.jsonl"
n_requests = len(txt_files)

with jsonlines.open(filename, mode='w') as writer:
    for i in range(n_requests):
        job = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant in in summarizing texts in Vietnamese."},
                {"role": "user", "content": "Tóm tắt văn bản sau bằng tiếng việt trong vòng không quá 3 câu: " + read_file(txt_files[i])}
            ]
        }
        writer.write(job)
        print('Processing articles number:', i)

# filename = "/content/drive/MyDrive/KLTN/jsonl/example_requests_to_parallel_process.jsonl"
# n_requests = len(txt_files)
# for i in range (n_requests):
#   jobs = [{
#     "model": "gpt-3.5-turbo",
#     "messages": [{"role": "system", "content": "You are a helpful assistant in in summarizing texts in Vietnamese."},
#                 {"role": "user", "content": "Tóm tắt văn bản sau bằng tiếng việt trong vòng không quá 3 câu: " + read_file(txt_files[i])}
#                 ]
#   }]
#   with open(filename + ".jsonl", "w") as f:
#       for job in jobs:
#           json_string = json.dumps(job)
#           f.write(json_string + "\n")
#   print('Processing articles number:', i)