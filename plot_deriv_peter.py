import os
from lib.phyplot import *
import numpy as np
import plotly as py
import plotly.graph_objs as go
import copy

path = "data/peter_psg/"
audio = "data/audio/peter/"
annotation = "data/annotation/peter/"

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
    "d(ps)": {
        "data": None,
        "time": None,
        "titlename": "derivate ps",
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
    "fo": {
        "data": None,
        "time": None,
        "titlename": "fo",
        "range": None,
        "color": 'rgb(255,0,0)',
        "hover": 'y+text+name',
        "yaxis": None,
        "width": 2,
        "layer": 'y4',
        "yvisible": True,
        "side": 'right'
    },
    "d(fo)": {
        "data": None,
        "time": None,
        "titlename": "derivate fo",
        "range": None,
        "color": 'rgb(255,0,255)',
        "hover": 'y+text+name',
        "yaxis": None,
        "width": 1,
        "layer": 'y5',
        "yvisible": True,
        "position": 0.01,
        "side": 'right'
    }
}

for i in range(1, 2):
    # initialisation
    dicdata = copy.deepcopy(dic)
    traces = []

    file_index = "B9"
    list_file = []

    for path, subdirs, files in os.walk(path):
        for name in files:
            if name.startswith(file_index):
                list_file.append(os.path.join(path, name))

    # print(list_file)

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

            if typeMeasure == "subglottal pressure":
                # calculate derivative of ps

                dps = np.diff(data)
                dps = np.append(dps, [0.0])
                print(dps)
                # np.savetxt("subglottal.txt", data)
                # np.savetxt("dsubglottal.txt", dps)
                # print(len(data))
                # print(len(dps))
                # trace dps
                dicdata["d(ps)"]["data"] = dps
                dicdata["d(ps)"]["time"] = time
                dicdata["d(ps)"]["range"] = scaleposition(dicdata["d(ps)"]["data"], "d(ps)")
                # add trace
                traces.append(add_trace(
                    dicdata["d(ps)"]["time"],
                    dicdata["d(ps)"]["data"],
                    dicdata["d(ps)"]["titlename"],
                    dicdata["d(ps)"]["hover"],
                    dicdata["d(ps)"]["layer"],
                    dicdata["d(ps)"]["color"],
                    dicdata["d(ps)"]["width"])
                )
                # set yaxis
                dicdata["d(ps)"]["yaxis"] = set_yaxis("d(ps)",
                                                      dicdata["d(ps)"]["titlename"],
                                                      dicdata["d(ps)"]["color"],
                                                      dicdata["d(ps)"]["range"],
                                                      yover='y5',
                                                      visible=dicdata["d(ps)"]["yvisible"],
                                                      side=dicdata["d(ps)"]["side"],
                                                      position=dicdata["d(ps)"]["position"]
                                                      )

            # Calculate fo
            if typeMeasure == "speech":
                wavefile = audio + file_index + ".wav"
                dicdata["fo"]["data"], dicdata["fo"]["time"] = compute_fo(wavefile)

                # calculate derivative of fo
                dfo = np.diff(dicdata["fo"]["data"])
                dfo = np.append(dfo, [np.nan])

                dicdata["d(fo)"]["data"] = dfo
                dicdata["d(fo)"]["time"] = dicdata["fo"]["time"]
                dicdata["d(fo)"]["range"] = scaleposition(dicdata["d(fo)"]["data"], "d(fo)")


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
                                                   yover='y5',
                                                   showgrid=False,
                                                   side='right',
                                                   position=1
                                                   )

                # trace dfo
                traces.append(add_trace(
                    dicdata["d(fo)"]["time"],
                    dicdata["d(fo)"]["data"],
                    dicdata["d(fo)"]["titlename"],
                    dicdata["d(fo)"]["hover"],
                    dicdata["d(fo)"]["layer"],
                    dicdata["d(fo)"]["color"],
                    dicdata["d(fo)"]["width"])
                )
                # set yaxis
                dicdata["d(fo)"]["yaxis"] = set_yaxis("d(fo)",
                                                      dicdata["d(fo)"]["titlename"],
                                                      dicdata["d(fo)"]["color"],
                                                      dicdata["d(fo)"]["range"],
                                                      # yover='y5',
                                                      visible=dicdata["d(fo)"]["yvisible"],
                                                      side=dicdata["d(fo)"]["side"],
                                                      position=dicdata["d(fo)"]["position"]
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
    annotation_shape = sentence_shape + phon_shape
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
        yaxis3=dicdata["d(ps)"]["yaxis"],
        yaxis4=dicdata["fo"]["yaxis"],
        yaxis5=dicdata["d(fo)"]["yaxis"],
        shapes=annotation_shape
    )

    # # Plotly ===============================================
    fileName = "plotpeter/" + file_index + ".html"
    fig = go.Figure(data=traces, layout=layout)
    py.offline.plot(fig, filename=fileName)


