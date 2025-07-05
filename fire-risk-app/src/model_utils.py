# Imports
import pandas as pd


def get_data_for_month(df_fires_history_risk, month):
    """
    Filter the historical fire risk DataFrame for a given month (YYYY-MM format)
    and prepare features and labels.

    Args:
        df_fires_history_risk (pd.DataFrame): Fire risk data.
        month (str): Target month in 'YYYY-MM' format.

    Returns:
        X_data_month (pd.DataFrame): Features for the month.
        y_data_month_true (pd.Series): True labels for fire risk.
    """
    # Ensure NEXT_MONTH_END is datetime
    df = df_fires_history_risk.copy()
    df['NEXT_MONTH_END'] = pd.to_datetime(df['NEXT_MONTH_END'])

    # Filter rows where year-month matches input
    df = df[df['NEXT_MONTH_END'].dt.strftime('%Y-%m') == month].set_index('GRID_ID')

    # Extract features and true labels
    X_data_month = df.drop(columns=['CURRENT_MONTH_END', 'NEXT_MONTH_END', 'RISK_NEXT_MONTH'])
    y_data_month_true = df['RISK_NEXT_MONTH']

    return X_data_month, y_data_month_true


def predict_fire_risk(X_data, y_data_true, model):
    """
    Predict fire risk using a trained model and format the result as a pandas Series.

    Args:
        X_data (pd.DataFrame): Feature data.
        y_data_true (pd.Series): True labels, used to match the index.
        model: Trained predictive model with a `.predict()` method.

    Returns:
        y_data_pred (pd.Series): Predicted fire risk, aligned with input index.
    """
    # Generate predictions using the model
    y_data_pred = model.predict(X_data)

    # Convert predictions to pandas Series with correct index
    y_data_pred = pd.Series(y_data_pred, index=y_data_true.index, name='RISK_NEXT_MONTH')

    return y_data_pred