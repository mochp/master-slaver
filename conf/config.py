import os


PORTS_INTERFACE = 8888
PORTS_MASTER = 8887
PORTS_SLAVERS = [8886, 8885, 8884]
DEVICE_SLAVERS = [1, 1, 1]
# 配置检验
assert len(DEVICE_SLAVERS) == len(PORTS_SLAVERS)

pwd = os.path.abspath(os.path.join(os.getcwd(), ".."))
INIT_MODEL_LIAN_PATH = os.path.join(pwd, "models/600.h5")


LABELS_LIAN = "idcard_head,idcard_tail,police,seal_name,seal_cir,seal_rec,tile,application,chart,captia,loss,overdraw,00,01"

LABELS_SIFANG = "participant,chart,seal,sign,page"
