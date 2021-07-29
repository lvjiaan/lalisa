import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlalchemy


def get_detail(driver, title_name):
    driver.get(r'E:\en_20210101_html/{name}.htm#{name}'.format(name=title_name))
    start = str(str(title_name)[0:1])
    rows = []

    details = driver.find_elements_by_css_selector("[role='row']")
    for row in details:
        ipc = {}
        name = row.find_elements_by_class_name('symbol')
        aa = row.find_elements_by_class_name("l1")
        if len(aa) > 0:
            tag = aa[0].text
            if tag.__contains__('(trans'):
                continue
        if len(name) <= 0:
            continue
        if len(name) > 0:
            ipc['codeId'] = name[0].text

        if len(aa) > 0:
            tag = aa[0].text
            ipc['desc'] = tag
        rows.append(ipc)
    results = []
    tier = 1
    for row in rows:
        result = {}
        if row['codeId'].__contains__('/'):
            result['codeId'] = str(row['codeId']).replace(' ', '')
            result['desc'] = row['desc']
            result['tier'] = row['desc'].count("•") + tier
            # results.append(result)
        else:
            result['codeId'] = str(row['codeId']).replace(' ', '')
            result['desc'] = row['desc']
            result['tier'] = tier
            # results.append(result)
            tier = tier + 1
        #parentid 加工
        for j in range(len(results) - 1, -1, -1):
            if int(results[j]['tier']) == int(result['tier']) - 1:
                result['parentId'] = results[j]['codeId']
                break
        results.append(result)
    return_results = pd.DataFrame(results)
    return driver, return_results


def test():
    chromedriver_path = r"./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chromedriver_path)
    driver.get(r'E:\en_20210101_html/index.htm')
    details = driver.find_elements_by_css_selector("[role='row']")
    list_main_head = []
    list_detail_head = []
    list_details = []
    for row in details:
        name = row.find_elements_by_class_name('symbol')
        if len(name) > 0:
            list_main_head.append(name[0].text)
    for main_detail in list_main_head:
        driver.get(r'E:\en_20210101_html/{name}.htm'.format(name=main_detail))
        details = driver.find_elements_by_css_selector("[role='row']")
        for row in details:
            name = row.find_elements_by_class_name('symbol')
            if len(name) > 0:
                if len(name[0].text) > 1:
                    list_detail_head.append(name[0].text)
    for detail_head in list_detail_head:
        driver.get(r'E:\en_20210101_html/{name}.htm'.format(name=detail_head))
        details = driver.find_elements_by_css_selector("[role='row']")
        for row in details:
            name = row.find_elements_by_class_name('symbol')
            if len(name) > 0:
                if len(name[0].text) > 3:
                    list_details.append(name[0].text)
    return driver, list_details


if __name__ == '__main__':
    # driver, list_details = test()
    # engin = sqlalchemy.create_engine("mssql+pymssql://sa:zhangxueyang2021@192.168.4.187:1433/Lvjiaan")
    # for detail in list_details:
    #     print(detail)
    #     driver, results = get_detail(driver, detail)
    #     results.to_sql("CT_IPC", con=engin, index=False, if_exists='append')
    # driver.quit()
    chromedriver_path = r"./chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chromedriver_path)
    driver, results = get_detail(driver, 'A23B')
    engin = sqlalchemy.create_engine("mssql+pymssql://sa:wlzx87811024@172.16.5.45:1433/Lvjiaan")
    results.to_sql("CT_IPC2", con=engin, index=False, if_exists='append')
    driver.quit()
