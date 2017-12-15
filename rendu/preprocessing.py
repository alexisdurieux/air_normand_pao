import sys
import os
import pandas as pd
import argparse




NORMALIZED_COLUMN_NAMES = {
    '# date': 'date',
    'Temp': 'temp',
    'RH': 'rh',
    'Tgrad': 't_grad',
    'Patm': 'pressure',
    'Pluvio': 'pluvio',
    '#ref': 'ref',
    '#61FD': 'NO2_61FD',
    '#61F0': 'NO2_61F0',
    '#61EF': 'NO2_61EF',
}

NO2_FILENAME = "AllNO2_QH.csv"
ENV_FILENAME = "Env_QH.csv"


def clean(filename):
    """ Process a csv file taking into account the COLUMN_NAMES dictionnary
    :param filename:
    :return:
    """
    if os.path.isdir(filename):
        list_csv = [os.path.join(filename, name) for name in os.listdir(filename) if name.split('.')[-1] == "csv"]
    else:
        list_csv = [filename]
    for csv_file in list_csv:
        try:
            df = pd.read_csv(csv_file, encoding='utf-8', delimiter=';')
        except UnicodeEncodeError:
            df = pd.read_csv(csv_file, encoding='ISO-8859-1', delimiter=';')

        df = df.rename(columns=NORMALIZED_COLUMN_NAMES)
        df.to_csv(csv_file, sep=';', encoding="utf-8", index=False)
        print("{} cleaned with success !".format(csv_file))


def create_no2_pkl(folder, out_pickle):
    """
    :param folder: path of the folder containing the NO2 and ENV csv inputs file
    :param out_pickle: path of the output pickle file
    :return:
    """
    if not os.path.isdir(folder):
        raise NotADirectoryError
    no2_filename = os.path.join(folder, NO2_FILENAME)
    env_filename = os.path.join(folder, ENV_FILENAME)

    df_no2 = pd.read_csv(no2_filename, encoding='utf-8', delimiter=';')
    df_env = pd.read_csv(env_filename, encoding='utf-8', delimiter=';')

    df_env = df_env.set_index('date').T

    out_df = pd.DataFrame(columns=['date', 'ref', 'NO2_61FD', 'NO2_61F0', 'NO2_61EF', 'rh', 't_grad', 'pressure',
                                   'temp', 'pluvio'])

    for i in range(len(df_no2)):
        row = df_no2.iloc[i]
        date = row.date
        env = df_env[date]
        rh = env.rh if 'rh' in env else 'NA'
        t_grad = env.t_grad if 't_grad' in env else 'NA'
        pressure = env.pressure if 'pressure' in env else 'NA'
        pluvio = env.pluvio if 'pluvio' in env else 'NA'
        temp = env.temp if 'temp' in env else 'NA'

        out_df.loc[i] = [date, row.ref, row.NO2_61FD, row.NO2_61F0, row.NO2_61EF, rh, t_grad, pressure,
                         temp, pluvio]

    out_df.to_pickle(out_pickle)


def normalize_pickle(input_pickle, output_pickle):
    df = pd.read_pickle(input_pickle)

    df = df[pd.notnull(df).all(axis=1)]
    tmp_df = df[['NO2_61FD', 'NO2_61F0', 'NO2_61EF', 'rh', 't_grad', 'pressure', 'temp']]
    normalized_df = (tmp_df - tmp_df.mean()) / tmp_df.std()
    df[['NO2_61FD', 'NO2_61F0', 'NO2_61EF', 'rh', 't_grad', 'pressure', 'temp']] = normalized_df

    df.to_pickle(output_pickle)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("clean", help="clean a csv file")

    args = parser.parse_args()
    print(args)
    args = sys.argv
    if len(args) < 2:
        print("Not enough arguments")
    elif len(args) < 3:
        if args[1] == "clean":
            print("Please input a csv file")
        else:
            print("Unknown command")
    else:
        if args[1] == "clean":
            clean(args[2])
        elif args[1] == "create_pickle":
            if len(args) < 4:
                print("Pickle out or folder input missing")
            else:
                folder = args[2]
                pickle_name = args[3]
                create_no2_pkl(folder, pickle_name)
        elif args[1] == "normalize_pickle":
            if len(args) < 4:
                print("Pickle out or folder input missing")
            else:
                folder = args[2]
                pickle_name = args[3]
                normalize_pickle(folder, pickle_name)
        else:
            print("Unknown command")


if __name__ == '__main__':
    main()
