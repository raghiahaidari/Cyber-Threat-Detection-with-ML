import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from joblib import dump

def status_to_int(s):
	if (s == 'normal'): return 0
	if (s == 'ddos'): return 1

# read combined dataframes
df_normal = pd.read_csv('../data/batches/normal.csv')
df_ddos = pd.read_csv('../data/batches/ddos.csv')

# combine dataframes
df = [df_normal, df_ddos]
df = pd.concat(df, ignore_index = True)

# fill NaN values with 0
df = df.fillna(0)

# convert string classes to int
df['status'] = df['status'].apply(status_to_int)

# extract features and target
target_columns = ['status']
X = df.drop(target_columns, axis = 1).values
y = df[target_columns].values

# convert dtype to int
X = X.astype(float)
y = y.astype(float)

# split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y)

# data preprocessing
scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# train the model
forest = RandomForestClassifier(n_estimators=10)
forest.fit(X_train_scaled, y_train.ravel())

# save the model to the disk
filename = '../model.sav'
dump(forest, filename)
