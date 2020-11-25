import sys
import os
import json
import pandas as pd
sys.path.insert(0, 'src')
from features import features_labels

def main(targets):
    '''
    Given the targets, main runs the main project pipeline logic.
    '''
    
    if 'test' in targets:
        with open('config/test-params.json') as test_params:
            feature_cfg = json.load(test_params)
            
            
            # make the data target
            file_names, file_labels, new_df = features_labels(**feature_cfg)
            new_df.to_csv("test/output/test_output.csv")
            print("The associated file names are: ") 
            print(file_names)
            print("The associated file labels are: ") 
            print(file_labels)
            print("Created the new features! Check folder test/output/ and observe the output features csv file!")
            print(new_df)
    return

if __name__=='__main__':
    #run via:
    targets = sys.argv[1:]
    main(targets)
