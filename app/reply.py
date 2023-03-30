import os
import json
from dotenv import load_dotenv
from redis import Redis
import openai
from slack_bolt import App

if __name__ == '__main__':

    load_dotenv()
    cache_client = Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'])
    slack_bot = App(token=os.environ['SLACK_BOT_TOKEN'])
    openai.api_key = os.getenv('OPENAI_API_KEY')

    while 1:
        item = cache_client.lpop('messages')
        if item is None:
            break
        item = json.loads(item)
        slack_bot_id = item['authorizations'][0]['user_id']
        question = item['event']['text'].replace('<@%s> ' %(slack_bot_id), '')

        response = openai.ChatCompletion.create(
            model=os.environ['SLACK_BOT_TOKEN'],
            messages=[
                {'role': 'user', 'content': question},
            ],
        )
        answer = response.choices[0]['message']['content']

        slack_bot.client.chat_postMessage(
            channel=item['event']['channel'],
            thread_ts=item['event']['event_ts'],
            text=answer
        )
