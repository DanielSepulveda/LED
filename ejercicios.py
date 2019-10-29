import streamlit as st
import pandas as pd
import numpy as np
import time
import uber_display
from scipy import stats

"# Numpy and Pandas Tutorial"
"### Semana i 2019"

"Made in Streamlit"

if st.checkbox('Show Uber Data'):
    st.subheader('Uber data data')
    uber_display.main()
    


"""# Numpy exercises  """

"- **Show numpy version**"
version = np.version.version
result = "Numpy version : {}".format(version)

# answer
result 


"- **Create the array :** "
"   *[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]*"

# answer
result = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
"Answer"
result


"- **Select the cell located in row 2 column 2 from this array**"

arr = np.array(([21, 22, 23], [11, 22, 33], [43, 77, 89]))
"*Array*"
arr

# answer
result = arr[2][2]
result 

"- **Select the column with index 0**"
arr = np.array(([21, 22, 23], [11, 22, 33], [43, 77, 89]))
arr

# answer
result = arr[0]
result


"- **Extract all the odd numbers in the next array**"
"   *[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]*"

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

# answer
result = arr[arr % 2 == 1]
result


"""- **Replace de odd numbers with negative numbers in the next array**"""
"   *[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]*"

arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

with np.nditer(arr, op_flags=['readwrite']) as it:
    for x in it:
        if x % 2 == 1:
            x[...] = x * -1

# answer

result = arr

result

"- **Reshape the next array from 1D to 2D**"
"   *[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]*"

arr = np.arange(10)
narr = np.reshape(arr, (-1, 2))

# answer
result = narr
result

"- **Compute euclidian distance between A and B **"
"A"
a = np.array([1,2,3,4,5])
a

"B"
b = np.array([4,5,6,7,8])
b

# Answers

result = np.linalg.norm(a - b)
result

"- **Find the most frequent value of petal length (3rd column) in the [iris dataset](https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data)**"

def downloadIrisDataset():
    url = './iris.data'
    iris = np.genfromtxt(url, delimiter=',', dtype='object')
    return iris
"*Dataset*"

iris = downloadIrisDataset()
names = ('sepallength', 'sepalwidth', 'petallength', 'petalwidth', 'species')

# answer

length = len(iris)
x = stats.mode(iris[0 : length, 2])
result = x
result[0][0]
