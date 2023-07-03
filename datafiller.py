import pandas as pd

def filler(df, method):
    start_date = df.index.min()
    end_date = df.index.max()
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    complete_df = pd.DataFrame(index=date_range)
    # Create missing days (holiday, weekends etc.) and linear fill
    merged_df = complete_df.merge(df, left_index=True, right_index=True, how='left')
    # Maybe time, quadratic or from_derivatives
    filled_df = merged_df.interpolate(method=method)
    return filled_df
