"""

Basis RF-Modell, hier zum Untersuchen von Pegeldaten einer Zeitreihe mit Split-Datum.

Soll als Vorlage für Anwendungen von RF dienen und einige optionale Features haben, 
die an- und auskommentiert werden können je nach Bedarf.

"""


def rf_modell(dataframe):
    model = RandomForestRegressor(
        n_estimators=200, #150-200 oft ausreichend für stabilen run 
        max_depth=10, # Tiefe der Bäume je nach Notwendigkeit/Anwendung anpassen
        random_state=42 # zur reproduktion, 42 ist der standard
    )
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    y_train_pred = model.predict(X_train)
    
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2_train = r2_score(y_train, y_train_pred)
    r2 = r2_score(y_test, y_pred) # r2 der testdaten 
    
    print("RMSE:", rmse)
    print("R2 Train:", r2_train)
    print("R2 Test:", r2) # Train und test ausgeben lassen! Wichtig für Bias/Varianz Analyse
 
    # Hier analysieren: Train >>>> test heißt Overfitting, aber beide schlecht wäre underfitting.
    
    # im optimalfall geringer bias und geringe varianz.
    """
    
    # FEATURE IMPORTANCE
    
    feature_importance = pd.Series(model.feature_importances_, index=X_train.columns)
    feature_importance = feature_importance.sort_values(ascending=False)

    print(feature_importance) # schnell gemacht und wichtig
    
    """
    
    rfmodell_output_path= r"..."
    
    plt.figure(figsize=(12,5))
    plt.plot(dataframe["Datum"][dataframe["Datum"] >= split_date], y_test, label="Real")
    plt.plot(dataframe["Datum"][dataframe["Datum"] >= split_date], y_pred, label="Prediction")
    plt.legend()
    plt.title(f"Pegel-Vorhersage für Daten ab {split_date}")

    plt.text(0.02, 0.95, f"R² = {r2:.2f}", transform=plt.gca().transAxes, verticalalignment='top')
    plt.savefig(f"{rfmodell_output_path}\\Pegel-Vorhersage_für_Daten_ab_{split_date}.png", dpi=300, bbox_inches="tight")

    plt.show()
    
    """
    
    OPTIONAL: SHAP VALUES
    
    import shap

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    shap.summary_plot(shap_values, X_test)
    
    """
    