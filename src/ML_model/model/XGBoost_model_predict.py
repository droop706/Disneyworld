import joblib
from sklearn.model_selection import train_test_split
import os

class XGBoostPredictor:
    def __init__(self, model_path='../xgboost_model.pkl'):
        """Load the trained model for making predictions."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, '..', 'xgboost_model.pkl')
        self.model = joblib.load(model_path)
        self.training_columns = self.model.feature_names_in_

    def preprocess_features(self, X_new):
        """
        Ensure the prediction dataset matches the training dataset in structure.

        Parameters:
        - X_new (pd.DataFrame): Feature dataframe for prediction.

        Returns:
        - X_new (pd.DataFrame): Processed dataframe matching training columns.
        """

        # Add missing columns (fill with 0)
        for col in self.training_columns:
            if col not in X_new.columns:
                X_new[col] = 0

        # Remove extra columns that were not in training data
        X_new = X_new[self.training_columns]

        # Ensure data types match
        X_new = X_new.astype(self.model.estimators_[0].feature_types)

        return X_new

    def predict(self, X_new):
        """
        Make predictions on new data.

        Parameters:
        - X_new (pd.DataFrame): Feature dataframe for prediction.

        Returns:
        - np.array: Predicted values.
        """
        X_new = self.preprocess_features(X_new)

        return self.model.predict(X_new)
