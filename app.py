from flask import Flask, request

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process

app = Flask(__name__)

@app.route('/recommendations', methods=['GET'])
def recommendation():

    args = request.args
    familiar_restaurant = args.get("restaurant")

    restaurants='restaurants.csv'

    df_restaurants=pd.read_csv(restaurants, usecols=['id','bna'], dtype={'id':'int32','bna':'str'})
    df_recommendations=pd.read_csv(restaurants, usecols=['bid','id','Lon', 'Lat'],dtype={'bid':'int32','id':'int32','Lon':'float32', 'Lat':'float32'})

    restaurants_users=df_recommendations.pivot(index='id', columns='bid',values=['Lon', 'Lat']).fillna(0)
    mat_restaurants_users=csr_matrix(restaurants_users.values)

    model_knn= NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20)

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
            recommendations.append({"id": str(ids)})
            print(bnas)
            print(ids)
        return recommendations

    recommendations = []
    if(familiar_restaurant):
        recommendations = recommender(familiar_restaurant, mat_restaurants_users, model_knn,20)
    return {"recommended_restaurants": recommendations}

@app.route('/healthy', methods=['GET', 'POST'])
def healthy():
    return "<H2>Flask App is Healthy!!!</H2>"

@app.route('/login', methods=['POST'])
def login():
    content = request.get_json(force=True)
    return {"Message" : content}, 201