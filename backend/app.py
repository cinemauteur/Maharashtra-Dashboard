from flask import Flask, jsonify, request, after_this_request
import pandas as pd
import os

app = Flask(__name__)

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,OPTIONS'
    return response

# Load data once at startup
DATA_PATH = os.path.join(os.path.dirname(__file__), "Sample.xlsx")
df_raw = pd.read_excel(DATA_PATH)

# Fix column name typo if present, and standardize
df_raw.columns = df_raw.columns.str.strip()

MONTH_COLS = ['Apr-25', 'May-25', 'Jun-25', 'Jul-25', 'Aug-25', 'Sep-25', 'Oct-25', 'Nov-25', 'Dec-25']
MONTHS_LABELS = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def apply_filters(region=None, district=None, product=None):
    df = df_raw.copy()
    if region and region != "All":
        df = df[df['Region'] == region]
    if district and district != "All":
        df = df[df['District'] == district]
    if product and product != "All":
        df = df[df['Product'] == product]
    return df


@app.route('/api/filters', methods=['GET'])
def get_filters():
    return jsonify({
        "regions": ["All"] + sorted(df_raw['Region'].unique().tolist()),
        "districts": ["All"] + sorted(df_raw['District'].unique().tolist()),
        "products": ["All"] + sorted(df_raw['Product'].unique().tolist()),
    })


@app.route('/api/summary', methods=['GET'])
def get_summary():
    region = request.args.get('region', 'All')
    district = request.args.get('district', 'All')
    product = request.args.get('product', 'All')
    df = apply_filters(region, district, product)

    total = int(df['Apr-Dec,25'].sum())
    latest_month = int(df['Dec-25'].sum())
    prev_month = int(df['Nov-25'].sum())
    mom_growth = round((latest_month - prev_month) / prev_month * 100, 2) if prev_month else 0

    return jsonify({
        "total_export": total,
        "latest_month": latest_month,
        "prev_month": prev_month,
        "mom_growth": mom_growth,
        "num_districts": int(df['District'].nunique()),
        "num_products": int(df['Product'].nunique()),
    })


@app.route('/api/monthly-trend', methods=['GET'])
def get_monthly_trend():
    region = request.args.get('region', 'All')
    district = request.args.get('district', 'All')
    product = request.args.get('product', 'All')
    df = apply_filters(region, district, product)

    trend = []
    for col, label in zip(MONTH_COLS, MONTHS_LABELS):
        trend.append({"month": label, "value": int(df[col].sum())})

    return jsonify(trend)


@app.route('/api/regions', methods=['GET'])
def get_regions():
    product = request.args.get('product', 'All')
    df = apply_filters(product=product)

    result = []
    for region, grp in df.groupby('Region'):
        total = int(grp['Apr-Dec,25'].sum())
        latest = int(grp['Dec-25'].sum())
        prev = int(grp['Nov-25'].sum())
        mom = round((latest - prev) / prev * 100, 2) if prev else 0
        grand_total = int(df_raw['Apr-Dec,25'].sum())
        share = round(total / grand_total * 100, 2) if grand_total else 0
        result.append({
            "region": region,
            "total_export": total,
            "dec_export": latest,
            "nov_export": prev,
            "mom_growth": mom,
            "share": share,
        })

    result.sort(key=lambda x: x['total_export'], reverse=True)
    return jsonify(result)


@app.route('/api/districts', methods=['GET'])
def get_districts():
    region = request.args.get('region', 'All')
    product = request.args.get('product', 'All')
    df = apply_filters(region=region, product=product)

    result = []
    for district, grp in df.groupby('District'):
        total = int(grp['Apr-Dec,25'].sum())
        latest = int(grp['Dec-25'].sum())
        prev = int(grp['Nov-25'].sum())
        mom = round((latest - prev) / prev * 100, 2) if prev else 0
        grand_total = int(df_raw['Apr-Dec,25'].sum())
        share = round(total / grand_total * 100, 2) if grand_total else 0
        region_name = grp['Region'].iloc[0]
        result.append({
            "district": district,
            "region": region_name,
            "total_export": total,
            "dec_export": latest,
            "nov_export": prev,
            "mom_growth": mom,
            "share": share,
        })

    result.sort(key=lambda x: x['total_export'], reverse=True)
    return jsonify(result)


@app.route('/api/products', methods=['GET'])
def get_products():
    region = request.args.get('region', 'All')
    district = request.args.get('district', 'All')
    df = apply_filters(region=region, district=district)

    result = []
    grand_total = int(df['Apr-Dec,25'].sum())
    for product, grp in df.groupby('Product'):
        total = int(grp['Apr-Dec,25'].sum())
        share = round(total / grand_total * 100, 2) if grand_total else 0
        result.append({"product": product, "total_export": total, "share": share})

    result.sort(key=lambda x: x['total_export'], reverse=True)
    return jsonify(result[:10])


@app.route('/api/district-monthly', methods=['GET'])
def get_district_monthly():
    district = request.args.get('district', 'All')
    df = apply_filters(district=district)
    trend = []
    for col, label in zip(MONTH_COLS, MONTHS_LABELS):
        trend.append({"month": label, "value": int(df[col].sum())})
    return jsonify(trend)


if __name__ == '__main__':
    print("✅ Maharashtra Export Dashboard API running at http://localhost:5000")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False)
    
