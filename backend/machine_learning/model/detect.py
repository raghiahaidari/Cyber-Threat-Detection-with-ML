from joblib import load
from sklearn.preprocessing import StandardScaler
from pandas import DataFrame

def classify_traffic(df, model_path):
    # extract features and target
    target_columns = ['status']
    X = df.drop(target_columns, axis = 1).values
    df = df.fillna(0)
    df = df.astype(float)

    # preprocess the data
    scaler = StandardScaler()
    scaler.fit(X)
    X_scaled = scaler.transform(X)

    # load the model
    model = load(model_path)
    predictions = model.predict(X_scaled)

    # return the predictions in a new dataframe (number, status)
    res_df = DataFrame(predictions, columns = ['status'])
    res_df['status'] = res_df['status'].apply(lambda x: 'normal' if x == 0 else 'ddos')

    return res_df
