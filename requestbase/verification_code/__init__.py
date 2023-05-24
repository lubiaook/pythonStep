from enum import Enum

from pip._internal.utils.misc import enum

import fateadm_api


# response=fateadm_api.FateadmApi.PredictFromFile()
#     10400= 4位纯数字
#     20400 4位纯英文
#     30400 4 位数字英文
#     40400 4 位汉字
#     50200 复杂计算题
class PreType(Enum):
    number = 10400
    enChar = 20400
    numAndEnChar = 30400
    ChinaChar = 40400
    math = 50200


if __name__ == '__main__':
    appId = '337980'
    appKey = 'tPggC+sdse4S0SEyvsWDNZVz9B/V5Y1f'
    pdId = '137980'
    pdSecret = 'IEn78nf6ywJK/oWKfxLKSCmszE0d10WA'
    feiFeiApi = fateadm_api.FateadmApi(app_key=appKey, app_id=appId, pd_key=pdSecret, pd_id=pdId)
    print(feiFeiApi.pd_id)
    balance = feiFeiApi.QueryBalcExtend()  # 直接返余额
    print(balance)

    print(PreType.number.value)
    
    feiFeiApi.Predict(pred_type=PreType.number.value, img_data='')
