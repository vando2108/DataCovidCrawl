import requests
import json

api_host = "https://covid19.ncsc.gov.vn/api/v3/covid/province/"

def LoadDate():
    with open("date.txt", "r") as f:
        date = f.read()
    date = date.split("\n")
    date.pop()
    ret = dict()
    for case in date:
        ret[case] = 0
    return ret

def LoadHeader():
    with open("header_covid_data.txt", "r") as f:
        headers = f.read()
    headers = headers.split("\n")
    headers.pop()
    ret = dict()
    date = LoadDate()
    for field_name in headers:
        if field_name.find("by_time") == -1 and field_name.find("by_day") == -1:
            ret[field_name] = 0
        else:
            ret[field_name] = dict()
    return ret

if __name__ == "__main__":
    total_data = LoadHeader()
    for id in range(2, 64):
        response = requests.get(api_host + str(id))
        data = response.json()
        print("id: ", data["id"])
        print("province name: ", data["name"])
        for field in total_data:
            if isinstance(total_data[field], int):
                total_data[field] += int(data[field])
            else:
                for date in data[field]:
                    if date in total_data[field]:
                        total_data[field][date] += int(data[field][date])
                    else:
                        total_data[field][date] = int(data[field][date])

    dates = set()
    for key in total_data:
        if isinstance(total_data[key], dict):
            for date in total_data[key]:
                dates.add(date)

    with open("covid_data.csv", "w") as f:
        f.write("date,")
        for key in total_data:
            if isinstance(total_data[key], dict):
                f.write(key + ',')
        f.write('\n')
        for date in dates:
            f.write(date + ',')
            for field in total_data:
                if isinstance(total_data[field], dict):
                    if date in total_data[field]:
                        f.write(str(total_data[field][date]) + ',')
                    else:
                        f.write("0,")
            f.write('\n')

        for key in total_data:
            if isinstance(total_data[key], int):
                f.write(key + ',' + str(total_data[key]) + '\n')
