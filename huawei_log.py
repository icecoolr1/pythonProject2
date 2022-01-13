import json
import datetime
import requests

ips = [
    "18.128.64.50",
    "18.128.65.50"
]


def getHUAWEIProblems(ip):
    # 接口地址
    url = "http://132.252.101.156:8090/gxpt/dataservice/api/queryData"

    # appKey
    appkey = {'appKey': '8d7f62ba4458f035cfc7afa32b3c7b6b'}

    date = datetime.datetime.now().strftime('%Y-%m-%d')
    cDate = date.replace("-", "/")

    # 开始时间 以24小时为一次
    # start_time = '2022/01/12 00:00:00'
    start_time = cDate+" 00:00:00"

    # 结束时间
    # end_time = '2022/01/12 23:59:59'
    end_time = cDate+" 23:59:59"

    s_time = start_time[0:11]

    # 接口入参
    queries = [{"aggregator": "none", "metric": "HWCPUserData", "tags": {"MgmtIp": ip}}]

    # 华三入参
    MgmtIp = {"MgmtIp": "18.128.64.203"}

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
    problems = {}
    for ip in ips:
        print(ip)
        problems[ip] = getHUAWEIProblems(ip)
    # 最终结果
    print(json.dumps(problems))
