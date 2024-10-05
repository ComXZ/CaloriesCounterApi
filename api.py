import json
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from caloriescounter import encodeandsearch
app = FastAPI()

class ProductCalories(BaseModel):
    name: str
    calories: float
    proteins: float
    caloriesfor100: float
    proteinsfor100: float

class Product(BaseModel):
    name: str
    weight: int

@app.post("/", response_model=List[ProductCalories])
def calculatecalories(product_list: List[Product]):
    dict_data = [product.dict() for product in product_list]
    result = encodeandsearch(dict_data)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port=8000)
