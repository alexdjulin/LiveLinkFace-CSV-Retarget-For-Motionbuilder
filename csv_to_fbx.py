# SOURCES
# https://re-thought.com/how-to-suppress-scientific-notation-in-pandas/
# https://stackoverflow.com/questions/28218698/how-to-iterate-over-columns-of-pandas-dataframe-to-run-regression

import pandas as pd


class BlendShape:

    def __init__(self, name, keys_dic):
        self.name = name
        self.keys_dic = keys_dic

    def __repr__(self):
        to_print = "{}\n".format(self.name)
        for key, value in self.keys_dic.items():
            to_print += "{}: {}\n".format(key, value)
        return to_print


def get_bs_data(csv_file):

    # store csv file in a dataframe
    data = pd.read_csv(csv_file)

    # round up data to get rid of scientific notation like 1.e-5 that may confuse maya/mobu
    data = data.round(4)

    # extract frames as timecode
    timecode = list()
    for value in data['Timecode'].tolist():
        timecode.append(value[:-4])

    # create list of blendshapes
    bs_data = list()
    for col_name, col_values in data.transpose().iterrows():
        bs_data.append(BlendShape(col_name, dict(zip(timecode, col_values.tolist()))))

    # get rid of the first two columns (Timecode/BlendShapeCount)
    bs_data = bs_data[2:]

    return bs_data


if __name__ == "__main":

    csv_file = r"C:\Users\natha\Desktop\csv_to_unreal\SizeTest_10_Mimic_mocap_LIVESTREAM.csv"
    bs_data = get_bs_data(csv_file)

    