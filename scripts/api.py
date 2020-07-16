import requests
import json 
import os 

thisfolder = os.path.dirname(os.path.abspath(__file__))

def list_to_json_file(path,res):
    with open(path, 'w')  as outfile:
        json.dump(res, outfile, indent = 4,
                ensure_ascii = False)


def filter_json(search_col,keyword,path):
    with open (path) as json_file :
        data  = json.load(json_file)
    for x in data:
        if x[search_col].lower() == keyword.lower():
            return x['id']
 
def parse_categories():
    url = "https://www.themealdb.com/api/json/v1/1/categories.php"
    response1 = requests.request("GET", url)
    categ = json.loads(response1.text)['categories']

    categ_list = []
    
    for x in categ :
        categ_obj =  {
            "id":int(x['idCategory']),
            "name":x['strCategory'],
            "img_link":x['strCategoryThumb'],
            "description":x['strCategoryDescription'],
        }
        categ_list.append(categ_obj)
    list_to_json_file(f'{thisfolder}/categories.json',categ_list)
    print('Done! categories parsed .')


def parse_ingredients():
    url = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
    response1 = requests.request("GET", url)
    ingredients = json.loads(response1.text)['meals']

    ingredients_list = []
    
    for x in ingredients :
        ingr_obj =  {
            "id":int(x['idIngredient']),
            "name":x['strIngredient'],
            "description":x['strDescription'],
        }
        ingredients_list.append(ingr_obj)
    list_to_json_file(f'{thisfolder}/ingredients.json',ingredients_list)
    print('Done! ingredients parsed.')

def parse_areas():
    url = "https://www.themealdb.com/api/json/v1/1/list.php?a=list"
    response1 = requests.request("GET", url)
    areas = json.loads(response1.text)['meals']

    areas_list = []
    cnt_id = 1
    for x in areas :
        if x['strArea'] != 'Unknown':
            area_obj =  {
                "id":cnt_id,
                "name":x['strArea'],
            }
            areas_list.append(area_obj)
            cnt_id += 1
    list_to_json_file(f'{thisfolder}/areas.json',areas_list)
    print('Done! areas parsed.')



def parse_meals():
    res = []
    with open (f"{thisfolder}/unparse_meals.json") as unparse_meals :
        data  = json.load(unparse_meals)
    cnt_id = 1
    ingr_meal = []

    for meal in data :
        meal_obj = {
            'id':cnt_id,
            'name':meal[0]['strMeal'],
            'category_id':filter_json('name',meal[0]['strCategory'],f"{thisfolder}/categories.json"),
            'area_id':filter_json('name',meal[0]['strArea'],f"{thisfolder}/areas.json"),
            'like_count':0,
            'instruction':meal[0]['strInstructions'],
            'img_link':meal[0]['strMealThumb'],
            'tags':meal[0]['strTags'],
            'video_link':meal[0]['strYoutube'],
        }
        
        for x in range(1,20) :
            if meal[0][f'strIngredient{x}'] and meal[0][f'strIngredient{x}'] != None :
                ingr_id = filter_json('name',meal[0][f'strIngredient{x}'],f"{thisfolder}/ingredients.json") 
                if ingr_id :
                    obj = {
                        'meal_id':cnt_id,
                        'igredient_id':ingr_id
                    }
                    ingr_meal.append(obj)
                
        res.append(meal_obj)
        cnt_id += 1
    list_to_json_file(f'{thisfolder}/ingredient_list.json',ingr_meal)
    list_to_json_file(f'{thisfolder}/parsed_meals.json',res)
    print('Done! meals parsed.')
    
# makes a list of lists comprised of dict values
def prep_query(file_name,fields):
    with open (file_name,encoding="utf8") as jf :
        list1  = json.load(jf)
    list_new=[]
    for i in range (len(list1)):
        list_new.append([])
    for j in range (0,len(list1)):
        for k,v in list1[j].items():
            if k in fields:
                list_new[j].append(v)
    return list_new

meals=prep_query("scripts/parsed_meals.json", ("id","name","category_id", "area_id", "like_count", "instructions","img_link", "tags", "video_link"))
print("meals", meals)
ingredient=prep_query("scripts/ingredients.json",("id","name","description"))
print("ingredient", ingredient)
meal_ingredient=prep_query("scripts/ingredient_list.json",("meal_id", "ingredient_id"))
print("meal_ingredient", meal_ingredient)
categories=prep_query("scripts/categories.json",("id", "name", "img_link", "description"))
print("categories", categories)
area=prep_query("scripts/areas.json",("id", "name"))
print("area",area)



if __name__ == "__main__": 
    # parse_categories()
    # parse_ingredients()
    # parse_areas()
    parse_meals()



#useful links `

#api request for list of all ingredients - https://www.themealdb.com/api/json/v1/1/list.php?i=list
#api request for list of all areas - https://www.themealdb.com/api/json/v1/1/list.php?a=list
#api request for list of all categories - https://www.themealdb.com/api/json/v1/1/list.php?c=list


