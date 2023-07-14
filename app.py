from flask import Flask, jsonify
from threads_api.src.threads_api import ThreadsAPI
from dotenv import load_dotenv
import os
import asyncio

app = Flask(__name__)

@app.route('/')
def hello():
    return os.environ.get('sampletext')

@app.route('/followers', methods=['GET'])
async def get_followers():
    api = ThreadsAPI()

    # Will login via REST to the Instagram API
    is_success = await api.login(username=os.environ.get('USERNAME'), password=os.environ.get('PASSWORD'), cached_token_path=".token")
    # print(f"Login status: {'Success' if is_success else 'Failed'}")

    if is_success:
        username_to_search = "marat_kotik"
        number_of_likes_to_display = 10

        user_id_to_search = await api.get_user_id_from_username(username_to_search)
        data = await api.get_user_followers(user_id_to_search)
        
        for user in data['users'][0:number_of_likes_to_display]:
            print(f"Username: {user['username']}")

    return jsonify(data)


if __name__ == '__main__':
    load_dotenv()
    app.run()