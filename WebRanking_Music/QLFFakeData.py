import sys
import json
import re

def fakeQLF(infile, outfile):
    with open(infile, 'r', encoding='utf-8') as fr:
        with open(outfile, 'w', encoding='utf-8') as fw:
            for line in fr:
                arr = line.strip().split('\t')
                if(len(arr) != 2):
                    continue
                clusterId = arr[0]
                query = arr[1]
                resultFormat = "{0}\t[QLF$2662:{1}]\t[QLF$2663:100]\n".format(query, clusterId)
                fw.write(resultFormat)

def slotFormat(slotTag):
    slotArr = slotTag.strip().split('|')
    slotOut = {"entity":[], "intent":{}, "constraint":[], "urlkeyword":[], "guarding":[], "officialsite":[], "siteconstraint":[], "otherslots":[]}
    # example of slotOut {entity:freedom of expression&1,intent:,constraint:,urlkeyword:dp,guarding:,officialsite:&,siteconstraint:,otherslots:^}
    for slot in slotArr:
        slotStruct = json.loads(slot, encoding='utf-8')
        type = slotStruct["Type"].lower()
        span = slotStruct["Span"]
        if(type == "ent_ent"):
            slotOut["entity"].append(span + '&1.0') # entity1^entity2
        elif (type == "cons_cons"): #constraint format: constraint
            slotOut["constraint"].append(span + "&&&")
        elif (type.startswith("int_")): #design format: int_intent1&intent1_tag1|intent1_tag2^int_intent2&intent2_tag1|intent2_tag2
            if type not in slotOut['intent']:
                slotOut['intent'][type] = []
            slotOut['intent'][type].append(span)
    slotOutStr = json.dumps(slotOut)
    res = "{"
    resDic = {}
    for k, v in slotOut.items():
        if k == "entity":
            res += 'entity:' + '^'.join(v) + ','
            resDic[k] = "^".join(v)
        elif k == "constraint":
            res += "constraint:" + '^'.join(v) + ','
            resDic[k] = '^'.join(v)
        elif k == "intent":
            resCur = ""
            for k_int, v_int in v.items():
                res += "intent:" + k_int + '&' + '|'.join(v_int) + '^'
                resCur +=k_int + '&' + '|'.join(v_int) + '^'
            resCur = resCur.rstrip('^')
            res = res.rstrip('^') + ','
            resDic[k] = resCur
        elif k == "otherslots":
            resDic[k] = '^'
        elif k == "officialsite":
            resDic[k] = '&'
        else:
            res += k + ':' + '^'.join(v) + ','
            resDic[k] = '^'.join(v)
    res = res.rstrip(',')+ '}'
    res = json.dumps(resDic, separators=(',', ':')).replace('"', '')
    return "AddQuery:MSSemanticFrame{0}".format(res)


def scoreFormat(infile, outfile):
    patReg = r"[^/]*/"
    with open(infile, 'r', encoding='utf-8') as fr:
        with open(outfile, 'w', encoding='utf-8') as fw:
            for line in fr:
                arr = line.strip().split('\t')
                if(len(arr) != 3):
                    continue
                int_id = arr[1]
                patArr = arr[2].split('||-||')
                for patScoreEle in patArr:
                    (pat, score) = patScoreEle.split("||||")
                    score = int(float(score) * 1600 / 99)
                    pat = pat.replace(".*$", "*").lstrip("^").replace("\.", ".")
                    pat= re.sub("(\[\^/\]\*/)+", "", pat)
                    pat = pat.replace("[^/]*$", "*")
                    res_http = "{0}\thttp://{1}\t{2}\t0\t0\t0\t0\t0\t0\t0\t0\t0\t\n".format(int_id, pat, score)
                    res_https = "{0}\thttps://{1}\t{2}\t0\t0\t0\t0\t0\t0\t0\t0\t0\t\n".format(int_id, pat, score)
                    res_http_www = "{0}\thttp://www.{1}\t{2}\t0\t0\t0\t0\t0\t0\t0\t0\t0\t\n".format(int_id, pat, score)
                    res_https_www = "{0}\thttps://www.{1}\t{2}\t0\t0\t0\t0\t0\t0\t0\t0\t0\t\n".format(int_id, pat, score)
                    fw.write(res_http)
                    fw.write(res_https)
                    fw.write(res_http_www)
                    fw.write(res_https_www)

def slotQLF(infile, outfile):
    with open(infile, 'r', encoding='utf-8') as fr:
        with open(outfile, 'w', encoding='utf-8') as fw:
            for line in fr:
                arr = line.strip().split('\t')
                if(len(arr)) != 2:
                    continue
                query = arr[0]
                slotTag = arr[1]
                slotFormatRes = slotFormat(slotTag)
                fw.write("{0}\t{1}\n".format(query, slotFormatRes))

def patternUnique(infile, outfile):
    intIdPatInfoDic = dict()
    with open(infile, 'r', encoding='utf-8') as fr:
        for line in fr:
            arr = line.strip().split('\t')
            intentId = arr[0]
            if intentId not in intIdPatInfoDic:
                intIdPatInfoDic[intentId] = dict()
            pat = arr[1].strip()
            if pat not in intIdPatInfoDic[intentId]:
                intIdPatInfoDic[intentId][pat] = []
            intIdPatInfoDic[intentId][pat].append(tuple(arr[2:]))
    with open(outfile, 'w', encoding='utf-8') as fw:
        for intentId, intentInfo in intIdPatInfoDic.items():
            for pat, patInfo in intentInfo.items():
                patInfoOpti = sorted(patInfo, key = lambda x:float(x[0]), reverse=True)[0]
                fw.write("{0}\t{1}\t{2}\n".format(intentId, pat, "\t".join(patInfoOpti)))




def main():
    if(len(sys.argv) == 1):
        infile = "C:/Code/data/input.tsv"
        outfile = "C:/Code/data/watch.tsv"
    else:
        infile = sys.argv[1]
        outfile = sys.argv[2]
    #fakeQLF(infile, outfile)
    #slotQLF(infile, outfile)
    #scoreFormat(infile, outfile)
    patternUnique(infile, outfile)

if __name__ == "__main__":
    main()