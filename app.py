from chalice import Chalice, Response
from urllib.parse import parse_qs
import os
import requests
import json
import time
app = Chalice(app_name='github-access-webhook')


def is_request_valid(request):
    is_token_valid = request['token'][0] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request['team_id'][0] == os.environ['SLACK_TEAM_ID']
    is_channel_id_valid = request['channel_id'][0] == os.environ['CHANNEL_ID']

    return is_token_valid and is_team_id_valid and is_channel_id_valid


@app.route('/git-user-validity', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def github_valid_user():
    request = parse_qs(app.current_request.raw_body.decode())
    print(request['text'][0])
    try:
        if not is_request_valid(request):
            return Response(body='You are not authorized to send this request.Please try from a valid source',
                            status_code=200,
                            headers={'Content-Type': 'text/plain'})
        text = request['text'][0].split()

        if len(text) != 1:
            res = {
                "response_type": "in_channel",
                "text": "you have entered invalid username"
            }
            return Response(body=res,
                            status_code=200,
                            headers={'Content-Type': 'application/json'})
        else:
            myres = requests.get('https://api.github.com/users/' + text[0])
            print(myres)
            res = {
                "response_type": "in_channel",
                "text": 'you have entered invalid username'

            }
            if(myres.ok):
                data = json.loads(myres.content)
                attachments = [
                    {
                        "fallback": "Here is the " + text[0] + " details",
                        "color": "#000000",
                        "pretext": text[0] + " info",
                        "author_name": data['name'],
                        "author_link": "http://github.com/" + text[0],
                        "author_icon": data['avatar_url'],
                        "title": 'https://github.com/' + text[0],
                        "title_link": data['url'],
                        "text": "User is valid and here is its info",
                        "fields": [
                            {
                                    "title": "Bio",
                                    "value": data['bio'],
                                    "short": False
                            },
                            {
                                "title": "Company",
                                "value": data["company"],
                                "short": False
                            },
                            {
                                "title": "Location",
                                "value": data['location'],
                                "short": False
                            }
                        ],
                        "image_url": "http://my-website.com/path/to/image.jpg",
                        "thumb_url": "http://example.com/path/to/thumb.png",
                        "footer_icon": "https://cdn4.iconfinder.com/data/icons/iconsimple-logotypes/512/github-256.png",
                        "footer": "Github Info",
                        "ts": time.time()
                    }
                ]
                res = {
                    "response_type": "in_channel",
                    "text": 'Here is the user info from github for ' + text[0],
                    "attachments": attachments
                }
            print(res)
            return Response(body=res,
                            status_code=200,
                            headers={'Content-Type': 'application/json'})
    except():
        return Response(body='Invalid Request',
                        status_code=400,
                        headers={'Content-Type': 'text/plain'})


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
