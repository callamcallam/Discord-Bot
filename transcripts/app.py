import requests
from flask import Flask, Response

app = Flask(__name__)

@app.route('/transcripts/<path:url>')
def display(url):
    # Template url: transcripts.centralcityrp.uk/transcripts/attachments/id/id.html
    # replace the base URL with the actual one
    base_url = 'https://cdn.discordapp.com/'
    full_url = base_url + url
    # get the HTML content from the CDN URL
    response = requests.get(full_url)
    html = response.text
    # return the HTML content as a response
    return Response(html, mimetype='text/html')

app.run(debug=True)
