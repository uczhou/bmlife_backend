import pandas as pd


def parseData(filename, outfilename=None):

    if filename.endswith('.xlsx'):
        data = pd.read_excel(filename)
    elif filename.endswith('.csv'):
        data = pd.read_csv(filename)
    else:
        raise Exception('File Type Not Supported: file should be xlsx or csv')

    df_key = ['year', 'make', 'model', 'trim', 'msrp', 'sale_price', 'rebate', 'res', 'money_factor', 'term',
              'yearly_mileage', 'payment', 'due', 'deposit']

    df_data = [[] for _ in range(data.shape[1])]

    for index, row in data.iterrows():
        if pd.isnull(row[0]):
            continue

        for i in range(row.shape[0]):
            if not pd.isnull(row[i]):
                df_data[i].append(row[i])
            else:
                if i == 6:
                    df_data[i].append(0)
                if i == 9:
                    df_data[i].append(36)
                if i == 10:
                    df_data[i].append(10000)
                if i == 12:
                    df_data[i].append('1st+plates+doc')
                if i == 13:
                    df_data[i].append(0)

    df_dict = {}

    for i in range(len(df_key)):
        # print(len(df_data))
        df_dict[df_key[i]] = df_data[i]

    car_df = pd.DataFrame.from_dict(df_dict)
    if outfilename:
        car_df.to_csv(outfilename.split('.')[0]+'.csv', index=False)
    else:
        car_df.to_csv(filename.split('.')[0] + '_cleaned.csv', index=False)
    return car_df
