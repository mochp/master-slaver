import pymysql

conn = pymysql.connect(host='172.18.89.119', port=3306, user='root', passwd='10NsS2mM!@#$', db='automl',charset='utf8')


class Param:
    def __init__(self, filePath, labelList):
        self.filePath = filePath
        self.labelList = labelList


def getMenuFeature(modlId):
    cur = conn.cursor()
    cur.execute(
        "select model_file_path from model_info where model_id ='%s';" % (
            modlId))
    cur.rowcount
    modelPath = cur.fetchall()
    cur.execute(
        "select label_value from model_label where model_id = '%s';" % (
            modlId))
    labelList = list(cur.fetchall())
    cur.close()
    param = Param(modelPath[0], labelList)
    path = param.filePath[0]

    total_lists = [x[0] for x in param.labelList]
    label = ','.join(total_lists)
    return path, label


if __name__ == "__main__":
    import os
    model_old_path, label = getMenuFeature(685)
    model_path = os.path.join("~/modelFile", os.path.split(model_old_path)[-1])
    print(model_path)
    print(label)