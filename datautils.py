import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error


def calculate_cross_correlation(df):
    columns = df.columns
    num_columns = len(columns)

    # Initialize a DataFrame to store the results
    result_df = pd.DataFrame(columns=['Column 1', 'Column 2', 'Max Correlation', 'Lag'])

    # Calculate cross-correlation between all column pairs
    for i in range(num_columns):
        for j in range(i+1, num_columns):
            column1 = columns[i]
            column2 = columns[j]

            max_corr = 0.0
            lag = None

            # Iterate over different lag values
            for l in range(15):
                # Drop the first l rows from both columns
                dropped_df = df[l:].reset_index(drop=True)
                dropped_column2 = dropped_df[column2]

                # Calculate cross-correlation using pandas corr function
                cross_corr = dropped_df[column1].corr(dropped_column2)

                # Update the maximum correlation and lag if necessary
                if abs(cross_corr) > abs(max_corr):
                    max_corr = cross_corr
                    lag = l

            # Append the result to the DataFrame
            result_df = result_df.append({'Column 1': column1, 'Column 2': column2,
                                          'Max Correlation': max_corr, 'Lag': lag}, ignore_index=True)

    return result_df


def col_shifter(df,target, shift):
    # Select the column to be shifted
    column_to_shift = target
    shifted_column_name = column_to_shift + '_shifted'
    # Shift the selected column by one row
    df[shifted_column_name] = df[column_to_shift].shift(shift)
    # Reorder the columns with the shifted column inserted at the beginning
    shifted_column_index = df.columns.get_loc(shifted_column_name)
    df = pd.concat(
        [df.iloc[:, shifted_column_index], df.iloc[:, :shifted_column_index], df.iloc[:, shifted_column_index + 1:]],
        axis=1)
    # Drop the first row since the shifted value is NaN
    df = df.dropna()

    return df


def splitter(X,y,test_size=0.3, isTimeseries=False):

    if isTimeseries:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size)
    return X_train, X_test, y_train, y_test


def get_scaler(scaler_name, X):
    if scaler_name == 'StandardScaler':
        scaler = StandardScaler()
    elif scaler_name == 'MinMaxScaler':
        scaler = MinMaxScaler()
    elif scaler_name == 'RobustScaler':
        scaler = RobustScaler()
    elif scaler_name == 'MaxAbsScaler':
        scaler = MaxAbsScaler()
    else:
        raise ValueError(f"Invalid scaler name: {scaler_name}")

    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
    return X_scaled_df, scaler


def calculate_regression_metrics(y_true, y_pred):
    metrics = {}

    metrics['Mean Absolute Error (MAE)'] = mean_absolute_error(y_true, y_pred)
    metrics['Mean Squared Error (MSE)'] = mean_squared_error(y_true, y_pred)
    metrics['Root Mean Squared Error (RMSE)'] = mean_squared_error(y_true, y_pred, squared=False)
    metrics['R-squared (R2)'] = r2_score(y_true, y_pred)
    metrics['Mean Absolute Percentage Error (MAPE)'] = 100 * mean_absolute_percentage_error(y_true, y_pred)
    metrics_df = pd.DataFrame(metrics, index=[0])
    return metrics_df
