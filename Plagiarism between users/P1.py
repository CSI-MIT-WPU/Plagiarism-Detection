
a={}
import re
import difflib
import pandas as pd
from pymongo import MongoClient

def custom_tokenizer(code):
    symbols = r'[.,;(){}[\]+-=*/%&|<>\n]'

    tokens = re.split(symbols, code)
    tokens = [token for token in tokens if token]

    return tokens

def calculate_similarity(code1, code2):

    tokens1 = custom_tokenizer(code1)
    tokens2 = custom_tokenizer(code2)

    matcher = difflib.SequenceMatcher(None, tokens1, tokens2)
    similarity_ratio = matcher.ratio()
    return similarity_ratio

def check_similarity(df):
    n =len(df)


    for i in range(n):
        for j in range(i + 1, n):
            similarity = calculate_similarity(df.iloc[i]['code'], df.iloc[j]['code'])
            similarity_threshold = 0.2  # Adjust the threshold as needed

            if similarity > similarity_threshold:
                code_i = df.iloc[i]['code']
                code_j = df.iloc[j]['code']
                id_i = df.iloc[i]['email']
                id_j = df.iloc[j]['email']
                print(f"Potential similarity detected between Code {id_i}:\n{code_i}\n and Code {id_j}:\n{code_j}!")

def main():
    # Example codes as a DataFrame with more similarity


    client = MongoClient("mongodb+srv://test:test@cluster0.opvmswf.mongodb.net/?retryWrites=true&w=majority")
    db = client["CSI"]
    collection = db["plagiarism_checker"]
    documents = list(collection.find({}))

    # Create a DataFrame using the retrieved documents
    df = pd.DataFrame(documents)

    # Check for similarity based on the "code" field
    check_similarity(df)




if __name__ == "__main__":
    main()