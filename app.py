from flask import Flask, render_template, jsonify, request
import pandas as pd
from ml_models import *  

app = Flask(__name__)

# CSV paths for each category
CSV_PATHS = {
    'laptop': 'cleaned_laptop.csv',
    'mouse': 'cleaned_mouse.csv',
    'keyboard': 'cleaned_keyboard.csv'
}

CATEGORIES = list(CSV_PATHS.keys())

# Load data from CSV based on category
def load_df(category):
    path = CSV_PATHS.get(category)
    if path:
        return pd.read_csv(path)
    return pd.DataFrame()

@app.route('/')
def dashboard():
    return render_template('dashboard.html', categories=CATEGORIES)

@app.route('/api/top5/<cat>')
def api_top5(cat):
    df = load_df(cat).dropna(subset=['rating'])
    top5 = df.sort_values('rating', ascending=False).head(5)
    return jsonify(top5[['title', 'rating']].to_dict(orient='list'))

@app.route('/api/avg-price/<cat>')
def api_avg_price(cat):
    df = load_df(cat)
    grp = df.groupby('brand')['price'].mean().sort_values(ascending=False).head(10)
    return jsonify({'brands': grp.index.tolist(), 'prices': grp.values.round(2).tolist()})

@app.route('/api/rating-dist/<cat>')
def api_rating_dist(cat):
    df = load_df(cat).dropna(subset=['rating'])
    bins = [0, 1, 2, 3, 4, 5]
    counts = pd.cut(df['rating'], bins=bins, right=False).value_counts().sort_index()
    labels = [f"{int(iv.left)}–{int(iv.right)}" for iv in counts.index]
    return jsonify({'ranges': labels, 'counts': counts.tolist()})

@app.route('/api/discount-vs-rating/<cat>')
def api_discount_rating(cat):
    df = load_df(cat).dropna(subset=['discount', 'rating'])
    return jsonify({'discounts': df['discount'].tolist(), 'ratings': df['rating'].tolist()})

@app.route('/api/cluster/<cat>')
def api_cluster(cat):
    df = load_df(cat).dropna(subset=['price', 'rating', 'original_price', 'discount'])
    dfc, _ = apply_kmeans(df)
    out = {}
    for c in sorted(dfc['cluster'].unique()):
        sub = dfc[dfc['cluster'] == c]
        out[str(c)] = {'x': sub['price'].tolist(), 'y': sub['rating'].tolist()}
    return jsonify(out)

@app.route('/api/elbow/<cat>')
def api_elbow(cat):
    df = load_df(cat).dropna(subset=['price', 'rating'])
    k_vals, inertias = get_elbow_data(df)
    return jsonify({'k_values': k_vals, 'inertias': inertias})

@app.route('/api/lr-rating/<cat>')
def api_lr_rating(cat):
    df = load_df(cat)
    result = linear_regression_rating(df)
    return jsonify(result)

@app.route('/api/lr-price/<cat>')
def api_lr_price(cat):
    df = load_df(cat)
    result = linear_regression_price(df)
    return jsonify(result)


@app.route('/api/top-discounts/<cat>')
def api_top_discounts(cat):
    df = load_df(cat).dropna(subset=['discount'])
    top5 = df.sort_values('discount', ascending=False).head(5)
    return jsonify(top5[['title', 'discount']].to_dict(orient='list'))

@app.route('/api/max-discount/<cat>')
def api_max_discount(cat):
    df = load_df(cat)
    max_discount = df.sort_values('discount', ascending=False).head(5)
    return jsonify(max_discount[['title', 'discount']].to_dict(orient='list'))

@app.route('/api/avg-discount/<cat>')
def api_avg_discount(cat):
    df = load_df(cat)
    grp = df.groupby('brand')['discount'].mean().sort_values(ascending=False).head(10)
    return jsonify({'brands': grp.index.tolist(), 'discounts': grp.values.round(2).tolist()})

@app.route('/pricing')
def pricing():
    return render_template('pricing.html', categories=CATEGORIES)

@app.route('/ratings')
def ratings():
    return render_template('ratings.html', categories=CATEGORIES)

@app.route('/discounts')
def discounts():
    return render_template('discounts.html', categories=CATEGORIES)

@app.route('/ml')
def ml_insights():
    return render_template('ml.html', categories=CATEGORIES)

if __name__ == '__main__':
    app.run(debug=True)
