from logs import saveLog
import time
import datetime
import re


def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000


def todayDay(slug):
    millis = int(round(time.time() * 1000))
    if unix_time_millis(slug) - millis < 86400000:
        return True
    else:
        return False


def getDate(date):
    regex = r"(\d.*?) "
    test_str = date

    matches = re.finditer(regex, test_str)

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1

            return match.group(groupNum)


def getHourByDate(date):
    regex = r" (\d.*?):"
    test_str = date

    matches = re.finditer(regex, test_str)

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1

            return match.group(groupNum)


def getAndroidVersion(device):
    regex = r":(\d.*?)/"
    test_str = device["BuildInfo"]["Fingerprint"]

    matches = re.finditer(regex, test_str)

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1

        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1

            return match.group(groupNum)


def processDevicesList(allResult, devicesList):
    # For every device in database, if devicesList is empty or don't contain that brand device, push that device in
    # new brand document first and then in devicesList, else push that device in correct brand document first and
    # then in devicesList
    for device in allResult:
        if (not devicesList) or (
                not filter(lambda x: x["Brand"] == device["BuildInfo"]["Manufacturer"], devicesList)):
            devicesList.append(
                {"Brand": device["BuildInfo"]["Manufacturer"], "IMEI": [device["TelephoneInfo"]["IMEI"]],
                 "counter": 1})
        else:
            map(lambda x: x["IMEI"].append(device["TelephoneInfo"]["IMEI"]), (filter(
                lambda x: (x["Brand"] == device["BuildInfo"]["Manufacturer"]) and (
                    not device["TelephoneInfo"]["IMEI"] in x["IMEI"]), devicesList)))

    # Count every devices
    for device in devicesList:
        device["counter"] = len(device["IMEI"])

    return devicesList


def mapIMEIinDevice(list, device):
    # For every device in database, if userList is empty or don't contain that device with his IMEI, push that
    # device in new brand document first and then in userList, else push that device in correct brand document
    # first and then in userList
    if (not list) or (
            not filter(lambda x: x["TelephoneInfo"]["IMEI"] == device["TelephoneInfo"]["IMEI"], list)):
        list.append(device)
    else:
        if (filter(lambda x: (x["TelephoneInfo"]["IMEI"] == device["TelephoneInfo"]["IMEI"]) and (
                not device["TelephoneInfo"]["IMEI"] in x["TelephoneInfo"]["IMEI"]), list)):
            # if imei isn't alredy inserted
            list.append(device)

    return list
