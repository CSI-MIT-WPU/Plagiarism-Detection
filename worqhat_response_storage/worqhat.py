import requests
from pymongo import MongoClient

WORQHAT_API_KEY = "" #api key daaldo idhar 
WORQHAT_API_ENDPOINT = "https://api.worqhat.com/api/ai/content/v2"  # AiCon V2

MONGODB_URI = "mongodb://localhost:27017"
MONGODB_DATABASE = "rachit"
MONGODB_COLLECTION = "responses"


def get_responses_from_worqhat(question):
    headers = {
        "Authorization": f"Bearer {WORQHAT_API_KEY}"
    }
    data = {
        "question": question,
        "preserve_history": False,
        "stream_data": False,
        "randomness": 0.4,
        "response_type": "json",
    }
    response = requests.post(WORQHAT_API_ENDPOINT, headers=headers, json=data)

    try:
        response.raise_for_status()
        response_content = response.json()

        return response_content
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        print(f"Response Content: {response.content}")
        raise Exception(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        print(f"Response Content: {response.content}")
        raise Exception(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        print(f"Response Content: {response.content}")
        raise Exception(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        print(f"Response Content: {response.content}")
        raise Exception(f"Error: {err}")


def store_responses_in_mongodb(question, response_contents):
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_COLLECTION]

    document = {
        "question": question,
        "responses": response_contents,
    }

    collection.insert_one(document)
    print(f"{len(response_contents)} responses stored in MongoDB successfully!")


if __name__ == "__main__":
    question = input("Enter a question: ")

    try:
        num_responses = 10  # Change this to the desired number of responses
        response_contents = [get_responses_from_worqhat(question) for _ in range(num_responses)]
        store_responses_in_mongodb(question, response_contents)
    except Exception as e:
        print(f"Error: {e}")
