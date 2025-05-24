import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
import joblib
import os
import requests
import cloudinary
import cloudinary.uploader
from io import StringIO
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def download_csv_from_cloudinary(url):
    """Download CSV file from Cloudinary."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text))
    except Exception as e:
        logger.error(f"Failed to download CSV from Cloudinary: {str(e)}")
        raise Exception(f"Failed to download CSV from Cloudinary: {str(e)}")

def upload_image_to_cloudinary(image_path):
    """Upload an image to Cloudinary and return the secure URL."""
    try:
        response = cloudinary.uploader.upload(
            image_path,
            resource_type="image",
            folder="churn_predictor"
        )
        return response['secure_url']
    except Exception as e:
        logger.error(f"Failed to upload image to Cloudinary: {str(e)}")
        raise Exception(f"Failed to upload image to Cloudinary: {str(e)}")

def load_and_preprocess_data(cloudinary_url, output_dir='media'):
    """Load and preprocess the CSV file from Cloudinary."""
    logger.debug("Loading and preprocessing data")
    df = download_csv_from_cloudinary(cloudinary_url)
    
    logger.debug(f"Risco_Churn values: {df['Risco_Churn'].value_counts().to_dict()}")
    
    colunas_numericas = ['Idade', 'Volume_Investimentos', 'Qtd_Servicos_Contratados', 'Score_Relacionamento']
    for col in colunas_numericas:
        df[col] = df[col].fillna(df[col].median())
    df['Perfil_Risco'] = df['Perfil_Risco'].fillna(df['Perfil_Risco'].mode()[0])
    
    le = LabelEncoder()
    df['Perfil_Risco'] = le.fit_transform(df['Perfil_Risco'])
    
    scaler = StandardScaler()
    df[colunas_numericas] = scaler.fit_transform(df[colunas_numericas])
    
    os.makedirs(output_dir, exist_ok=True)
    joblib.dump(le, os.path.join(output_dir, 'label_encoder.pkl'))
    joblib.dump(scaler, os.path.join(output_dir, 'standard_scaler.pkl'))
    
    return df, le, scaler

def train_and_evaluate_holding(df, output_dir='media'):
    """Train and evaluate Random Forest for 'Abriu_Holding'."""
    logger.debug("Training and evaluating holding model")
    X = df.drop(['Abriu_Holding', 'Risco_Churn', 'Id'], axis=1)
    y_holding = df['Abriu_Holding']
    
    X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(X, y_holding, test_size=0.2, random_state=42)
    
    rf_h = RandomForestClassifier(random_state=42)
    rf_h.fit(X_train_h, y_train_h)
    y_pred_h = rf_h.predict(X_test_h)
    y_prob_h = rf_h.predict_proba(X_test_h)
    
    report_h = classification_report(y_test_h, y_pred_h, output_dict=True, labels=[0, 1])
    matrix_h = confusion_matrix(y_test_h, y_pred_h).tolist()
    
    report_path = os.path.join(output_dir, 'relatorio_holding.txt')
    with open(report_path, 'w') as f:
        f.write(classification_report(y_test_h, y_pred_h))
    
    matriz_holding_path = os.path.join(output_dir, 'matriz_holding.png')
    plt.figure(figsize=(6, 5))
    sns.heatmap(confusion_matrix(y_test_h, y_pred_h), annot=True, fmt='d')
    plt.title('Matriz - Abriu Holding')
    plt.savefig(matriz_holding_path)
    plt.close()
    matriz_holding_url = upload_image_to_cloudinary(matriz_holding_path)
    
    importancia_holding_path = os.path.join(output_dir, 'importancia_holding.png')
    importances_h = pd.Series(rf_h.feature_importances_, index=X.columns)
    plt.figure(figsize=(8, 6))
    importances_h.sort_values(ascending=False).plot(kind='barh')
    plt.title('Importância das Variáveis - Holding')
    plt.savefig(importancia_holding_path, bbox_inches="tight")
    plt.close()
    importancia_holding_url = upload_image_to_cloudinary(importancia_holding_path)
    
    scores_h = cross_val_score(rf_h, X, y_holding, cv=5, scoring='f1')
    
    joblib.dump(rf_h, os.path.join(output_dir, 'rf_holding.pkl'))
    
    return report_h, scores_h.mean(), matriz_holding_url, importancia_holding_url, report_path, importances_h.to_dict(), y_prob_h

def train_and_evaluate_churn(df, output_dir='media'):
    """Train and evaluate Random Forest for 'Risco_Churn'."""
    logger.debug("Training and evaluating churn model")
    X = df.drop(['Abriu_Holding', 'Risco_Churn', 'Id'], axis=1)
    y_churn = df['Risco_Churn']
    
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_churn, test_size=0.2, random_state=42)
    
    rf_c = RandomForestClassifier(random_state=42)
    rf_c.fit(X_train_c, y_train_c)
    y_pred_c = rf_c.predict(X_test_c)
    y_prob_c = rf_c.predict_proba(X_test_c)
    
    # Explicitly define labels for binary classification (0=Baixo, 1=Médio)
    report_c = classification_report(y_test_c, y_pred_c, output_dict=True, labels=[0, 1])
    matrix_c = confusion_matrix(y_test_c, y_pred_c, labels=[0, 1]).tolist()
    
    matriz_churn_path = os.path.join(output_dir, 'matriz_churn.png')
    plt.figure(figsize=(6, 5))
    sns.heatmap(confusion_matrix(y_test_c, y_pred_c, labels=[0, 1]), annot=True, fmt='d')
    plt.title('Matriz - Risco de Churn')
    plt.savefig(matriz_churn_path)
    plt.close()
    matriz_churn_url = upload_image_to_cloudinary(matriz_churn_path)
    
    importancia_churn_path = os.path.join(output_dir, 'importancia_churn.png')
    importances_c = pd.Series(rf_c.feature_importances_, index=X.columns)
    plt.figure(figsize=(8, 6))
    importances_c.sort_values(ascending=False).plot(kind='barh')
    plt.title('Importância das Variáveis - Churn')
    plt.savefig(importancia_churn_path, bbox_inches="tight")
    plt.close()
    importancia_churn_url = upload_image_to_cloudinary(importancia_churn_path)
    
    scores_c = cross_val_score(rf_c, X, y_churn, cv=5, scoring='f1_weighted')
    
    joblib.dump(rf_c, os.path.join(output_dir, 'rf_churn.pkl'))
    
    return report_c, scores_c.mean(), matriz_churn_url, importancia_churn_url, importances_c.to_dict(), y_prob_c

def predict_single(data, output_dir='media'):
    """Predict for a single data point using saved models."""
    logger.debug("Predicting single data point")
    try:
        le = joblib.load(os.path.join(output_dir, 'label_encoder.pkl'))
        scaler = joblib.load(os.path.join(output_dir, 'standard_scaler.pkl'))
        rf_h = joblib.load(os.path.join(output_dir, 'rf_holding.pkl'))
        rf_c = joblib.load(os.path.join(output_dir, 'rf_churn.pkl'))
        
        input_data = pd.DataFrame([data])
        input_data['Perfil_Risco'] = le.transform([input_data['Perfil_Risco'].iloc[0]])[0]
        
        colunas_numericas = ['Idade', 'Volume_Investimentos', 'Qtd_Servicos_Contratados', 'Score_Relacionamento']
        input_data[colunas_numericas] = scaler.transform(input_data[colunas_numericas])
        
        pred_h = rf_h.predict(input_data)[0]
        prob_h = rf_h.predict_proba(input_data)[0]
        pred_c = rf_c.predict(input_data)[0]
        prob_c = rf_c.predict_proba(input_data)[0]
        
        importances_h = joblib.load(os.path.join(output_dir, 'importances_holding.pkl'))
        feature_importance = [{'feature': k, 'importance': v} for k, v in importances_h.items()]
        
        return {
            'abriu_holding': 'Sim' if pred_h == 1 else 'Não',
            'risco_churn': {0: 'Baixo', 1: 'Médio'}[pred_c],
            'probabilidades': {
                'holding_sim': prob_h[1] * 100,
                'holding_nao': prob_h[0] * 100,
                'churn_medio': prob_c[1] * 100,
                'churn_baixo': prob_c[0] * 100,
            },
            'feature_importance': feature_importance
        }
    except Exception as e:
        logger.error(f"Failed to predict: {str(e)}")
        raise Exception(f"Failed to predict: {str(e)}")

def run_predictor(cloudinary_url='https://res.cloudinary.com/djz9qsw5v/raw/upload/v1748064726/base_clientes_w1_fake_gpdjxz.csv', output_dir='media'):
    """Run the full prediction pipeline with Cloudinary integration."""
    logger.debug("Running predictor pipeline")
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        df, le, scaler = load_and_preprocess_data(cloudinary_url, output_dir)
        
        report_h, f1_h, matriz_holding_url, importancia_holding_url, relatorio_holding_path, importances_h, prob_h = train_and_evaluate_holding(df, output_dir)
        report_c, f1_c, matriz_churn_url, importancia_churn_url, importances_c, prob_c = train_and_evaluate_churn(df, output_dir)
        
        joblib.dump(importances_h, os.path.join(output_dir, 'importances_holding.pkl'))
        joblib.dump(importances_c, os.path.join(output_dir, 'importances_churn.pkl'))
        
        total_predictions = len(df)
        holding_conversions = df['Abriu_Holding'].sum()
        medio_risk_clients = (df['Risco_Churn'] == 1).sum()
        model_accuracy = (report_h['accuracy'] + report_c['accuracy']) / 2 * 100
        
        distribution_data = [
            {'label': 'Baixo Risco', 'value': (df['Risco_Churn'] == 0).mean() * 100, 'color': '#22c55e'},
            {'label': 'Médio Risco', 'value': (df['Risco_Churn'] == 1).mean() * 100, 'color': '#eab308'},
        ]
        holding_data = [
            {'label': 'Sim', 'value': df['Abriu_Holding'].mean() * 100, 'color': '#3b82f6'},
            {'label': 'Não', 'value': (1 - df['Abriu_Holding'].mean()) * 100, 'color': '#9ca3af'},
        ]
        
        # Create RandomForestClassifier instances for confusion matrix
        rf_h = joblib.load(os.path.join(output_dir, 'rf_holding.pkl'))
        rf_c = joblib.load(os.path.join(output_dir, 'rf_churn.pkl'))
        
        return {
            'holding_report': report_h,
            'holding_f1_score': f1_h,
            'churn_report': report_c,
            'churn_f1_score': f1_c,
            'matriz_holding_url': matriz_holding_url,
            'matriz_churn_url': matriz_churn_url,
            'importancia_holding_url': importancia_holding_url,
            'importancia_churn_url': importancia_churn_url,
            'relatorio_holding_url': relatorio_holding_path,
            'metrics': {
                'totalPredictions': total_predictions,
                'holdingConversions': holding_conversions,
                'highRiskClients': medio_risk_clients,
                'modelAccuracy': model_accuracy,
                'trends': {
                    'predictions': 0.0,
                    'conversions': 0.0,
                    'risk': 0.0
                },
                'distributionData': distribution_data,
                'holdingData': holding_data
            },
            'performance': {
                'holdingReport': {
                    'precision': {'sim': report_h['1']['precision'], 'nao': report_h['0']['precision']},
                    'recall': {'sim': report_h['1']['recall'], 'nao': report_h['0']['recall']},
                    'f1Score': {'sim': report_h['1']['f1-score'], 'nao': report_h['0']['f1-score']},
                    'accuracy': report_h['accuracy']
                },
                'churnReport': {
                    'precision': {
                        'medio': report_c['1']['precision'],
                        'baixo': report_c['0']['precision']
                    },
                    'recall': {
                        'medio': report_c['1']['recall'],
                        'baixo': report_c['0']['recall']
                    },
                    'f1Score': {
                        'medio': report_c['1']['f1-score'],
                        'baixo': report_c['0']['f1-score']
                    },
                    'accuracy': report_c['accuracy']
                },
                'holdingMatrix': confusion_matrix(df['Abriu_Holding'], rf_h.predict(df.drop(['Abriu_Holding', 'Risco_Churn', 'Id'], axis=1)), labels=[0, 1]).tolist(),
                'churnMatrix': confusion_matrix(df['Risco_Churn'], rf_c.predict(df.drop(['Abriu_Holding', 'Risco_Churn', 'Id'], axis=1)), labels=[0, 1]).tolist(),
                'featureImportance': [{'feature': k, 'importance': v} for k, v in importances_h.items()]
            },
            'stats': {
                'predictionsToday': total_predictions,
                'modelAccuracy': model_accuracy,
                'clientsAnalyzed': total_predictions,
                'highRiskChurn': medio_risk_clients
            }
        }
    except Exception as e:
        logger.error(f"Error in run_predictor: {str(e)}")
        raise