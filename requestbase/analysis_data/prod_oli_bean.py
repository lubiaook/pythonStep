from flask import Flask, jsonify
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

app = Flask(__name__)
valid_pages = ['m2405.html', 'm2407.html', 'm2408.html', 'm2409.html', 'm24011.html', "m2412.html", "m2501.html",
               "m2503.html"]
global_future_valid_pages = ["ZS24K.html", "ZS00Y.html", "ZS24U.html", "ZS24N.html", "ZS25F.html", "ZS25H.html"]


def get_data_from_page(url):
    try:
        chrome_driver_path = './chromedriver'
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        # options.add_argument('--proxy-server=http://221.224.252.112:31341')
        # options.add_argument('--proxy-server=http://49.7.11.187:80')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
        driver.get(url)
        currentElement = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[8]/div[1]/div/div[1]')
#        dayOpenElement = driver.find_element(By.XPATH,
        #                                      '//*[@id="app"]/div/div/div[8]/div[2]/div/table/tbody/tr[1]/td[1]/span/span')
        # yesterdayEndOpenElement = driver.find_element(By.XPATH,
        #                                               '//*[@id="app"]/div/div/div[8]/div[2]/div/table/tbody/tr[2]/td[1]/span/span')
        cnName=driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div[7]/div/div[1]/span[1]')
        enName=driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div[7]/div/div[1]/span[2]')

        data = {
            'status': 1,
            'current': currentElement.text,
            'enName': enName.text,
            'cnName': cnName.text
        }
        driver.quit()
    except NoSuchElementException as e:
        # 处理元素未找到异常
        data = {'status': 0,
                'error': 'Element not found'}
    except Exception as e:
        # 处理其他异常
        data = {'status': 0, 'error': str(e)}

    return data


@app.route('/get_dict/<page>', methods=['GET'])
def get_dict(page):
    if page == 'qihuo':
        data = valid_pages
    elif page == '':
        data = global_future_valid_pages
    else:
        data = valid_pages
    return jsonify({'data': data})


@app.route('/get_data/<page>', methods=['GET'])
def get_data(page):
    url = "https://quote.eastmoney.com/qihuo/" + page
    print(url)
    if page not in valid_pages:
        return jsonify({'error': 'Invalid page value. Must be one of: {}'.format(valid_pages)}), 400

    data = get_data_from_page(url)
    return jsonify({'data': data})


@app.route('/get_data_eastmoney/<page>', methods=['GET'])
def get_data_eastmoney(page):
    if page not in global_future_valid_pages:
        return jsonify({'error': 'Invalid page value. Must be one of: {}'.format(global_future_valid_pages)}), 400
    url = "https://quote.eastmoney.com/globalfuture/" + page
    data = get_data_from_page(url)
    return jsonify({'data': data})





if __name__ == '__main__':
    app.run(debug=True)
