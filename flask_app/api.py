import numpy as np
import pandas as pd
import pickle
from ast import literal_eval as make_tuple
import re

gbc_model = pickle.load(open('./model/gbc_model.pkl', 'rb'))
prediction_vector = pickle.load(open('./data/prediction_vector.pkl', 'rb'))
ssX_los, ssX_age = pickle.load(open('./model/scalers_los_age.pkl', 'rb'))

# The prediction vector that is loaded is initialized to all zeros. It has
# all the feature labels, and so we can use a dictionary to update the value
# for the vector based on the label.

prediction_defaults = {
    'sex_code': 'sex_code_M',
    'race': 'race_4',
    'ethnicity': 'ethnicity_2',
    'public_health_region': 'public_health_region_06',
    'first_payment_src': 'first_payment_src_MA',
    'pat_age': -0.288, # patient age was scaled and centered so it has a mean of 0. Median is -0.28
    'hiv_drug': 0,
    'type_of_admission': 'type_of_admission_1',
    'source_of_admission': 'source_of_admission_1',
    'admit_weekday': 1,
    'length_of_stay': -0.57, # patient age was scaled so that it has a mean of 0. Median is 0.17
    'hospital': 'hospital_community'
}

def make_prediction(features):
    # When make_prediction is called, make a copy of our prediction_default_dictionary and then
    # change the values according to what features the user changed.

    feature_dict = prediction_defaults.copy()

    #print(features)

    for key, value in features.items():
        if key == 'length_of_stay':
            feature_dict[key] = ssX_los.transform(np.asarray([float(value)]).reshape(-1,1))[0,0]
        elif key == 'pat_age':
            feature_dict[key] = ssX_age.transform(np.asarray([float(value)]).reshape(-1,1))[0,0]
        else:
            if "(" in value:
                value = make_tuple(value)
            feature_dict[key] = value

    print(feature_dict)

    new_prediction = prediction_vector.copy()
    # Every time make_prediction is called, we go ahead and update prediction_vector so that
    # whatever feature it is that the user changed gets updated in the prediction vector.
    # Otherwise, keep all of the defaults that prediction_vector was initialized with.
    for key, value in feature_dict.items():
        if key == 'pat_age' or key =='hiv_drug' or key == 'admit_weekday' or key == 'length_of_stay':
            new_prediction[key] = value
        else:
             new_prediction[value] = 1

    #print(new_prediction)
    #print(new_prediction[('5849', 'N')])

    X = np.asarray(new_prediction).reshape(1,-1)
    #X = np.asarray(prediction_vector).reshape(1,-1)
    print(gbc_model.predict(X))
    print(gbc_model.predict_proba(X))
    prob_survived = gbc_model.predict_proba(X)[0, 0]

    result = {
        'prediction': int(prob_survived > 0.5),
        'prob_survived': prob_survived
    }

    print(result)
    
    return result

if __name__ == '__main__':
    print(make_prediction(example))
