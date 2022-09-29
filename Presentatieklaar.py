#!/usr/bin/env python
# coding: utf-8

# In[44]:


import requests
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

df = pd.read_csv('StudentsPerformance.csv')
st.title('Student Performance')
st.markdown('Mirthe Fischer, Liam van Toor, Lotte Broers en Reinoud Tas')
st.header('Inleiding')
st.markdown('Er is een dataset geraadpleegd met daarin informatie over de score bij bepaalde vakken. Hierin zijn bepaalde elementen weergegeven die mogelijk invloed hebben op de score.')
st.dataframe(df.head())
st.markdown('In deze head van de dataset zijn de verschillende variabelen te zien')

df.info()
df.describe()
df.rename(columns = {'race/ethnicity':'Group', 'gender' : 'Gender', 'lunch' : 'Lunch',
                    'test preparation course' : 'Preparation', 'math score' : 'Math_score',
                    'reading score' : 'Reading_score', 'writing score' : 'Writing_score'}, inplace = True)


df['Average_score'] = df.iloc[:, 5:9].mean(axis = 1) 
df['Parental_education'] = np.where(df['parental level of education'].isin(['some high school', 'high school']), 
                                    'Low','High')
df['Parental_education'] = np.where(df['parental level of education'].isin(['some college', "associate's degree"]), 
                                   'Middle', df['Parental_education'])

df.drop('parental level of education', axis = 1, inplace = True)
df = df.round(decimals = 0)

df_num = df[['Math_score', 'Reading_score', 'Writing_score', 'Average_score']]
df_cat = df[['Gender', 'Group', 'Lunch', 'Preparation', 'Parental_education']]


st.dataframe(df.head())
st.markdown('Met de info functie hebben wij bepaald dat er geen Na waardes in de dataset aanwezig zijn, wel hebben wij een paar acties ondernomen om de kwaliteit van de dataset te verbeteren. Die kan je hier zien')

st.header('Analyse')
pivot_table = pd.pivot_table(df, index = ['Group', 'Gender', 'Lunch', 'Preparation',], 
               values = ['Math_score', 'Reading_score', 'Writing_score', 'Average_score'])
dfpivot_table = pivot_table.reset_index()
dfpivot_table = dfpivot_table.round(decimals = 0)
dfpivot_table.style.set_properties(**{'background-color': 'beige',
                           'color': 'black',
                           'border-color': 'black',
                           'border-width': '1px',
                           'border-style': 'solid'})

st.dataframe(dfpivot_table.head())
st.markdown('Met deze pivot table is er gekeken naar de verschillende variabelen en de invloed van die variabelen op het eindresultaat.')
    
species_color_map = {'female':'rgb(204,255,204)', 'male':'rgb(255,204,204)'}
fig6 = px.histogram(df, x=df_num['Math_score'], color = df_cat['Gender'],title = 'Scores compared to gender', opacity = 0.5
                       , labels = {'x' : 'Math score', 
                      'color' : 'Gender'}, color_discrete_map=species_color_map)
fig6.update_layout(height = 500, width = 700)
st.plotly_chart(fig6)
st.markdown('Over het algemeen scoren mannen iets beter op wiskunde dan vrouwen')

    
fig7 = px.histogram(df, x=df_num['Reading_score'], color = df_cat['Gender'],title = 'Scores compared to gender', opacity = 0.5
                       , labels = {'x' : 'Reading score', 
                      'color' : 'Gender'}, color_discrete_map=species_color_map)
fig7.update_layout(height = 500, width = 700)
st.plotly_chart(fig7)

fig8 = px.histogram(df, x=df_num['Writing_score'], color = df_cat['Gender'],title = 'Scores compared to gender', opacity = 0.5
                       , labels = {'x' : 'Writing score', 
                      'color' : 'Gender'}, color_discrete_map=species_color_map)
fig8.update_layout(height = 500, width = 700)
st.plotly_chart(fig8)
st.markdown('Vrouwen scoren over het algemeen beter op lezen en schrijven dan mannen')

fig9 = px.histogram(df, x=df_num['Average_score'], color = df_cat['Gender'],title = 'Scores compared to gender', opacity = 0.5
                       , labels = {'x' : 'Average score', 
                      'color' : 'Gender'}, color_discrete_map=species_color_map)
fig9.update_layout(height = 500, width = 700)
st.plotly_chart(fig9)
st.markdown('Vrouwen scoren over het algemeen gemiddeld iets hoger dan de mannen')

fig1 = px.box(df , x = ['Preparation'], y = 'Average_score', 
             title = 'Average score compared to preparation', color = 'Lunch', notched = True,
             labels = {'Average_score' : 'Average score', 
                      'Preparation' : 'Amount of preparation', 'value' : 'Amount of preparation'}, 
             color_discrete_sequence=px.colors.qualitative.Bold)
