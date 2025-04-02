import joblib
from sklearn.model_selection import train_test_split
import os

class XGBoostPredictor:
    def __init__(self, model_path='../xgboost_model.pkl'):
        """Load the trained model for making predictions."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, '..', 'xgboost_model.pkl')
        self.model = joblib.load(model_path)

    def predict(self, X_new):
        """
        Make predictions on new data.

        Parameters:
        - X_new (pd.DataFrame): Feature dataframe for prediction.

        Returns:
        - np.array: Predicted values.
        """
        return self.model.predict(X_new)
