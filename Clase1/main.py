from fastapi import FastAPI

app = FastAPI(title='Mi primer API')

@app.get('/')
def root():
    return {'message': 'Hola mundo'}


#Parametros

@app.get('/items/{item_id}')
def read_item(item_id: int):
    return {'item_id': item_id}
