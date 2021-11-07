from collections import defaultdict
import random
from flask import Flask, send_from_directory, redirect
from flask_restful import Resource, Api, abort, reqparse
from enum import Enum
import csv
from pathlib import Path
from collections import namedtuple
Politician = namedtuple('Politician', ['picture_name', 'emotion', 'emotion_strength'])



app = Flask(__name__, static_folder='../static')
api = Api(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


politicians = []

# TODO move to a sqlite db or something more sensible. 
with open('../static/db.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
        else:
            if float(row[3]) > 0.4:
                politicians.append(
                    Politician(row[0], row[1], row[2], row[3])
                )
        line_count += 1


politicians_by_emotion = defaultdict(dict)

for politician in politicians:
    # Need the emotion dictionary to have a list. We choose a random 
    # picture from this list for emotion by politician. 
    if politician.emotion not in politicians_by_emotion[politician.name]:
        politicians_by_emotion[politician.name][politician.emotion] = []
    politicians_by_emotion[politician.name][politician.emotion].append(
        politician.picture_name
    )

class PoliticianPics(Resource):
    def get(self, picture_file):
        return send_from_directory(app.static_folder, picture_file, max_age=0)


class Politicians(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'politician',
            type=str,
            required=True,
            help="Which politician to choose"
        )

        parser.add_argument(
            'emotion', 
            type=str, 
            required=True, 
            help='Emotion that you want your politician to have'
        )
        args = parser.parse_args()

        politician_emotion_pictures = politicians_by_emotion[args['politician']][args['emotion']]

        if politician_emotion_pictures:
            picture_file = random.choice(politician_emotion_pictures)
            return redirect(api.url_for(PoliticianPics, picture_file=picture_file))
        else:
            abort(404, message=f"No {args['politician']} found with emotion {args['emotion']}")


api.add_resource(Politicians, '/politicians/')
api.add_resource(PoliticianPics, '/politicianpics/<picture_file>/')

if __name__ == '__main__':
    app.run()