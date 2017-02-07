import pandas as pd
import numpy as np
import os
import sys


def GenChangeQuery(dataIn):
    dataChange = dataIn[dataIn['Score'] + dataIn['DocumentPosition'] != 1000]
    queryList = list(dataChange['m:Query'].values)
    return queryList

def GeRDFormatFile(ranker_outfile, rdformat_infile):
    dataIn = pd.read_csv(ranker_outfile, sep ='\t', header = 0)
    columns = ['m:Url', 'DocumentPosition', 'Score', 'm:Query']
    dataIn = dataIn[columns]
    posChangeQueryList = GenChangeQuery(dataIn)
    queryUrlSortBaseScore = dict()
    queryUrlListSort = dict()
    for row in dataIn.values:
        query = row[3]
        """
        if query not in posChangeQueryList:
            continue
        """
        if query not in queryUrlSortBaseScore:
            queryUrlSortBaseScore[query] = {}
        url = row[0]
        score = row[2]
        queryUrlSortBaseScore[query][url] = score
        for query, urlList in queryUrlSortBaseScore.items():
            if query not in queryUrlListSort:
                queryUrlListSort[query] = []
            urlListSort = sorted(urlList.items(), key=lambda x: x[1], reverse=True)
            queryUrlListSort[query] = [item[0] for item in urlListSort]

    with open(rdformat_infile, 'w') as fw:
        for query, urlList in queryUrlListSort.items():
            for i in range(len(urlList)):
                url = urlList[i]
                fw.write("{0}\t{1}\t{2}\n".format(query, url, i))


def main():
    ranker_outfile = "C:/Code/data/JSRankerOutput.tsv"
    rdformat_infile = "C:/Code/data/JSRankerResult.tsv"
    GeRDFormatFile(ranker_outfile, rdformat_infile)

if __name__ == "__main__":
    main()