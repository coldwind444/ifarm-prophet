from fastapi import FastAPI
from datetime import datetime
import pandas as pd
from prophet import Prophet

app = FastAPI()

def fit_model(str):
    df = pd.read_csv("data.csv") 
    df['time'] = pd.to_datetime(df['time'])
    dependent_v = 'relative_humidity_2m (%)' if str == 'h' else 'temperature_2m (°C)'
    df = df.rename(columns={'time':'ds', dependent_v: 'y'})
    model = Prophet()
    model.fit(df)
    return model

humid_model = fit_model('h')
temp_model = fit_model('t')

@app.get("/")
def read_root():
    return { "message": "Facebook Prophet model of Time Series Forecasting"}

@app.get("/humidity/{steps}")
def read_humidity(steps : int):
    future = humid_model.make_future_dataframe(periods=steps, freq='H')    
    forecast = humid_model.predict(future)
    future_forecast = forecast[forecast['ds'] > datetime.now()]
    result = future_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    return result.to_dict(orient = "records")

@app.get("/temperature/{steps}")
def read_temperature(steps : int):
    future = temp_model.make_future_dataframe(periods=steps, freq='H')    
    forecast = temp_model.predict(future)
    future_forecast = forecast[forecast['ds'] > datetime.now()]
    result = future_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    return result.to_dict(orient = "records")