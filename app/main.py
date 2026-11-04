from fastapi import FastAPI

'''
Crtl + Shft + ñ
python -m uvicorn app.main:app --reload
'''

app = FastAPI(
    title='GeoData Intelligence',
    description='AI-Assisted Geospatial Data Harmonisation Platform',
    version='0.1.0',
)

@app.get('/')
def root():
    return {
        'message':'Welcome to GeoData Intelligence API',
        'status':'running'
    }

@app.get('/health')
def health_check():
    return {
        'status':'healthy'
    }