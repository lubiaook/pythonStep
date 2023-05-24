from lxml import etree
import requests
import fateadm_api


##
def getcodeText(pre_type, img):
    result = None
    appId = '337980'
    appKey = 'tPggC+sdse4S0SEyvsWDNZVz9B/V5Y1f'
    pdId = '137980'
    pdSecret = 'IEn78nf6ywJK/oWKfxLKSCmszE0d10WA'
    feiFeiApi = fateadm_api.FateadmApi(app_key=appKey, app_id=appId, pd_key=pdSecret, pd_id=pdId)
    response = feiFeiApi.Predict(pred_type=pre_type, img_data=img)
    # response = feiFeiApi.PredictFromFile(pred_type=pre_type, img_data=img)
    print(response.request_id)
    print(response.ret_code)
    return response.pred_rsp.value


if __name__ == '__main__':
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx'
    guwenMainPage = requests.get(url=url, headers=header)
    guwenMainPageEtree = etree.HTML(guwenMainPage.text)
    imgUrl = guwenMainPageEtree.xpath('//*[@id="imgCode"]/@src')
    print(imgUrl)
    imgUrlT = 'http://so.gushiwen.cn' + imgUrl[0]
    print(imgUrlT)
    # # 下载图片
    imgCode = requests.get(url=imgUrlT, headers=header).content
    with open('./imgCode.jpg', 'wb') as wb:
        wb.write(imgCode)

    # 调用
    code =getcodeText(30400,imgCode)
    print(code)

