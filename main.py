import requests
from time import sleep
from utils import send_to_assembly

filename = "/path/to/file"

headers, sub_endpoint = send_to_assembly(filename)

polling_response = requests.get(sub_endpoint, headers=headers)
while polling_response.json()['status'] != 'completed':
    sleep(5)
    print("Transcript processing ...")
    try:
        polling_response = requests.get(sub_endpoint, headers=headers)
    except:
        print("Failed transcription")

response_srt = requests.get(f"{sub_endpoint}/srt", headers=headers)
response_vtt = requests.get(f"{sub_endpoint}/vtt", headers=headers)

with open(f"{filename}.srt", "w") as _file:
    _file.write(response_srt.text)

with open(f"{filename}.vtt", "w") as _file:
    _file.write(response_vtt.text)