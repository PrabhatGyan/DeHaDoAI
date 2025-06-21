
path_of_prompt = '/DATA/gyan/GP/ncvpripg2025/dehado/internvl_prompt.txt'

def load_prompt(file_path=path_of_prompt):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()