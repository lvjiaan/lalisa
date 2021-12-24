import pandas as pd

sheet = pd.read_excel('E:\\a_t2.xlsx', sheet_name='a_t2')

if __name__ == '__main__':
    # 指定第一列为行索引
    result = pd.read_excel('E:\\a_t2.xlsx', sheet_name='a_t2', index_col=0)


    set1 = set(sheet['apply_num'].values)
    print(len(set1))
    print(len(sheet['apply_num'].values))

    # for data in sheet:
    #     print(data.)
