import numpy as np
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error
from src.ML_model.feature_target_table.merge_waitingdf_weatherdf import MergeWaitingDFWeatherDF
from src.ML_model.model.parameter_grid import PARAMETERS_GRID
import pandas as pd
from sklearn.multioutput import MultiOutputRegressor
import numpy as np

class XGBoostTrainer:
    def __init__(self, df_features_targets):
        """
        Initializes the training class.

        Parameters:
        - df_features_targets (pd.DataFrame): Dataframe with features and target columns.
        """
        self.df = df_features_targets
        self.model = None
        self.X_train, self.X_test, self.y_train, self.y_test = self.preprocess_data()
        self.best_params = None  # Store best hyperparameters
        self.param_grid = PARAMETERS_GRID

    def preprocess_data(self):
        """Prepare features (X) and targets (y), and split into train/test."""
        y = self.df.filter(like="SPOSTMIN_")  # All target columns
        X = self.df.drop(columns=y.columns)  # All feature columns

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def hyperparameter_tuning(self):
        """
        Perform hyperparameter tuning using GridSearchCV with MultiOutputRegressor.
        """
        base_model = MultiOutputRegressor(xgb.XGBRegressor())
        param_grid_names = {f"estimator__{key}": value for key, value in self.param_grid.items()}
        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=param_grid_names,
            cv=3,
            scoring="neg_mean_squared_error",
            verbose=1,
            n_jobs=-1
        )

        y_train_array = self.y_train.values if isinstance(self.y_train, pd.DataFrame) else self.y_train
        grid_search.fit(self.X_train, self.y_train)

        self.best_params = {key.replace("estimator__", ""): value for key, value in grid_search.best_params_.items()}
        return {"best_params": self.best_params, "best_score": grid_search.best_score_}

    def train_model(self):
        """Train an XGBoost model using the best parameters from GridSearch."""
        if not self.best_params:
            raise ValueError("Run hyperparameter_tuning() first to get best parameters.")

        self.model = MultiOutputRegressor(xgb.XGBRegressor(**self.best_params))  # Use best params
        self.model.fit(self.X_train, self.y_train)
        joblib.dump(self.model, "xgboost_model.pkl")  # Save the trained model

    def evaluate_model(self):
        """Evaluate model performance using MAE and RMSE."""
        y_pred = self.model.predict(self.X_test)
        mae = mean_absolute_error(self.y_test, y_pred)
        mse = mean_squared_error(self.y_test, y_pred)
        rmse = np.sqrt(mse)

        return {"MAE": mae, "RMSE": rmse}
