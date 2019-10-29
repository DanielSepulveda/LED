import pandas as pd
import numpy as np

# Combinar dos series

ser1 = pd.Series(list("abcdefghijklmnñopqrstuvwxyz"))
ser2 = pd.Series(np.arange(26))
df = pd.DataFrame({"col1": ser1, "col2": ser2})

# Declarar un pandas series de la sig lista

mylist = list("abcdefghijklmnñopqrstuvwxyz")
ser1 = pd.Series(mylist)

# Filtrar elementos que no esten en un series

ser1 = pd.Series([1, 2, 3, 4, 5])
ser2 = pd.Series([4, 5, 6, 7, 8])
ser1[-ser1.isin(ser2)]

# Convertir numpy arr a dataframe de un tamaño especifico. Ejemplo, cambiar
# el tamaño del vector a una matrix 7 x 5

np.random.RandomState(100)
ser1 = np.random.randint(1, 10, 35)
pd.DataFrame(np.reshape(ser1, (-1, 5)))

# Manipular un dataframe de strings

df = pd.DataFrame(["how", "to", "kick", "ass"])
df.apply(lambda x : x.str.capitalize())

# Calcular distancia euclidiana entre dos vectores

p = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
q = pd.Series([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
df = pd.DataFrame({"p": p, "q": q}).reset_index()
a = df.apply(lambda row : pow(row["q"] - row["p"], 2), axis=1)
suma = sum(a)
res = np.sqrt(suma)
