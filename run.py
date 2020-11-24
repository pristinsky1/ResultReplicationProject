import sys
import os
import json
sys.path.insert(0, 'src')
from features import features_labels

def main(targets):
    '''
    Runs the main project pipeline logic, given the targets.
    main runs the targets in order of data=>analysis=>model
    '''
    
    if 'test' in targets:
        with open('config/test-params.json') as fh:
            feature_cfg = json.load(fh)
            
            
            # make the data target
            file_names, file_labels, new_df = features_labels(**feature_cfg)
            print("Created the new features!")
            print(The associated file names are: " + file_names)
            print(The associated file labels are: " + file_labels)
    return new_df

if __name__=='__main__':
    #run via:
    targets = sys.argv[1:]
    main(targets)
