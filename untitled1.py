# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 20:23:49 2017

@author: hengyliu
"""

# -*- coding: utf-8 -*-

import os
import math


def EngineNormalized(engine):
    engine = engine.lower().strip()
    if engine.find("bingbefore") != -1 or engine.find("bb") != -1:
        engine = "bingbefore"
    elif engine.find("bingafter") != -1 or engine.find('ba') != -1:
        engine = 'bingafter'
    elif engine.find('google') != -1 or engine.find("g") != -1:
        engine = 'google'
    return engine


def EnginePosNormalized(enginePos):
    enginePosArr = enginePos.split(',')
    left = (enginePosArr[0].split(':')[1].strip()).lower()
    right = (enginePosArr[1].split(':')[1].strip()).lower()
    left = EngineNormalized(left)
    right = EngineNormalized(right)
    return [left, right]


def Read_QueryEngineInfo(fn):
    taskId_query_enginePos = {}
    with open(fn, 'r', encoding='utf-8') as fr:
        fr.readline()
        for line in fr:
            arr = line.strip().split('\t')
            taskInfo = arr[0].split('[')[-1].split()[0]
            if taskInfo not in taskId_query_enginePos:
                taskId_query_enginePos[taskInfo] = {}
            query = arr[1]
            engineInfo = EnginePosNormalized(arr[2])
            taskId_query_enginePos[taskInfo][query] = engineInfo
    return taskId_query_enginePos


def QueryIdealUrlList(dirPath, taskId_query_enginePos):
    query_scoreIdealUrl = {}
    files = os.listdir(dirPath)
    queryNotIn_num = 0
    for file in files:
        task_id = file[:file.find("-withUrl")]
        if task_id not in taskId_query_enginePos:
            print("Task_id : {0} not exist in taskId_query_engiePos".format(task_id))
            continue
        query_enginePos = taskId_query_enginePos[task_id]
        with open(dirPath + file, 'r', encoding='utf-8') as fr:
            columns = fr.readline().strip().split(',')
            print('\t'.join(columns))
            query_idx = columns.index('Query')
            BaseName_idx = columns.index("BaseName")
            ExpName_idx = columns.index("ExpName")
            JudgeMent_idx = columns.index("Judgment")
            L1_idx = columns.index("L1")
            L10_idx = columns.index("L10")
            R1_idx = columns.index("R1")
            R10_idx = columns.index("R10")
            for line in fr:
                line = line.replace('"', "")
                arr = line.strip().split(',')
                query = arr[query_idx].strip('"')
                if query not in query_enginePos:
                    queryNotIn_num += 1
                    print("query: {0}\tnot in query_enginePos".format(query))
                    continue
                engine_pos = query_enginePos[query]
                baseName = EngineNormalized(arr[BaseName_idx])
                expName = EngineNormalized(arr[ExpName_idx])
                judgeScore = int(arr[JudgeMent_idx])
                if judgeScore < 0:
                    basePos = engine_pos.index(baseName)
                    idealUrlList = SelectIdealUrlList(arr[L1_idx: L10_idx + 1], arr[R1_idx: R10_idx], baseName, basePos)
                elif judgeScore > 0:
                    expPos = engine_pos.index(expName)
                    idealUrlList = SelectIdealUrlList(arr[L1_idx: L10_idx + 1], arr[R1_idx: R10_idx], expName, expPos)
                else:
                    if baseName.find("google") != -1:
                        expPos = engine_pos.index(expName)
                        idealUrlList = SelectIdealUrlList(arr[L1_idx: L10_idx + 1], arr[R1_idx: R10_idx], expName, expPos)  # arr[L1_idx: L10_idx + 1]
                    else:
                        basePos = engine_pos.index(baseName)
                        idealUrlList = SelectIdealUrlList(arr[L1_idx: L10_idx + 1], arr[R1_idx: R10_idx], baseName, basePos)
                if len(idealUrlList) == 0:
                    continue
                if query in query_scoreIdealUrl:
                    oldScore = query_scoreIdealUrl[query][0]
                    if oldScore >= abs(judgeScore):
                        continue
                query_scoreIdealUrl[query] = (abs(judgeScore), idealUrlList, task_id)
    print(queryNotIn_num)
    return query_scoreIdealUrl

def UrlNormalized(url):
    url = url.lower().replace('http://', '').replace("https://", "").replace("www.", "").rstrip('/').strip()
    return url

def GoogleUrlLegal(googleUrlList, bingUrlList):
    legal = True
    bingUrlListNormalized = [UrlNormalized(url) for url in bingUrlList]
    for url in googleUrlList[:3]:
        url = UrlNormalized(url)
        if url not in bingUrlListNormalized:
            legal = False
            break
    return legal

def SelectIdealUrlList(leftUrlList, rightUrlList, winEngine, winEnginePos):
    res = []
    if winEngine.find("google") != -1:
        if winEnginePos == 0:
            if GoogleUrlLegal(leftUrlList, rightUrlList):
                res = leftUrlList
        elif winEnginePos == 1:
            if GoogleUrlLegal(rightUrlList, leftUrlList):
                res = rightUrlList
    elif winEngine.find("bing") != -1:
        if winEnginePos == 0:
            res = leftUrlList
        else:
            res = rightUrlList
    return res

def Store(fn, query_scoreIdealUrls):
    with open(fn, 'w', encoding='utf-8') as fw:
        for query, query_scoreIdealUrls in query_scoreIdealUrls.items():
            fw.write("{0}\t{1}\t{2}\t{3}\n".format(query, str(query_scoreIdealUrls[0]), '\t'.join(query_scoreIdealUrls[1]), query_scoreIdealUrls[2]))

def main():
    judge_excel_path = "C:/Code/data/TrainDataForFusionScoreFuction/judgementsExcel/"
    fn_query_enginePos = "C:/Code/data/queryJudgmentsEnginePos_Page1.tsv"
    fn_trainDataForScore = "C:/Code/data/TrainDataForFusionScoreFuction/FusionScoreTrainData.tsv"

    taskId_query_engineInfo = Read_QueryEngineInfo(fn_query_enginePos)
    query_scoreIdealUrls = QueryIdealUrlList(judge_excel_path, taskId_query_engineInfo)
    Store(fn_trainDataForScore, query_scoreIdealUrls)



if __name__ == '__main__':
    main()