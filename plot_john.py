import os
from lib.phyplot import *
import numpy as np
import plotly as py
import plotly.graph_objs as go
import copy

path = "data/data/"
audio = "data/audio/john/"
annotation = "data/annotation/john/"
dic = {
    "speech": {
        "data": None,
        "time": None,
        "titlename": "speech",
        "range": None,
        "color": 'rgba(0,194,186, 0.4)',
        "hover": 'x+text',
        "yaxis": None,
        "width": 1,
        "layer": 'y',
        "yvisible": False,
        "position": 0,
        "side": 'left'
    },
    "subglottal pressure": {
        "data": None,
        "time": None,
        "titlename": "subglottal pressure",
        "range": None,
        "color": 'rgb(18,0,82)',
        "hover": 'y+text+name',
        "yaxis": None,
        "width": 2,
        "layer": 'y2',
        "yvisible": True,
        "position": 0,
        "side": 'left'
    },
    "intra-oral pressure": {
        "data": None,
        "time": None,
        "titlename": "intra-oral pressure",
        "range": None,
        "color": 'rgb(255,0,255)',
        "hover": 'y+text+name',
        "yaxis": None,
        "width": 1,
        "layer": 'y2',
        "yvisible": True,
        "position": 0,
        "side": 'left'
    },
    "oral airflow": {
        "data": None,
        "time": None,
        "titlename": "oral airflow",
        "range": None,
        "color": 'rgb(255,140,0)',
        "hover": 'y+text+name',
        "yaxis": None,
        "width": 1,
        "layer": 'y3',
        "yvisible": True,
        "position": 0.001,
        "side": 'right'

    },
    "intensity": {
        "data": None,
        "time": None,
        "titlename": "intensity",
        "range": None,
        "color": 'rgb(153,153,0)',
        "hover": 'y+text+name',
        "yaxis": None,
        "width": 1,
        "layer": 'y4',
        "yvisible": True,
        "position": 0.999,
        "side": 'left'
    },
    "fo": {
        "data": None,
        "time": None,
        "titlename": "fo",
        "range": None,
        "color": 'rgb(255,0,0)',
        "hover": 'y+text+name',
        "yaxis": None,
        "width": 2,
        "layer": 'y5',
        "yvisible": True,
        "side": 'right'
    }
}

for i in range(24, 25):
    # initialisation
    dicdata = copy.deepcopy(dic)
    traces = []

    # Get filename index
    if i < 10:
        file_index = "t0" + str(i)
    else:
        file_index = "t" + str(i)
    print(file_index)
    list_file = []

    # Fetch files
    for path, subdirs, files in os.walk(path):
        for name in files:
            if name.startswith(file_index):
                list_file.append(os.path.join(path, name))

    if list_file:
        for file in list_file:
            data, time, typeMeasure = importwsig(file)
            # fetch data
            dicdata[typeMeasure]["data"] = data
            dicdata[typeMeasure]["time"] = time
            dicdata[typeMeasure]["range"] = scaleposition(dicdata[typeMeasure]["data"], typeMeasure)
            # add trace
            traces.append(add_trace(
                dicdata[typeMeasure]["time"],
                dicdata[typeMeasure]["data"],
                dicdata[typeMeasure]["titlename"],
                dicdata[typeMeasure]["hover"],
                dicdata[typeMeasure]["layer"],
                dicdata[typeMeasure]["color"],
                dicdata[typeMeasure]["width"])
            )
            # set yaxis
            dicdata[typeMeasure]["yaxis"] = set_yaxis(typeMeasure,
                dicdata[typeMeasure]["titlename"],
                dicdata[typeMeasure]["color"],
                dicdata[typeMeasure]["range"],
                yover='y5',
                visible=dicdata[typeMeasure]["yvisible"],
                side=dicdata[typeMeasure]["side"],
                position=dicdata[typeMeasure]["position"]
            )

            # Calculate fo
            if typeMeasure == "speech":
                wavefile = audio + file_index + ".wav"
                dicdata["fo"]["data"], dicdata["fo"]["time"] = compute_fo(wavefile)
                dicdata["fo"]["range"] = scaleposition(dicdata["fo"]["data"], "fo")
                # fo trace
                traces.append(add_trace(
                    dicdata["fo"]["time"],
                    dicdata["fo"]["data"],
                    dicdata["fo"]["titlename"],
                    dicdata["fo"]["hover"],
                    dicdata["fo"]["layer"],
                    dicdata["fo"]["color"],
                    dicdata["fo"]["width"])
                )
                # fo axis
                dicdata["fo"]["yaxis"] = set_yaxis("fo",
                    dicdata["fo"]["titlename"],
                    dicdata["fo"]["color"],
                    dicdata["fo"]["range"],
                    visible=True,
                    showline=False,
                    showgrid=False,
                    side='right',
                    position=1
                )

    # Fetch annotation
    annotation_sentence = annotation + file_index + ".txt"
    annotation_phon = annotation + file_index + "_phon.txt"

    sentence_dic = read_annotation(annotation_sentence)
    phon_dic = read_annotation(annotation_phon, encoding="utf-16")

    sentence_x, sentence_y, sentence_text, sentence_shape = annotation_shape(sentence_dic,
                                                                             "sentence",
                                                                             boundary_label="middle",
                                                                             content_label="sentence",
                                                                             position=-2,
                                                                             width=2)
    phon_x, phon_y, phon_text, phon_shape = annotation_shape(phon_dic,
                                                             "phon",
                                                             boundary_label="middle",
                                                             content_label="phoneme",
                                                             position=-1,
                                                             width=1)
    # Annotation grid
    annotation_final = sentence_shape + phon_shape
    # Annotation trace
    traces.append(annotation_trace(sentence_x,
                                   sentence_y,
                                   sentence_text,
                                   fontsize=30,
                                   labelname="sentence",
                                   ysetting='y2'
                                   )
                  )
    traces.append(annotation_trace(phon_x,
                                   phon_y,
                                   phon_text,
                                   fontsize=24,
                                   labelname="phoneme",
                                   ysetting='y2'
                                   )
                  )

    # Layout ===============================================
    layout = go.Layout(
        title=file_index,
        yaxis=dicdata["speech"]["yaxis"],
        yaxis2=dicdata["subglottal pressure"]["yaxis"],
        yaxis3=dicdata["oral airflow"]["yaxis"],
        yaxis4=dicdata["intensity"]["yaxis"],
        yaxis5=dicdata["fo"]["yaxis"],
        shapes=annotation_final
    )

    # # Plotly ===============================================
    fileName = "plotJohn/" + file_index + ".html"
    fig = go.Figure(data=traces, layout=layout)
    py.offline.plot(fig, filename=fileName)
