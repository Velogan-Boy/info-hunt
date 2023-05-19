import json
import tqdm

def remove_attribute(json_data, attribute):
    if attribute in json_data:
        del json_data[attribute]
    return json_data


file_path = "./articles/indianExp.json"

with open(file_path, "r" ,encoding='utf-8') as file:
    json_data = json.load(file)

for i in tqdm.tqdm(range(len(json_data))):
    json_data[i] = remove_attribute(json_data[i], "content")


with open(file_path, "w", encoding='utf-8') as file:
    json.dump(json_data, file)
