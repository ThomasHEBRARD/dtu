import csv
from io import StringIO


def log_as_dictionary(log):
    EVENTS = {}
    for row in csv.reader(StringIO(log), delimiter=";"):
        if len(row):
            if row[1] in EVENTS:
                EVENTS[row[1]].append(row[0])
            else:
                EVENTS[row[1]] = [row[0]]

    return EVENTS


def dependency_graph(log):
    TEMP = {}
    for tasks in log.values():
        for i in range(len(tasks) - 1):
            if tasks[i] not in TEMP:
                TEMP[tasks[i]] = {tasks[i + 1]: 1}
            elif tasks[i + 1] not in TEMP[tasks[i]]:
                TEMP[tasks[i]][tasks[i + 1]] = 1
            else:
                TEMP[tasks[i]][tasks[i + 1]] += 1
    return TEMP


########################################################################
########################################################################
from xml.dom import minidom
import datetime


def read_from_file(filename):
    CASES = {}
    file = minidom.parse(
        f"/Users/thomashebrard/code/dtu/02269_process_mining/{filename}"
    )

    models = file.getElementsByTagName("trace")
    for model in models:
        case = model.getElementsByTagName("string")[0].attributes["value"].value
        if case not in CASES:
            CASES[case] = []

        for event in model.getElementsByTagName("event"):
            event_data = {
                "org:resource": None,
                "concept:name": None,
                "cost": None,
                "time:timestamp": None,
            }
            # strings:
            for ev in event.getElementsByTagName("string"):
                if ev.attributes["key"].value in event_data:
                    event_data[ev.attributes["key"].value] = ev.attributes[
                        "value"
                    ].value
            # ints
            for ev in event.getElementsByTagName("int"):
                if ev.attributes["key"].value in event_data:
                    event_data[ev.attributes["key"].value] = int(
                        ev.attributes["value"].value
                    )

            date = datetime.datetime.strptime(
                event.getElementsByTagName("date")[0].attributes["value"].value,
                "%Y-%m-%dT%H:%M:%S%z",
            )
            date = date.replace(tzinfo=None)
            event_data[
                event.getElementsByTagName("date")[0].attributes["key"].value
            ] = date
            CASES[case].append(event_data)
    return CASES


def dependency_graph(log):
    for key, value in log.items():
        log[key] = [v["concept:name"] for v in value]

    TEMP = {}
    for tasks in log.values():
        for i in range(len(tasks) - 1):
            if tasks[i] not in TEMP:
                TEMP[tasks[i]] = {tasks[i + 1]: 1}
            elif tasks[i + 1] not in TEMP[tasks[i]]:
                TEMP[tasks[i]][tasks[i + 1]] = 1
            else:
                TEMP[tasks[i]][tasks[i + 1]] += 1
    return TEMP
