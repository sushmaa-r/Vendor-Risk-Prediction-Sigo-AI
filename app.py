from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# LOAD MODELS

lr_model = joblib.load(
    "logistic_model.pkl"
)

rf_model = joblib.load(
    "random_forest_model.pkl"
)

# HOME PAGE

@app.route('/')
def home():

    return render_template(
        'home.html',
        active_page='home'
    )

# PREDICT PAGE

@app.route('/predict_page')
def predict_page():

    return render_template(
        'predict.html',
        active_page='predict'
    )

# DASHBOARD PAGE

@app.route('/dashboard')
def dashboard():

    total_vendors = 10000

    high_risk = 8022

    low_risk = 1978

    avg_rating = 3.8

    return render_template(

        'dashboard.html',

        active_page='dashboard',

        total_vendors=total_vendors,

        high_risk=high_risk,

        low_risk=low_risk,

        avg_rating=avg_rating
    )

# ABOUT PAGE

@app.route('/about')
def about():

    return render_template(
        'about.html',
        active_page='about'
    )

# PREDICTION ROUTE

@app.route('/predict', methods=['POST'])

def predict():

    Years_In_Business = float(
        request.form['Years_In_Business']
    )

    Total_Orders = float(
        request.form['Total_Orders']
    )

    Delivered_Orders = float(
        request.form['Delivered_Orders']
    )

    Returned_Orders = float(
        request.form['Returned_Orders']
    )

    Delayed_Orders = float(
        request.form['Delayed_Orders']
    )

    Disputed_Orders = float(
        request.form['Disputed_Orders']
    )

    Avg_Delivery_Days = float(
        request.form['Avg_Delivery_Days']
    )

    Rating = float(
        request.form['Rating']
    )

    Product_Quality_Score = float(
        request.form['Product_Quality_Score']
    )

    Response_Time_Hours = float(
        request.form['Response_Time_Hours']
    )

    Refund_Rate = float(
        request.form['Refund_Rate']
    )

    Contract_Value = float(
        request.form['Contract_Value']
    )

    Vendor_Category = request.form[
        'Vendor_Category'
    ]

    # CALCULATED FEATURES

    delivery_delay_rate = (
        Delayed_Orders / Total_Orders
    )

    return_rate = (
        Returned_Orders / Total_Orders
    )

    dispute_rate = (
        Disputed_Orders / Total_Orders
    )

    # CATEGORY VARIABLES

    Vendor_Category_Chemicals = 0

    Vendor_Category_Electronics = 0

    Vendor_Category_Food_Beverage = 0

    Vendor_Category_IT_Hardware = 0

    Vendor_Category_IT_IS = 0

    Vendor_Category_Machinery = 0

    Vendor_Category_Office = 0

    Vendor_Category_Office_Supplies = 0

    Vendor_Category_Packaging = 0

    Vendor_Category_Raw_Materials = 0

    Vendor_Category_Textiles = 0

    # CATEGORY ENCODING

    if Vendor_Category == "Chemicals":

        Vendor_Category_Chemicals = 1

    elif Vendor_Category == "Electronics":

        Vendor_Category_Electronics = 1

    elif Vendor_Category == "Food & Beverage":

        Vendor_Category_Food_Beverage = 1

    elif Vendor_Category == "IT Hardware":

        Vendor_Category_IT_Hardware = 1

    elif Vendor_Category == "IT/IS":

        Vendor_Category_IT_IS = 1

    elif Vendor_Category == "Machinery":

        Vendor_Category_Machinery = 1

    elif Vendor_Category == "Office":

        Vendor_Category_Office = 1

    elif Vendor_Category == "Office Supplies":

        Vendor_Category_Office_Supplies = 1

    elif Vendor_Category == "Packaging":

        Vendor_Category_Packaging = 1

    elif Vendor_Category == "Raw Materials":

        Vendor_Category_Raw_Materials = 1

    elif Vendor_Category == "Textiles":

        Vendor_Category_Textiles = 1

    # CREATE DATAFRAME

    final_features = pd.DataFrame([[

        Years_In_Business,
        Total_Orders,
        Delivered_Orders,
        Returned_Orders,
        Delayed_Orders,
        Disputed_Orders,
        Avg_Delivery_Days,
        Rating,
        Product_Quality_Score,
        Response_Time_Hours,
        Refund_Rate,
        Contract_Value,
        delivery_delay_rate,
        return_rate,
        dispute_rate,

        Vendor_Category_Chemicals,
        Vendor_Category_Electronics,
        Vendor_Category_Food_Beverage,
        Vendor_Category_IT_Hardware,
        Vendor_Category_IT_IS,
        Vendor_Category_Machinery,
        Vendor_Category_Office,
        Vendor_Category_Office_Supplies,
        Vendor_Category_Packaging,
        Vendor_Category_Raw_Materials,
        Vendor_Category_Textiles

    ]], columns=[

        'Years_In_Business',
        'Total_Orders',
        'Delivered_Orders',
        'Returned_Orders',
        'Delayed_Orders',
        'Disputed_Orders',
        'Avg_Delivery_Days',
        'Rating',
        'Product_Quality_Score',
        'Response_Time_Hours',
        'Refund_Rate',
        'Contract_Value',
        'delivery_delay_rate',
        'return_rate',
        'dispute_rate',

        'Vendor_Category_Chemicals',
        'Vendor_Category_Electronics',
        'Vendor_Category_Food & Beverage',
        'Vendor_Category_IT Hardware',
        'Vendor_Category_IT/IS',
        'Vendor_Category_Machinery',
        'Vendor_Category_Office',
        'Vendor_Category_Office Supplies',
        'Vendor_Category_Packaging',
        'Vendor_Category_Raw Materials',
        'Vendor_Category_Textiles'

    ])

    # LOGISTIC REGRESSION PROBABILITY

    probability = lr_model.predict_proba(
        final_features
    )

    # RANDOM FOREST PREDICTION

    prediction = rf_model.predict(
        final_features
    )

    # RISK LABEL

    risk = (
        "High Risk"
        if prediction[0] == 1
        else "Low Risk"
    )

    # RETURN RESULT

    return render_template(

        "predict.html",

        active_page='predict',

        prediction_text=f'Risk Level: {risk}',

        probability_text=f'Failure Probability: {probability[0][1]*100:.2f}%',

        probability_value=round(
            probability[0][1]*100,
            2
        ),

        form_data=request.form
    )

# RUN APP

if __name__ == "__main__":

    app.run(debug=True)