import io
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd 
from nltk import word_tokenize, sent_tokenize
import re, string, unicodedata
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from sklearn.base import BaseEstimator,TransformerMixin
from nltk.corpus import stopwords
import contractions

app = FastAPI()

final_model_reloaded = joblib.load('hotel_model.joblib')
templates = Jinja2Templates(directory="templates")
def getFeatureImportance():	
    feature_names = final_model_reloaded.named_steps['transform'].get_feature_names_out()
    svm_coef = final_model_reloaded.named_steps['classifier'].coef_.toarray()
    feature_importance = pd.DataFrame({'Feature': feature_names, 'Coefficient': svm_coef[0]})
    feature_importance['abs_coef'] = feature_importance['Coefficient'].abs()
    feature_importance_sorted = feature_importance.sort_values(by='abs_coef', ascending=False)
    feature_importance_sorted = feature_importance_sorted.iloc[:1000]
    return feature_importance_sorted

def extract_features(data, features_df):
    results = []
    for text in data:
        found_features = []
        words = text.split()
        for word in words:
            for index, row in features_df.iterrows():
                if word.startswith(row['Feature']):
                    found_features.append({
                        'feature': row['Feature'],
                        'Coefficient': row['Coefficient'],
                        'word': word  # La palabra específica que coincidió con el feature
                    })
        results.append(found_features)
    return results


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict/")
async def predict(file: UploadFile = File(None), text_input: str = Form(None)):
    try:
        if file:
            if not file.filename.endswith('.xlsx'):
                return JSONResponse(content={"error": "El archivo debe tener formato .xlsx"}, status_code=400)

            data = pd.read_excel(io.BytesIO(file.file.read()), engine='openpyxl')
            if("Textos_espanol" not in data.columns):
                return JSONResponse(content={"error": "La columna debe llamarse 'Textos_espanol'"}, status_code=400)
            data = data["Textos_espanol"].tolist()
            
        elif text_input:
            data = pd.DataFrame({'Textos_espanol': [text_input]})
        else:
            return JSONResponse(content={"error": "El texto no puede ser vacio"}, status_code=400)
        predictions = final_model_reloaded.predict(data)
        extracted_features = extract_features(data, getFeatureImportance())
        if file:
            predictions_list = predictions.tolist()
            return JSONResponse(content={"predictions": predictions_list, "palabras": extracted_features }, status_code=200)
        else:
            output = pd.DataFrame({'Textos_espanol': data['Textos_espanol'], 'sdg': predictions})
            excel_output = io.BytesIO()
            output.to_excel(excel_output, index=False)
            return FileResponse(excel_output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename='predictions.xlsx')

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
