from chalice import Chalice, Response
from urllib.parse import parse_qs
import os
import requests
import json
import time
from chalicelib.response_template import Fields, Attachment, SlackResponse
app = Chalice(app_name='github-info-webhook')


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
        text = request['text'][0].split()
        if not is_request_valid(request):
            return Response(body='You are not authorized to send this request.Please try from a valid source',
                            status_code=200,
                            headers={'Content-Type': 'text/plain'})
        elif len(text) != 1:
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
            res = SlackResponse()
            res.response_type = "in_channel"
            res.text = 'you have entered invalid username'
            res_json = json.dumps(res.to_struct())

            if(myres.ok):
                data = json.loads(myres.content)
                attach = Attachment()
                attach.fallback = "Here is the " + text[0] + " details"
                attach.color = "#000000"
                attach.pretext = text[0] + " info"
                attach.author_name = data['name']
                attach.author_icon = data['avatar_url']
                attach.title = 'https://github.com/' + text[0]
                attach.title_link = data['url']
                attach.text = "User is valid and here is its info"
                field1 = Fields()
                field2 = Fields()
                field3 = Fields()
                field1.title = "Bio"
                field1.value = data['bio']
                field1.short = False
                field2.title = "Company"
                field2.value = data['company']
                field2.short = False
                field3.title = "Location"
                field3.value = data['location']
                field3.short = False
                attach.fields = [field1, field2, field3]
                attach.image_url = "http://my-website.com/path/to/image.jpg"
                attach.thumb_url = "http://example.com/path/to/thumb.png"
                attach.footer_icon = "https://cdn4.iconfinder.com/data/icons/iconsimple-logotypes/512/github-256.png"
                attach.footer = "Github Info"
                attach.ts = time.time()
                res = SlackResponse()
                res.response_type = "in_channel"
                res.text = 'Here is the user info from github for ' + text[0]
                res.attachments = [attach]
                res_json = json.dumps(res.to_struct())

            print(res_json)
            return Response(body=res_json,
                            status_code=200,
                            headers={'Content-Type': 'application/json'})
    except():
        return Response(body='Invalid Request',
                        status_code=400,
                        headers={'Content-Type': 'text/plain'})
