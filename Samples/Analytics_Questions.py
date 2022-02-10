import pandas as pd
import matplotlib.pyplot as plt
import math
import requests

json = requests.get('https://volleypal.39-data.ru/get_objects/').json()
data = pd.json_normalize(json,"data")
shapes = data['shape'].unique()

def df_by_shape(df):
    group = []
    for i in shapes:
        array = df[df['shape'] == i]
        group.append(array)
    return group

#q1      Draw a boxplot showing the area size distribution for each shape
#answer  See below

array = []

for i in df_by_shape(data):
    array.append(i['area'].values)

fig, ax = plt.subplots()
ax.set_title('Area Distribution for Shapes')
ax.boxplot(array)
ax.set_xticklabels(shapes)

plt.show()

#q2      Calculate the mean, max, and standard deviation of the area size of each color
#answer  See below

for i in df_by_shape(data):
    mean = i['area'].mean()
    max = i['area'].max()
    std = i['area'].std()
    shape = i['shape'].unique()
    print(shape[0],':', 'mean: ', round(mean),', max: ', round(max),', std: ', round(std),)

#q3      What is the average area size of a yellow square?
#answer  See below

q3 = data[(data['color'] == 'yellow') & (data['shape'] == 'square')]
print('average area of a yellow square:', round(q3['area'].mean()))

#q4      Which shape is most likely to be green?
#answer  A circle. There's a 72.4% chance a green shape will be a circle

q4 = data[data['color'] == 'green']
answer = q4.groupby(by=['shape'], as_index=0).sum()
answer['perc'] = (answer['area'] / answer['area'].sum()) * 100
answer.sort_values(by='perc', ascending=False)
answer['perc'] = round(answer['perc'], 1)
answer

#q5      Given that the object is red, with an area size larger than 3,000 - what are the chances the object is a square? a triangle? a circle?
#answer  There's a 15.2% chance the object will be a square, 44.4% chance of it being a triangle, and 40.4% chance of it being a circle

q5 = data[(data['color'] == 'red') & (data['area'] > 3000)]
answer = q5.groupby(by=['shape'], as_index=0).sum()
answer['perc'] = (answer['area'] / answer['area'].sum()) * 100
answer = answer.sort_values(by='perc', ascending=False)
answer['perc'] = round(answer['perc'], 1)
answer

#q6      Write a function that calculates the side or radius of an object, depending on the shape and area of the object
#q7      Add a column to the dataset called "side" that shows the size matching the area in each row, round that number to the closest integer (shape side or radius).
#answer  See below

def calc_side(df):
    
    #df['side'] = df['side'].astype(float)
    
    df.loc[df['shape']=='circle','side'] = df['area'] / (2*math.pi)
    df.loc[df['shape']=='triangle','side'] = df['area'] / 3
    df.loc[df['shape']=='square','side'] = df['area'] / 4
    df['side'] = df['side'].round(decimals = 0)
    
    #the below commented out formulas are what I wanted to but could not execute for triangles and squares
    #df.loc[df['shape']=='triangle','side'] = math.sqrt( ( math.sqrt(3)/4 ) * df['area'] )
    #df.loc[df['shape']=='square','side'] = math.sqrt( df['area'] / 4 ) * 4
    
    return df.head(5)

calc_side(data)

#q8      Draw a boxplot showing the side size distribution for each shape - what can you infer from this plot?
#answer  The typical radius of a circle is larger than the side of a square or triangle 

array = []

for i in df_by_shape(data):
    array.append(i['side'].values)

fig, ax = plt.subplots()
ax.set_title('Side Size Distribution for Shapes')
ax.boxplot(array)
ax.set_xticklabels(shapes)

plt.show()

#q9      Make a scatter plot with "side" on the x-axis, "area" on the y axis with a different color for each shape.
#answer  See below

for i in df_by_shape(data):
    x = []
    y = []
    shape = i['shape'].unique()
    x.append(i['side'].values)
    y.append(i['area'].values)
    plt.scatter(x, y,label=shape)

plt.xlabel("area")
plt.ylabel("side")
plt.legend(loc='upper left')
plt.show()

#q10     Create a data frame, table, or list that show for each shape:
    #a.      The proportion of red objects within the shape
    #b.      The proportion of blue area out of the shape's total area (sum of blue sizes of a shape divided by the total size of a shape)
#q11     Create a function that calculates 10. b. for a given shape and color
#answer  See below

def function_q10(df):
    for i in shapes:
        array = df[df['shape'] == i]
        array = array.groupby(by=['color'], as_index=0).agg({'area': ['count', 'sum']})
        array.columns = array.columns.droplevel()
        array.columns = ['color', 'count', 'area']
        array['perc_area'] = array['area'] / array['area'].sum()
        array['perc_area'] = round(array['perc_area'], 2)
        array['shape'] = i            
        print(array,'\n')

function_q10(data)


