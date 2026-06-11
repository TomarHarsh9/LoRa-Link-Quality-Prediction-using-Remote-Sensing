import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
from sklearn.preprocessing import StandardScaler

#  Load Csv from QGis 
df = pd.read_csv("QGIS/training_data.csv")


#  Rename band columns (adjust if names differ)
df = df.rename(columns={
    "SAMPLE_1": "B02",   # Blue
    "SAMPLE_2": "B03",   # Green
    "SAMPLE_3": "B04",   # Red
    "SAMPLE_4": "B08"    # NIR
})
print(df.head())

# calculate Ndvi Or Ndwi 
eps = 1e-10

df["NDVI"] = (df["B08"] - df["B04"]) / (df["B08"] + df["B04"] + eps)
df["NDWI"] = (df["B03"] - df["B08"]) / (df["B03"] + df["B08"] + eps)


# prepare training data 
X = df[["B02", "B03", "B04", "B08", "NDVI", "NDWI"]].values
y = df["class"].values

#  Split data into training and testing sets

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
#  Create SVM classifier

svm = SVC(
    kernel="rbf",   # non-linear kernel
    C=10,          # regularization parameter
    gamma="scale"      # kernel coefficient
)

#  Train the SVM model

svm.fit(X_train, y_train)

#prdict class lable for unseen pixels 
y_pred = svm.predict(X_test)

#Test the trained model

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

joblib.dump(svm, "svm_model.pkl")
joblib.dump(scaler, "scaler.pkl")
