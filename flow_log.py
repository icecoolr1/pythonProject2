import datetime
import json

import requests

methods = [
    'P_CRCInputError',
    'P_CRCOutputError',
    'P_IfFluxIn',
    'P_IfFluxOut'
]

ips = [

    # 华三
    "18.128.64.131",
    "18.128.64.132",
    "18.128.64.133",
    "18.128.64.134",
    "18.128.64.135",
    "18.128.64.136",
    "18.128.64.141",
    "18.128.64.142",
    "18.128.64.143",
    "18.128.64.144",
    "18.128.64.145",
    "18.128.64.146",
    "18.128.64.147",
    "18.128.64.148",
    "18.128.64.149",
    "18.128.64.150",
    "18.128.64.151",
    "18.128.64.152",
    "18.128.64.153",
    "18.128.64.154",
    "18.128.64.155",
    "18.128.64.156",
    "18.128.64.157",
    "18.128.64.158",
    "18.128.64.159",
    "18.128.64.163",
    "18.128.64.164",
    "18.128.64.165",
    "18.128.64.173",
    "18.128.64.190",
    "18.128.64.191",
    "18.128.64.202",
    "18.128.64.203",
    "18.128.64.222",
    "18.128.64.223",

    # 华为
    "18.128.64.1",
    "18.128.64.3",
    "18.128.64.4",
    "18.128.64.5",
    "18.128.64.6",
    "18.128.64.7",
    "18.128.64.16",
    "18.128.64.17",
    "18.128.64.18",
    "18.128.64.19",
    "18.128.64.20",
    "18.128.64.21",
    "18.128.64.22",
    "18.128.64.23",
    "18.128.64.27",
    "18.128.64.28",
    "18.128.64.41",
    "18.128.64.42",
    "18.128.64.50",
    "18.128.64.51",
    "18.128.64.52",
    "18.128.64.61",
    "18.128.64.62",
    "18.128.64.63",
    "18.128.64.64",
    "18.128.64.65",
    "18.128.64.66",
    "18.128.64.67",
    "18.128.64.70",
    "18.128.64.71",
    "18.128.64.72",
    "18.128.64.73",

]


def flow_dect(method, ip):
    # 接口地址
    url = "http://132.252.101.156:8090/gxpt/dataservice/api/queryData"

    # appKey
    appkey = {'appKey': '8d7f62ba4458f035cfc7afa32b3c7b6b'}

    date = datetime.datetime.now().strftime('%Y-%m-%d')
    cDate = date.replace("-", "/")

    # 开始时间 以24小时为一次
    # start_time = '2022/01/12 00:00:00'
    start_time = cDate + " 00:00:00"

    # 结束时间
    # end_time = '2022/01/12 23:59:59'
    end_time = cDate + " 23:59:59"
    s_time = start_time[0:11]

    # 接口入参
    queries = [{"aggregator": "none", "metric": method, "tags": {"MgmtIp": ip}}]

    # 封装json
    data = {'start': start_time, 'end': end_time, 'queries': queries}

    time_list = ['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55']

    # 发送post请求
    req1 = requests.post(url, json=data, headers=appkey)

    # 将返回值转为json模式
    res = req1.json()
    items = json.loads(json.dumps(res))

    # 获得接口内部dps项的值
    items1 = items["value"]
    length = len(items1)
    if length > 0:
        items2 = items["value"][0]['dps']
    else:
        return "not found data"

    # 该字典接受各个时间段返回的次数 如果某时间段小于12次 则出现异常
    timeCount = {}
    # 该列表返回最后出现异常时段的结果
    result_list = []
    # 返回精确时间列表
    accuracy_timeCount = {}
    # 返回异常时间字典
    accuracy_wrongTimeCount = {}
    res_timeList = {}

    # {时段1:[返回时间],时段2:[返回时间]}
    for item in items2:
        # 获取时段
        num_str_1 = item[11:13]
        # 获取各时段接口返回次数
        if num_str_1 not in timeCount:
            timeCount[num_str_1] = 1
            accuracy_timelist = [item]
            accuracy_timeCount[num_str_1] = accuracy_timelist
        else:
            timeCount[num_str_1] += 1
            accuracy_timeCount[num_str_1].append(item)

    # 获取具体时间
    for hour in accuracy_timeCount:
        if timeCount[hour] < 12:
            accuracy_wrongTimeCount[hour] = []
            result_list.append(hour)
            for time in accuracy_timeCount[hour]:
                tTime = time[14:16]
                cTime_list = [tTime]
                accuracy_wrongTimeCount[hour].append(tTime)

    for hour in accuracy_wrongTimeCount:
        list_res = accuracy_wrongTimeCount[hour]
        list_fres = list(set(time_list).difference(set(list_res)))
        # print(list_fres)
        lista = []
        res_timeList[hour] = lista
        for res in list_fres:
            res_timeList[hour].append(s_time + hour + ":" + res + ":00")

    return res_timeList


if __name__ == '__main__':
    method_problems = {}
    problems = {}
    for method in methods:
        for ip in ips:
            print(ip)
            problems[ip] = flow_dect(method, ip)
        method_problems[method] = problems

    # 最终结果
    # print(json.dumps(problems))
    print(json.dumps(method_problems))
