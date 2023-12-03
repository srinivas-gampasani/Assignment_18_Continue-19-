from flask import Flask, request, jsonify
import json

app =Flask(__name__)

with open('100tweets.json', 'r', encoding='utf-8') as file:
    tweets = json.load(file)
    
@app.route('/')
def welcome():
    return 'Welcome to Saint Louis University celebrating the Winter Fest ❤️❤️❤️💕❤️❤️❤️🎈🎁'

@app.route('/tweets', methods=['GET'])
def get_all_tweets():
    try:
        return jsonify(tweets)
    except Exception as e:
        return str(e), 500
    
@app.route('/tweets_filtered', methods=['GET'])
def get_filtered_tweets():
    try:
        keyword = request.args.get('keyword')
        if keyword:
            filtered_tweets = [tweet for tweet in tweets if keyword.lower() in tweet['text'].lower()]
            return jsonify(filtered_tweets)
        return jsonify(tweets)
    except Exception as e:
        return str(e), 500

@app.route('/tweet/<int:tweet_id>', methods=['GET'])
def get_tweet_by_id(tweet_id):
    try:
        tweet = next((t for t in tweets if t['id'] == tweet_id), None)
        if tweet:
            return jsonify(tweet)
        return 'Tweet not found', 404
    except ValueError:
        return 'Invalid tweet ID', 400
    except Exception as e:
        return str(e), 500
    
@app.route('/tweets', methods=['POST'])
def create_tweet():
    try:
        data=request.get_json()
        if 'text' not in data or 'user' not in data:
            return 'Bad or incomplete requesr', 400
        
        new_tweet = {
            'id' : len(tweets) + 1,
            'text' : data['text'],
            'user': data['user']
        }

        tweets.append(new_tweet)
        return jsonify(new_tweet), 201
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=False)  #if i enter True generates 200 respons code


