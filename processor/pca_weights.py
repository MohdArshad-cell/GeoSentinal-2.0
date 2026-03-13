from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

def calculate_dynamic_weights(mct_series, int_series):
    """
    PCA-based weighting mechanism with a fallback for new datasets[cite: 211, 215].
    """
    # Safety Check: Agar 2 se kam data points hain, toh PCA nahi chal sakta
    if len(mct_series) < 2:
        # Default weighting as mentioned in Section 5.2 
        return {'w_mct': 0.5, 'w_int': 0.5}

    try:
        data = pd.DataFrame({'MCT': mct_series, 'INT': int_series})
        
        # Step: Standardization [cite: 223]
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        
        # Step: Perform PCA [cite: 225, 226]
        pca = PCA(n_components=1)
        pca.fit(scaled_data)
        
        # Squared loadings logic to derive weights [cite: 229, 231]
        loadings = pca.components_[0] ** 2
        weights = loadings / loadings.sum()
        
        return {'w_mct': weights[0], 'w_int': weights[1]}
    
    except Exception as e:
        # Kuch bhi error aaye toh default weights par wapis jao
        return {'w_mct': 0.5, 'w_int': 0.5}