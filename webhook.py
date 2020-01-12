from flask import Flask, make_response, request, jsonify
import os
import pandas as pd
import numpy as np
df=pd.read_csv('products_mapped.csv')

app=Flask(__name__)

@app.route('/')
def results():
    req=request.get_json(force=True)
    action=req.get('queryResult').get('action')

    if action == 'recommend':
        parameters = req.get('queryResult').get('parameters')
        product = parameters.get("products")
        skin_type = parameters.get("skin_type")
        result={}
        result['fulfillmentText']=query(product,skin_type)
        result=jsonify(result)
        return make_response(result)

def query(op1,op2):
    lbl=op1+'_'+op2
    lbl=lbl.strip()
    df_2=df[df.label==lbl].reset_index().drop('index',axis=1)
    df_3=df_2.sample(5)
    df_2['dist'] = 0.0
    myItem = df_2.sample() #find a random product
    #t = df_2.sort_values('rank', ascending=False)
    #myItem = t.head(1)
    P1 = np.array([myItem.X.values, myItem.Y.values]).reshape(1, -1)
    for i in range(len(df_2)):
        P2 = np.array([df_2['X'][i], df_2['Y'][i]]).reshape(-1, 1)
        df_2.dist[i] = (P1 * P2).sum() / (np.sqrt(np.sum(P1)) * np.sqrt(np.sum(P2))) #cosine similarity
    df_2 = df_2.sort_values('dist', ascending=False)

    if df_2['dist'].empty:
        df_2=df_2.sample(5)
    txt=''

    counter=1
    for x in range(0,5) :
        txt=txt+str(counter)+') '+str(df_2.at[x,'name'])+' by '+str(df_2.at[x,'brand'])+'. Price: $'+str(df_2.at[x,'price'])+'\n'
        counter+=1

    counter=1
    msg=''
    prod=df_3['name'].values
    brand=df_3['brand'].values
    price=df_3['price'].values
    for x in range (0,5):
        msg=msg+str(counter)+ ') '+prod[x]+' by '+ brand[x]+'. Price: $'+str(price[x])+'\n'
        counter += 1

    return msg



#def index():
    #return results()

#parameters = req.get('queryResult').get('action')
#product=parameters.get("products")
#skin_type=parameters.get("skin_type")

if __name__=='__main__':
    app.run(debug=True,use_reloader=True)
  
