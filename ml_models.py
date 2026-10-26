from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# KMeans model with 3 clusters (default)
def apply_kmeans(data, n_clusters=3):
    numeric_data = data[['price', 'original_price', 'discount', 'rating']].dropna()
    model = KMeans(n_clusters=n_clusters, random_state=42)
    model.fit(numeric_data)
    data['cluster'] = model.labels_
    return data, model.inertia_

# Elbow method to find optimal number of clusters

def get_elbow_data(data, max_k=10):
    inertia_values = []
    k_values = list(range(1, max_k + 1))  # Trying k from 1 to max_k

    for k in k_values:
        model = KMeans(n_clusters=k, random_state=42)
        model.fit(data[['price', 'original_price', 'discount', 'rating']])  # Using relevant columns
        inertia_values.append(model.inertia_)  # Inertia is the sum of squared distances of samples to their closest cluster center

    return k_values, inertia_values

def linear_regression_rating(data):
    df = data[['price', 'original_price', 'discount', 'rating']].dropna()

    X = df[['price', 'original_price', 'discount']]
    y = df['rating']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    return {
        'mse': mean_squared_error(y_test, y_pred),
        'r2': r2_score(y_test, y_pred),
        'coefficients': model.coef_.tolist(),
        'intercept': model.intercept_
    }

def linear_regression_price(data):
    df = data[['original_price', 'discount', 'rating', 'price']].dropna()

    X = df[['original_price', 'discount', 'rating']]
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    return {
        'mse': mean_squared_error(y_test, y_pred),
        'r2': r2_score(y_test, y_pred),
        'coefficients': model.coef_.tolist(),
        'intercept': model.intercept_
    }
