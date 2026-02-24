#!/usr/bin/env python3
import sys, json, os, numpy as np, pickle

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

def train_and_save():
    import pandas as pd
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split

    csv_path = os.path.join(os.path.dirname(__file__), 'Housing.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Housing.csv not found at {csv_path}. Place it in the backend/ folder.")

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    df['price'] = np.log(df['price'])
    df['total_room'] = df['bedrooms'] + df['bathrooms']
    df.drop(['bedrooms', 'bathrooms'], axis=1, inplace=True)
    cols = ['mainroad','guestroom','basement','hotwaterheating','airconditioning','prefarea']
    df[cols] = df[cols].replace({'yes':1,'no':0})
    df = pd.get_dummies(df, columns=['furnishingstatus'], drop_first=True, dtype=int)
    df = pd.get_dummies(df, columns=['stories'], drop_first=True, dtype=int)

    X = df.drop('price', axis=1)
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = Pipeline([('scaler', StandardScaler()), ('model', LinearRegression())])
    pipeline.fit(X_train, y_train)

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(pipeline, f)
    return pipeline

def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    return train_and_save()

def main():
    # Strip surrounding quotes that Windows cmd may add
    arg = sys.argv[1].strip('"').strip("'")
    features = json.loads(arg)
    model = load_model()
    X = np.array(features).reshape(1, -1)
    log_price = model.predict(X)[0]
    price = np.exp(log_price)
    print(f"{price:.2f}")

if __name__ == '__main__':
    main()