fig1.update_xaxes(categoryorder = 'array', categoryarray = ['standard', 'free/reduced', 'High', 'Middle', 'Low'])
st.plotly_chart(fig1)
st.markdown('Het blijkt dat mensen die lunch hebben gehad en zich hebben voorbereid het beste resultaat hebben gehaald. Lunch heeft altijd een positief effect op de score, voorbereid of niet.')

fig2 = go.Figure()
for group in ['group A', 'group B', 'group C', 'group D', 'group E']:
    df_fig = df[df.Group == group]
    fig2.add_trace(go.Scatter(
                   x=df_fig['Reading_score'],
                   y=df_fig['Writing_score'],
                   name=group, mode = 'markers'))
A_annotation=[{ 'text': 'Most spread out, lower on average','showarrow': False, 'x': 60, 'y': 90}]
B_annotation=[{ 'text': 'Biggest range, mostly in the middle','showarrow': False, 'x': 60, 'y': 90}]
C_annotation=[{ 'text': 'Most clustered near the middle','showarrow': False, 'x': 60, 'y': 90}]
D_annotation=[{ 'text': 'Clustered near the top middle','showarrow': False, 'x': 60, 'y': 90}]
E_annotation=[{ 'text': 'Spread out near the top','showarrow': False, 'x': 60, 'y': 90}]
dropdown_buttons = [
{'label': "All groups", 'method': "update", 'args': [{"visible": [True, True, True, True, True]}, 
                                                  {'title': 'All groups', 'annotations': []}]},    
{'label': "group A", 'method': "update", 'args': [{"visible": [True, False, False, False, False]}, 
                                                  {'title': 'Group A', 'annotations': A_annotation}]},
{'label': "group B", 'method': "update", 'args': [{"visible": [False, True, False, False, False]}, 
                                                  {'title': 'Group B', 'annotations': B_annotation}]},
{'label': "group C", 'method': "update", 'args': [{"visible": [False, False, True, False, False]},
                                                  {'title' : 'Group C', 'annotations':C_annotation}]},
{'label': "group D", 'method': "update", 'args': [{"visible": [False, False, False, True, False]}, 
                                                  {'title': 'Group D', 'annotations': D_annotation}]},
{'label': "group E", 'method': "update", 'args': [{"visible": [False, False, False, False, True]}, 
                                                  {'title': 'Group E', 'annotations': E_annotation}]},    
]

fig2.update_layout({
    'updatemenus':[{
            'type': 'dropdown',
            'x': 1.3, 'y': 0.5,
            'showactive': True, 'active': 0,
            'buttons': dropdown_buttons
            }]})
fig2.update_layout(legend_title_text = "Different groups", title = 'Relation between reading and writing score')
fig2.update_xaxes(title_text="Reading score")
fig2.update_yaxes(title_text="Writing score")

st.plotly_chart(fig2)
st.markdown('Er is een duidelijk sterk verband tussen de scores van lezen en schrijven over alle groepen.')


df2 = df.groupby('Group')['Math_score', 'Reading_score', 'Writing_score', 'Average_score'].mean()
df2 = pd.DataFrame(df2)
df2.head()

race=['group A', 'group B', 'group C', 'group D', 'group E']

fig3 = go.Figure(data=[
    go.Bar(name='Math score', x=race, y=df2['Math_score']),
    go.Bar(name='Reading score', x=race, y=df2['Reading_score']),
    go.Bar(name='Writing score', x=race, y=df2['Writing_score']),
    go.Bar(name='Average', x=race, y=df2['Average_score'])])

sliders = [
    {'steps':[
    {'method': 'update', 'label': 'Total', 'args': [{'visible': [True, True, True, True, True]}]},
    {'method': 'update', 'label': 'Math score', 'args': [{'visible': [True, False, False, False, False]}]},
    {'method': 'update', 'label': 'Reading score', 'args': [{'visible': [False, True, False, False, False]}]},
    {'method': 'update', 'label': 'Writing score', 'args': [{'visible': [False, False, True, False, False]}]},
    {'method': 'update', 'label': 'Average', 'args': [{'visible': [False, False, False, True, False]}]}]}]

# Update the figure to add sliders and show
fig3.update_layout({'sliders': sliders})

st.plotly_chart(fig3)
st.markdown('Er is geen duidelijke verschil tussen de scores per groep, maar wel een opwaardse trend.')

fig5 = px.box(df , x = 'Parental_education', y = 'Average_score', title = 'Average score compared to parental education level', 
             color = 'Parental_education',
             labels = {'Parental_education' : 'Parental education', 
                      'Average_score' : 'Average score'}, color_discrete_sequence=px.colors.qualitative.Bold)
st.plotly_chart(fig5)
st.markdown('Het opleidingsniveau van de ouders heeft geen duidelijke invloed op prestatie, behalve als het opleidingsniveau laag is.')

st.header('Conclusie')
Image = Image.open('conlusie.png')
st.image(Image)
            


# In[41]:





# In[39]:





# In[ ]:




