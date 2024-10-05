from typing import Dict, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote_plus, unquote_plus
import chardet


def search(prepared_product: List[dict]) -> List[dict]:
    option = Options()
    option.add_argument('--disable-gpu')
    option.add_argument('--headless')
    driver = webdriver.Firefox(options=option)
    end_result = []
    for product in prepared_product:
        driver.get(product["url"])

        try: 
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.media-body')))

            # element = driver.find_elements_by_xpass("//div[@class='media-body']//a//p")
            media_body = driver.find_element(By.CLASS_NAME, "media-body")
            media_body_child_a = media_body.find_element(By.TAG_NAME, "a")
            media_body_child_a_child_p = media_body_child_a.find_elements(By.TAG_NAME, "p")
            result = media_body_child_a_child_p[-1].text

            calories_text = result.split(", ")[0]
            calories = int(calories_text.split()[0])
            end_calories = (calories/100)*product["weight"]

            proteins_text = result.split(", ")[1]
            proteins = float(proteins_text.split()[0])
            end_proteins = (proteins/100)*product["weight"]

            print(calories, proteins)
            end_result.append({"name": product["name"], "calories": end_calories, "proteins": end_proteins, "caloriesfor100": calories, "proteinsfor100": proteins})
        except TimeoutException:
            print(f"Not found, {product["url"]}")
            end_result.append({"name": product["name"], "calories": 0, "proteins": 0, "caloriesfor100": 0, "proteinsfor100": 0})
    return end_result

def encodeandsearch(text_weight: List[dict]) -> List[dict]:
    """
    function endcode and search - Декодирует поисковой текст в кодировку иврита и вычесляет калорийность и протеин продукта
    :params: 
    text_weight: List[Dict[str, int]] - Список продуктов и их веса
    """
    prepared_product = []
    for product_dict in text_weight:
        product_dict["encode_name"] = product_dict["name"].encode('windows-1255')
        url_encoded_text = quote_plus(product_dict["encode_name"])
        product_dict["url"] = f"https://www.foodsdictionary.co.il/allsearch.php?q={url_encoded_text}"
        prepared_product.append(product_dict)
    return search(prepared_product)

if __name__ == "__main__":
    products_weights_list = []
    for i in range(int(input("How much products at all: "))):
        text = input("Enter the name of a product: ")
        weight = int(input("Enter the weight of the product: "))
        products_weights = {"name": text, "weight": weight}
        products_weights_list.append(products_weights)

    total_calories = 0
    total_proteins = 0
    print(products_weights_list)
    result = encodeandsearch(products_weights_list)
    print(result)
    for product in result:
        print(f"product: {product["name"][::-1]}, calories per 100g: {product["caloriesfor100"]}, proteins per 100g: {product["proteinsfor100"]}")
        print(f"total calories of {product["name"][::-1]}: {product["calories"]}, total proteins of {product["name"][::-1]}: {product["proteins"]}")
        print()
        total_calories += product["calories"]
        total_proteins += product["proteins"]
    print(total_calories, total_proteins)