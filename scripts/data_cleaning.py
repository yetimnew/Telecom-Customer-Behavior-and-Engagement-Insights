# data_cleaning.py

import pandas as pd
import os

def detect_outliers(data, columns=None):
    """
    Detects outliers in the entire DataFrame or specified columns using the Interquartile Range (IQR) method.

    Args:
        data (pd.DataFrame): The input DataFrame.
        columns (str or list, optional): Specific column(s) to check for outliers.
                                         If None, checks all numeric columns in the DataFrame.

    Returns:
        pd.DataFrame: A DataFrame with outliers for the specified columns or the entire DataFrame.
    """
    if isinstance(columns, str):  # If a single column is passed as a string
        columns = [columns]

    if columns is None:  # If no columns are specified, select all numeric columns
        columns = data.select_dtypes(include=['number']).columns
    elif not isinstance(columns, list):  # Ensure columns is a list
        raise ValueError("Columns must be a string, list, or None.")

    outliers_data = pd.DataFrame()  # To store all outliers for specified columns

    for column in columns:
        if column not in data.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame.")

        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Get outliers for the column
        outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
        print(f"\nOutliers in {column}: {len(outliers)}")

        # Append outliers for this column to the combined DataFrame
        outliers_data = pd.concat([outliers_data, outliers])

    # Drop duplicates if the same rows appear for multiple columns
    outliers_data = outliers_data.drop_duplicates()

    return outliers_data

def handle_missing_values(data, strategy="mean", columns=None):
    """
    Handles missing values in the dataset or specific columns.

    Args:
        data (pd.DataFrame): The input DataFrame.
        strategy (str): The strategy to handle missing values ('mean', 'median', 'drop').
        columns (list or str, optional): Column(s) to handle missing values. If None, applies to the entire dataset.

    Returns:
        pd.DataFrame: The DataFrame with missing values handled.
    """
    # Remove leading and trailing spaces from column names
    data.columns = data.columns.str.strip()

    if columns is None:
        # Apply the strategy to the entire dataset
        if strategy == "mean":
            return data.fillna(data.mean())
        elif strategy == "median":
            return data.fillna(data.median())
        elif strategy == "drop":
            return data.dropna()
        else:
            raise ValueError("Invalid strategy. Choose from 'mean', 'median', or 'drop'.")
    else:
        # Apply the strategy to specific column(s)
        if isinstance(columns, str):  # Convert single column string to a list
            columns = [columns]

        if not all(col in data.columns for col in columns):
            raise ValueError("One or more columns not found in the DataFrame.")

        for column in columns:
            if strategy == "mean":
                data[column] = data[column].fillna(data[column].mean())
            elif strategy == "median":
                data[column] = data[column].fillna(data[column].median())
            elif strategy == "drop":
                data = data.dropna(subset=columns)
            else:
                raise ValueError("Invalid strategy. Choose from 'mean', 'median', or 'drop'.")

        return data
def remove_duplicates(data):
    """
    Removes duplicate rows from the dataset.

    Args:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame without duplicates.
    """
    before = data.shape[0]
    data = data.drop_duplicates()
    after = data.shape[0]
    print(f"Removed {before - after} duplicate rows.")
    return data

def standardize_column_names(data):
    """
    Standardizes column names by making them lowercase and replacing spaces with underscores.

    Args:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with standardized column names.
    """
    data.columns = data.columns.str.lower().str.replace(" ", "_")
    print("Column names standardized.")
    return data

def save_outliers(outlier_dict, folder_path="outliers"):
    """
    Saves the outlier DataFrames to CSV files in a specified folder.

    Args:
        outlier_dict (dict): A dictionary where keys are column names and values are DataFrames of outliers.
        folder_path (str): Path to the folder where CSV files will be saved.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for column, outliers in outlier_dict.items():
        if not outliers.empty:
            file_path = os.path.join(folder_path, f"{column}_outliers.csv")
            outliers.to_csv(file_path, index=False)
            print(f"Outliers for {column} saved to {file_path}")
def check_duplicates_by_column(data, column_name):
    """
    Checks for duplicates in a specific column of a DataFrame and returns the number of duplicate values.

    Args:
        data (pd.DataFrame): The input DataFrame.
        column_name (str): The column name to check for duplicates.

    Returns:
        int: The number of duplicate values in the specified column.
    """
    if column_name not in data.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")
    
    # Count duplicates in the specified column
    duplicate_count = data[column_name].duplicated().sum()
    
    print(f"Number of duplicate values in column '{column_name}': {duplicate_count}")
    return duplicate_count
def calculate_duplicate_percentage(data, column_name):
    # Count the total number of rows
    total_rows = len(data)
    
    # Count the number of duplicate rows for the specified column
    duplicate_rows = data[column_name].duplicated().sum()
    
    # Calculate the percentage of duplicates
    duplicate_percentage = (duplicate_rows / total_rows) * 100
    
    return duplicate_percentage
def retain_relevant_columns(data, columns):
    """
    Retains only the specified columns in the DataFrame.

    Args:
        data (pd.DataFrame): The input DataFrame.
        columns (list): List of column names to retain.

    Returns:
        pd.DataFrame: The DataFrame with only the specified columns.
    """
    return data[[col for col in columns if col in data.columns]]
def add_total_data_volume(data, dl_column="total_dl__bytes", ul_column="total_ul__bytes"):
    """
    Adds a derived column for total data volume (DL + UL).

    Args:
        data (pd.DataFrame): The input DataFrame.
        dl_column (str): The column name for download data volume.
        ul_column (str): The column name for upload data volume.

    Returns:
        pd.DataFrame: The DataFrame with a new column 'total_data_volume'.
    """
    if dl_column not in data.columns or ul_column not in data.columns:
        raise ValueError("DL or UL column not found in the DataFrame.")
    
    data["total_data_volume"] = data[dl_column] + data[ul_column]
    return data
def add_total_data_volume(data, dl_column="total_dl__bytes", ul_column="total_ul__bytes"):
    """
    Adds a derived column for total data volume (DL + UL).

    Args:
        data (pd.DataFrame): The input DataFrame.
        dl_column (str): The column name for download data volume.
        ul_column (str): The column name for upload data volume.

    Returns:
        pd.DataFrame: The DataFrame with a new column 'total_data_volume'.
    """
    if dl_column not in data.columns or ul_column not in data.columns:
        raise ValueError("DL or UL column not found in the DataFrame.")
    
    data["total_data_volume"] = data[dl_column] + data[ul_column]
    return data
def rename_columns(data, rename_map):
    """
    Renames columns based on a provided mapping.

    Args:
        data (pd.DataFrame): The input DataFrame.
        rename_map (dict): Dictionary mapping old column names to new names.

    Returns:
        pd.DataFrame: The DataFrame with renamed columns.
    """
    return data.rename(columns=rename_map, inplace=False)
def handle_missing_values_in_columns(data, strategy="mean", columns=None):
    """
    Handles missing values in specific columns using a specified strategy.

    Args:
        data (pd.DataFrame): The input DataFrame.
        strategy (str): Strategy to handle missing values ('mean', 'median', 'drop').
        columns (list): List of columns to handle missing values. If None, applies to all.

    Returns:
        pd.DataFrame: The DataFrame with missing values handled.
    """
    return handle_missing_values(data, strategy=strategy, columns=columns)