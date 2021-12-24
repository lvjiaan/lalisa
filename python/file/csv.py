import pandas as pd









if __name__ == '__main__':

    data = pd.read_csv('E:\\1.csv')



    for index, row in data.iterrows():
        print(row['json'])
