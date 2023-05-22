import yaml
import re

def read_yaml_config(file_path):
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
        return config

def kuma_custom_check(text):
    pattern = r'熊熊.*?["“]([^"”]+)["”]'
    result = re.findall(pattern, text)
    return result