from flask import Flask, request
from flask.templating import render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

template = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>M4ple2Sonolus Converter</title>
  </head>
  <body>
      Convert M4ple SUS to Sonolus level.json
  </body>
</html>"""

def convertM4pleSUS(input_sus):
    sus = input_sus
    START_SYMBOL = 'BPM\n'
    header = sus[:sus.find(START_SYMBOL)]
    start_index = sus.find(START_SYMBOL) + len(START_SYMBOL)

    measures = sus[start_index:].replace(' ', '').split('\n')
    measures = list(filter(lambda x: len(x) > 1 and x[0] == '#', measures))

    bpm_list = list(filter(lambda x: x[:4] == '#BPM', measures))
    for i in range(len(bpm_list)):
        bpm_index = bpm_list[i][4:6]
        bpm = bpm_list[i].split(':')[1]
        new_bpm_index = str(int(bpm_index) - 1).zfill(2)
        bpm_list[i] = f"#BPM{new_bpm_index}: {bpm}"

    ref_bpm_list = list(filter(lambda x: x[4:6] == '08', measures))
    for i in range(len(ref_bpm_list)):
        measure, bpm_index = ref_bpm_list[i].split(':')
        new_bpm_index = str(int(bpm_index) - 1).zfill(2)
        ref_bpm_list[i] = f"{measure}: {new_bpm_index}"

    pulses = list(filter(lambda x: x[:4] != '#BPM' and x[4:6] == '02', measures))

    tap_notes = list(filter(lambda x: x[4] == '1', measures))

    directinal_notes = list(filter(lambda x: x[4] == '5', measures))

    slide_notes = list(filter(lambda x: x[4] == '3', measures))
    for i in range(len(slide_notes)):
        slide_note = list(slide_notes[i])

        if ord(slide_note[6].upper()) < ord('A'):
            raise Exception('Unspported SUS.')
        slide_note[6] = str(ord(slide_note[6].upper()) - ord('A'))
        slide_notes[i] = ''.join(slide_note)

    controls = pulses + bpm_list + ref_bpm_list
    notes = tap_notes + directinal_notes + slide_notes

    output_sus = ""
    output_sus += header
    for control in controls:
        output_sus += control + '\n'
    output_sus += "\n#TIL00: \"\"\n"
    output_sus += "#HISPEED 00\n"
    output_sus += "#MEASUREHS 00\n\n"
    for note in notes:
        output_sus += note + '\n'
    return output_sus

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return template
    elif request.method == 'POST':
        chart = request.json['chart']
        return convertM4pleSUS(chart)

if __name__ == '__main__':
  app.run(host='localhost', port=8080)