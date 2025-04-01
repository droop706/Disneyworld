import xgboost as xgb
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error

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

    def preprocess_data(self):
        """Prepare features (X) and targets (y), and split into train/test."""
        y = self.df.filter(like="SPOSTMIN_")  # All target columns
        X = self.df.drop(columns=y.columns)  # All feature columns

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def hyperparameter_tuning(self, param_grid):
        """
        Perform hyperparameter tuning using GridSearchCV.
        """
        grid_search = GridSearchCV(
            estimator=xgb.XGBRegressor(),
            param_grid=param_grid,
            cv=3,
            scoring="neg_mean_squared_error",
            verbose=1,
            n_jobs=-1
        )
        grid_search.fit(self.X_train, self.y_train)

        self.best_params = grid_search.best_params_
        return {"best_params": self.best_params, "best_score": grid_search.best_score_}

    def train_model(self):
        """Train an XGBoost model using the best parameters from GridSearch."""
        if not self.best_params:
            raise ValueError("Run hyperparameter_tuning() first to get best parameters.")

        self.model = xgb.XGBRegressor(**self.best_params)  # Use best params
        self.model.fit(self.X_train, self.y_train)
        joblib.dump(self.model, "xgboost_model.pkl")  # Save the trained model

    def evaluate_model(self):
        """Evaluate model performance using MAE and RMSE."""
        y_pred = self.model.predict(self.X_test)
        mae = mean_absolute_error(self.y_test, y_pred)
        rmse = mean_squared_error(self.y_test, y_pred, squared=False)
        return {"MAE": mae, "RMSE": rmse}
