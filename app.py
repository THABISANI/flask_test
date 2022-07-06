from flask import Flask, request
from numpy import number

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process
import math

app = Flask(__name__)

@app.route('/recommendations', methods=['GET'])
def recommendation():

    args = request.args
    familiar_restaurant = args.get("restaurant")
    if not familiar_restaurant:
        familiar_restaurant = "KFC"
    
    number_of_restaurants = 0
    print("===========Number of Res============")
    print(number_of_restaurants)
    if args.get("size") is None:
        number_of_restaurants = 20
    else:
        number_of_restaurants = int(args.get("size")) + 1

    restaurants='restaurants.csv'

    df_restaurants=pd.read_csv(restaurants, usecols=['id','bna'], dtype={'id':'int32','bna':'str'})
    df_recommendations=pd.read_csv(restaurants, usecols=['bid','id','Lon', 'Lat'],dtype={'bid':'int32','id':'int32','Lon':'float32', 'Lat':'float32'})

    restaurants_users=df_recommendations.pivot(index='id', columns='bid',values=['Lon', 'Lat']).fillna(0)
    mat_restaurants_users=csr_matrix(restaurants_users.values)

    model_knn= NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=number_of_restaurants)

    model_knn.fit(mat_restaurants_users)

    def recommender(restaurant_name, data,model, n_recommendations ):
        model.fit(data)
        idx=process.extractOne(restaurant_name, df_restaurants['bna'])[2]
        print('Restaurant Selected: ',df_restaurants['bna'][idx], 'Index: ',idx)
        print('Searching for recommendations.....')
        distances, indices=model.kneighbors(data[idx], n_neighbors=n_recommendations)
        recommendations = []
        for i in indices:
            bnas = df_restaurants['bna'][i].where(i!=idx)
            ids = df_restaurants['id'][i].where(i!=idx)
            id_list = ids.to_dict().values()
            for x in id_list:
                if not math.isnan(x):
                    recommendations.append({"id": int(x)})
            print(bnas)
            print(ids)
        print("=====Recomd===========")
        print(recommendations)
        return recommendations

    recommendations = []
    if(familiar_restaurant):
        recommendations = recommender(familiar_restaurant, mat_restaurants_users, model_knn,number_of_restaurants)
    return {"recommended_restaurants": recommendations}

@app.route('/healthy', methods=['GET', 'POST'])
def healthy():
    return "<H2>Flask App is Healthy!!!</H2>"

@app.route('/login', methods=['POST'])
def login():
    content = request.get_json(force=True)
    return {"Message" : content}, 201