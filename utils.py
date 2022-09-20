import requests
from config import AUTH_TOKEN


def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

def upload_file(filename):
    headers = {'authorization': AUTH_TOKEN}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                            headers=headers,
                            data=read_file(filename))
    video_url = response.json()["upload_url"]
    return video_url


def send_to_assembly(filename):
    transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
    headers = {
    "authorization": AUTH_TOKEN,
    "content-type": "application/json"
    }
    transcript_request = {
    "audio_url": upload_file(filename)
    }

    transcript_response = requests.post(transcript_endpoint, 
                                    json=transcript_request,
                                    headers=headers)


    transcript_id = transcript_response.json()['id']
    sub_endpoint = transcript_endpoint + "/" + transcript_id

    return headers, sub_endpoint


