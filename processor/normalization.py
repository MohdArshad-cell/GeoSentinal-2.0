import pandas as pd
import numpy as np

class GeoNormalization:
    def __init__(self, window_days=1095):
        """
        PDF Section 5.1: 36-month (approx. 1095 days) rolling window normalization.
        """
        self.window = window_days

    def apply_rolling_min_max(self, df, column_name):
        """
        Formula: Score_norm = (Score_t - min_36m) / (max_36m - min_36m)
        Ye formula ensure karta hai ki 1.0 hamesha peak tension ko represent kare 
        relative to the recent past[cite: 201, 209].
        """
        # Rolling min aur max calculate karna (pichle 36 mahino ka)
        rolling_min = df[column_name].rolling(window=self.window, min_periods=1).min()
        rolling_max = df[column_name].rolling(window=self.window, min_periods=1).max()
        
        # Denominator zero na ho, iska check
        denominator = rolling_max - rolling_min
        
        # Min-Max Normalization logic [cite: 201]
        normalized_series = (df[column_name] - rolling_min) / denominator
        
        # Agar denominator 0 hai (yani min aur max same hain), toh value 0 set karein
        return normalized_series.fillna(0.0)

    def process_pillars(self, raw_data_df):
        """
        Dono pillars (MCT aur INT) ko common range (0.0 to 1.0) mein scale karna[cite: 198].
        """
        df = raw_data_df.copy()
        
        # Pillar 1 (MCT) Normalization
        df['mct_norm'] = self.apply_rolling_min_max(df, 'mct_raw')
        
        # Pillar 2 (INT) Normalization
        df['int_norm'] = self.apply_rolling_min_max(df, 'int_raw')
        
        return df