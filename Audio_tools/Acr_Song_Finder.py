from acrcloud.recognizer import ACRCloudRecognizer
from acrcloud.recognizer import ACRCloudRecognizeType
import json
import logging
from pprint import pprint

# ACR Cloud Song Searcher Class

# To use this class you need the Acr Python SDK which can be found here
# https://github.com/acrcloud/acrcloud_sdk_python

# You also need to create a configuration file with the following Key's replacing the value with your credentials Values
# config = {
#     'host': 'id_eu_west.api.acrcloud.com',
#     'access_key': 'access key',
#     'access_secret': 'secret key',
#     'debug': True,
#     'timeout': 10
# }
# Additional help can be found here https://docs.acrcloud.com/docs/acrcloud/tutorials/identify-music-by-sound/

class Acr_cloud(object):
    def __init__(self, config_file):
        self.config = self.load_creds(config_file)
        self.acr = ACRCloudRecognizer(self.config)

    def load_creds(self, config_file):
        try:
            with open(config_file, 'r') as creds:
                usr_key = json.load(creds)
                return usr_key
        except Exception as e:
            logging.error(e)

    def trace_sample(self, wav_file):
        data_dictionary = json.loads(self.acr.recognize_by_file(wav_file, 0))
        data_dictionary = data_dictionary["metadata"]
        song_data = {"Artist": data_dictionary["music"][0]["artists"][0]["name"],
                     "Title": data_dictionary["music"][0]["title"],
                     "Duration": data_dictionary["music"][0]["duration_ms"]}
        mins = str(round((float(song_data["Duration"])/1000)/60, 2))  # Convert duration_ms to minutes and seconds

        song_data["Duration"] = mins.replace(".", ":")
        song_data["Genre"] = data_dictionary["music"][1]["genres"][0]["name"]
        return song_data


# You can test with this to make sure your configuration and package installation is correct
# if __name__ == '__main__':
#     arc = Acr_cloud("config.json")
#     song = arc.trace_sample(r"sample.wav")
#     pprint(song)
