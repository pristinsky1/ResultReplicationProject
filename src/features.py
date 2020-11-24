import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os




def three_cols(row):
    time = list(map(int, row['packet_times'].split(';')[0:-1]))
    size = list(map(int, row['packet_sizes'].split(';')[0:-1]))
    dirs = list(map(int, row['packet_dirs'].split(';')[0:-1]))
    dict1 = {'packet_time': time, 'packet_size': size, 'packet_dir': dirs}
    return pd.DataFrame(dict1)

# This function takes all the counts of the 0-300bytes for the 1->2 Direction and all the counts
# of the 1200-1500bytes for the 2->1 Direction and creates sum values for the two features per dataset.
# uses the three_cols function as a helper function
def big_byte_count_feature(dataset):        
    packet_size_count1 = []
    packet_size_count2 = []
    for i in range(dataset.shape[0]):
        row = three_cols(dataset.iloc[i])
        ones = row.loc[row['packet_dir'] == 1]['packet_size']
        twos = row.loc[row['packet_dir'] == 2]['packet_size']
        one_count=0
        two_count=0
        for packet in ones:
            if (int(packet) >= 0) and (int(packet) <= 300):
                one_count += 1
        for packet in twos:
            if (int(packet) >= 1200) and (int(packet) <= 1500):
                two_count += 1
        packet_size_count1.append(one_count)
        packet_size_count2.append(two_count)
    return [sum(packet_size_count1), sum(packet_size_count2)]
  
  
  # input: filepaths
# output: 4 lists -> associated file names, labels, feature1, feature2
# uses the big_byte_count_feature as a helper function
def features_labels(files):
    Dir1_ByteCount_0to300_feature = []
    Dir2_ByteCount_1200to1500_feature = []
    labels = []
    file_names = []
    for file in files:
        if ('novpn' in file) or (file[:2] == '._'):
            continue
        if 'novideo' in file:
            labels.append(0)
        else:
            labels.append(1)
        file_names.append(file)
        df = pd.read_csv('/teams/DSC180A_FA20_A00/b05vpnxray/data/unzipped/' + file)
        sum_values = big_byte_count_feature(df)
        Dir1_ByteCount_0to300_feature.append(sum_values[0])
        Dir2_ByteCount_1200to1500_feature.append(sum_values[1])
    feature_df = pd.DataFrame(data={'Dir1_ByteCount_0to300_feature': Dir1_ByteCount_0to300_feature,
                                    'Dir2_ByteCount_1200to1500_feature': Dir2_ByteCount_1200to1500_feature})
    return file_names, labels, feature_df 

# accesses the data file found within the data folder and creates the features and label for it
# uses the big_byte_count_feature as a helper function
def input_feature_label():
    Dir1_ByteCount_0to300_feature = []
    Dir2_ByteCount_1200to1500_feature = []
    labels = []
    file_names = []
    filepath = "data"
    files = os.listdir(filepath)
    for file in files:
        if ('novpn' in file) or (file[:2] == '._'):
            return "File Invalid. Must be vpn data, nor can it be empty."
        if 'novideo' in file:
            labels.append(0)
        else:
            labels.append(1)
        file_names.append(file)
        df = pd.read_csv('data/' + file)
        sum_values = big_byte_count_feature(df)
        Dir1_ByteCount_0to300_feature.append(sum_values[0])
        Dir2_ByteCount_1200to1500_feature.append(sum_values[1])
    feature_df = pd.DataFrame(data={'Dir1_ByteCount_0to300_feature': Dir1_ByteCount_0to300_feature,
                                    'Dir2_ByteCount_1200to1500_feature': Dir2_ByteCount_1200to1500_feature})
    return file_names, labels, feature_df

  
  #Trains the model on all the data found within the GoodData on dsmlp, and then predicts 
#whether streaming or not for the input data chunk entered
def ml_model_train(X, y, input_X, input_y):
    model = RandomForestClassifier()
    model = model.fit(X[['Dir1_ByteCount_0to300_feature','Dir2_ByteCount_1200to1500_feature']],y)
    prediction = model.predict(input_X[['Dir1_ByteCount_0to300_feature','Dir2_ByteCount_1200to1500_feature']])
    if prediction == 1:
        val = True
    else:
        val = False
    return ("Prediction Value: " + str(prediction[0]), "True Value: " + str(input_y[0]), 'is_streaming? : ' + str(val))
