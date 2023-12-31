# -*- coding: utf-8 -*-
"""Quality.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NecjE476-PSoZRl7ap5vwFa2_sNSm7BN
"""

from google.colab import drive
drive.mount('/content/drive')
fname = "/content/drive/My Drive/Colab Notebooks/iris.csv.gz"
f_name = "/content/drive/My Drive/Colab Notebooks/iris.csv"

import scipy
import sklearn
import pandas as pd
import matplotlib
import numpy as npy
import sys
import random
from itertools import combinations
from sklearn.model_selection import train_test_split

# KNN
from sklearn.neighbors import KNeighborsClassifier

# SVM
from sklearn import svm

# K-Means
from sklearn.cluster import KMeans

# MaxMin

def euclidean_metric(val1, val2):
  sum = 0.0
  for i in range(len(val1)):
    dif = val1[i] - val2[i]
    sum += dif * dif
  return npy.sqrt(sum)

def maximin_clusters(data_set: npy.ndarray, q = 0.8):
  if len(data_set) == 0:
    return [[]]
  elif len(data_set) == 1:
    return [[0]]

  scnd_cntr = npy.argmax(list(map(lambda v: euclidean_metric(data_set[0], v), data_set)))
  cluster_centers = [random.randint(0, 119), scnd_cntr]
  old_maxmin = euclidean_metric(data_set[0], data_set[scnd_cntr])
  new_maxmin = old_maxmin * q
  clusters = []
  while len(clusters) != 3:
    clusters = [[] for i in cluster_centers]

    max = 0
    max_i = 0
    for i, val in enumerate(data_set):
      min = euclidean_metric(val, data_set[cluster_centers[0]])
      min_j = 0
      for j, cntr in enumerate(cluster_centers):
        metr = euclidean_metric(val, data_set[cntr])
        if metr < min:
          min = metr
          min_j = j
      clusters[min_j].append(i)
      if min > max:
        max = min
        max_i = i
    old_maxmin = new_maxmin
    new_maxmin = max
    cluster_centers.append(max_i)
  # Последний 4 центр входит в последний кластер
  return cluster_centers[:3]

def check_image(centers, image, x_, y_):
  min_dist = 9999999
  min_center = 0.0
  for center in centers:
    if (euclidean_metric(x_[center], image) < min_dist):
      min_dist = euclidean_metric(x_[center], image)
      min_center = center

  return y_[min_center]

dataset = pd.read_csv(fname)

# Срез: отсекаем классы
x = dataset.values[:, 0:4]

# Оставляем только классы
y = dataset.values[:, 4]

# Перемешать и разделить данные в пропорции 90:10
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# Разделим 3 класса на 2

def get_class(e_class):
  class1 = ['setosa']
  class2 = ['versicolor']
  class3 = ['virginica']
  
  
  if (e_class in class1):
    return 1
  elif (e_class in class2):
    return 2
  else: return 3

def get_cluster_class(e_class):
  class1 = [0]
  class2 = [1]
  class3 = [2]
  
  if (e_class in class1):
    return 1
  elif (e_class in class2):
    return 2
  else: return 3

def conf_matrix(y_true, y_pred):
  result = npy.zeros((3, 3))
  for i in range(len(y_true)):
    result[get_class(y_true[i])-1][get_class(y_pred[i])-1] += 1

  return result    
# np - количество положительных объектов
# nn - количество отрицатиельных объектов
# fp - количество ложных пропусков 
# fn - количество ложных обнаружений
# tp - количество верных пропусков
# tn - количество верных обнаружений

# neigh = KNeighborsClassifier(n_neighbors=3)
# neigh.fit(x_train, y_train)
# neigh.predict(x_test[0])

# KNN
neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(x_train, y_train)

y_pred = neigh.predict(x_test)

conf_mat = conf_matrix(y_test, y_pred)

# classes: 1, 2, 3
tp_1 = conf_mat[0][0] + conf_mat[1][1] + conf_mat[2][2]
tn_1 = conf_mat[1][1] + conf_mat[2][2] + conf_mat[1][2] + conf_mat[2][1]
fp_1 = conf_mat[1][0] + conf_mat[2][0]
fn_1 = conf_mat[0][1] + conf_mat[0][2]


tp_2 = tp_1
tn_2 = conf_mat[0][0] + conf_mat[0][2] + conf_mat[2][0] + conf_mat[2][2]
fp_2 = conf_mat[0][1] + conf_mat[2][1]
fn_2 = conf_mat[1][1] + conf_mat[1][2]


tp_3 = tp_1
tn_3 = conf_mat[0][0] + conf_mat[0][1] + conf_mat[1][0] + conf_mat[1][1]
fp_3 = conf_mat[1][2] + conf_mat[2][2]
fn_3 = conf_mat[2][1] + conf_mat[2][2]

precision = int((tp_1/(tp_1 + fp_1) + tp_2/(tp_2 + fp_2) + tp_3/(tp_3 + fp_3)) / 4 * 100)
recall = int((tp_1/(tp_1 + fn_1) + tp_2/(tp_2 + fn_2) + tp_3/(tp_3 + fn_3)) / 4 * 100)


print("1.")
# Доля правильных ответов ответов модели в пределах класса
print("Точность: ", precision)

# Количество истино положительных среди всех меток класса, которые были определены как "положительный"
print("Полнота: ", recall)

# Гармоническое среднее между точностью и полнотой
print("F1: ", int(2 * (precision * recall) / (precision + recall)))

print("3. Среднеквадратичная ошибка")
error = 0
for test, pred in zip([get_class(i) for i in y_test], [get_class(i) for i in y_pred]):
  error += (test - pred) ** 2
error /= len(y_test)
print(error)

print("4. Кросс-Валидация")
folds = 5
x_train_folds = npy.array_split(x, folds)
y_train_folds = npy.array_split(y, folds)
accuracies = []
for i in range(folds):
  xtest = x_train_folds[i]
  ytest = y_train_folds[i]
  x_tr = npy.vstack((x_train_folds[0:i] + x_train_folds[i+1:]))
  y_tr = npy.vstack((y_train_folds[0:i] + y_train_folds[i+1:])).ravel()

  neigh_ = KNeighborsClassifier(n_neighbors=3)
  neigh_.fit(x_tr, y_tr)
  ypred= neigh_.predict(xtest)
  accuracies.append(npy.mean(ytest==ypred))

print("Точность на каждом из 5 фолдов: ", accuracies)

# Столбцы резервируются за экспертным решением, строки за решением классификатора
print("5.")
print("Матрица неточностей: \n", conf_mat)

# Доля дисперсии зависимой переменной, объясняемая рассматриваемой моделью зависимости 
print("6. Коэффициент детерминации")
y_mean = sum([get_class(i) for i in y_pred])/len(y_pred)
y_tot = 0.0
for test in [get_class(i) for i in y_test]:
  y_tot += (test - y_mean) ** 2
y_tot /= len(y_test)
print(1-error/y_tot)

# SVM
clf = svm.SVC()
clf.fit(x_train, y_train)

y_pred = clf.predict(x_test)

conf_mat = conf_matrix(y_test, y_pred)

# classes: 1, 2, 3
tp_1 = conf_mat[0][0] + conf_mat[1][1] + conf_mat[2][2]
tn_1 = conf_mat[1][1] + conf_mat[2][2] + conf_mat[1][2] + conf_mat[2][1]
fp_1 = conf_mat[1][0] + conf_mat[2][0]
fn_1 = conf_mat[0][1] + conf_mat[0][2]


tp_2 = tp_1
tn_2 = conf_mat[0][0] + conf_mat[0][2] + conf_mat[2][0] + conf_mat[2][2]
fp_2 = conf_mat[0][1] + conf_mat[2][1]
fn_2 = conf_mat[1][1] + conf_mat[1][2]


tp_3 = tp_1
tn_3 = conf_mat[0][0] + conf_mat[0][1] + conf_mat[1][0] + conf_mat[1][1]
fp_3 = conf_mat[1][2] + conf_mat[2][2]
fn_3 = conf_mat[2][1] + conf_mat[2][2]

precision = int((tp_1/(tp_1 + fp_1) + tp_2/(tp_2 + fp_2) + tp_3/(tp_3 + fp_3)) / 4 * 100)
recall = int((tp_1/(tp_1 + fn_1) + tp_2/(tp_2 + fn_2) + tp_3/(tp_3 + fn_3)) / 4 * 100)


print("1.")
print("Точность: ", precision)
print("Полнота: ", recall)
print("F1: ", int(2 * (precision * recall) / (precision + recall)))

print("3. Среднеквадратичная ошибка")
error = 0
for test, pred in zip([get_class(i) for i in y_test], [get_class(i) for i in y_pred]):
  error += (test - pred) ** 2
error /= len(y_test)
print(error)

print("4. Кросс-Валидация")
folds = 5
x_train_folds = npy.array_split(x, folds)
y_train_folds = npy.array_split(y, folds)
accuracies = []
for i in range(folds):
  xtest = x_train_folds[i]
  ytest = y_train_folds[i]
  x_tr = npy.vstack((x_train_folds[0:i] + x_train_folds[i+1:]))
  y_tr = npy.vstack((y_train_folds[0:i] + y_train_folds[i+1:])).ravel()

  clf_ = svm.SVC()
  clf_.fit(x_tr, y_tr)
  ypred= clf_.predict(xtest)

  accuracies.append(npy.mean(ytest==ypred))

print("Точность на каждом из 5 фолдов: ", accuracies)

print("5.")
print("Матрица неточностей: \n", conf_mat)

print("6. Коэффициент детерминации")
y_mean = sum([get_class(i) for i in y_pred])/len(y_pred)
y_tot = 0.0
for test in [get_class(i) for i in y_test]:
  y_tot += (test - y_mean) ** 2
y_tot /= len(y_test)
print(1-error/y_tot)

# K-Means

kmeans = KMeans(n_clusters=3, random_state=0).fit(x_train)

y_pred = kmeans.predict(x_test)

conf_mat = conf_matrix(y_test, y_pred)

# classes: 1, 2, 3
tp_1 = conf_mat[0][0] + conf_mat[1][1] + conf_mat[2][2]
tn_1 = conf_mat[1][1] + conf_mat[2][2] + conf_mat[1][2] + conf_mat[2][1]
fp_1 = conf_mat[1][0] + conf_mat[2][0]
fn_1 = conf_mat[0][1] + conf_mat[0][2]


tp_2 = tp_1
tn_2 = conf_mat[0][0] + conf_mat[0][2] + conf_mat[2][0] + conf_mat[2][2]
fp_2 = conf_mat[0][1] + conf_mat[2][1]
fn_2 = conf_mat[1][1] + conf_mat[1][2]


tp_3 = tp_1
tn_3 = conf_mat[0][0] + conf_mat[0][1] + conf_mat[1][0] + conf_mat[1][1]
fp_3 = conf_mat[1][2] + conf_mat[2][2]
fn_3 = conf_mat[2][1] + conf_mat[2][2]

precision = int((tp_1/(tp_1 + fp_1) + tp_2/(tp_2 + fp_2) + tp_3/(tp_3 + fp_3)) / 4 * 100)
recall = int((tp_1/(tp_1 + fn_1) + tp_2/(tp_2 + fn_2) + tp_3/(tp_3 + fn_3)) / 4 * 100)


print("1.")
print("Точность: ", precision)
print("Полнота: ", recall)
print("F1: ", int(2 * (precision * recall) / (precision + recall)))

print("3. Среднеквадратичная ошибка")
error = 0
for test, pred in zip([get_class(i) for i in y_test], (y_pred + 1)):
  error += (test - pred) ** 2
error /= len(y_test)
print(error)

print("4. Кросс-Валидация")
folds = 5
x_train_folds = npy.array_split(x, folds)
y_train_folds = npy.array_split(y, folds)
accuracies = []
for i in range(folds):
  xtest = x_train_folds[i]
  ytest = y_train_folds[i]
  x_tr = npy.vstack((x_train_folds[0:i] + x_train_folds[i+1:]))
  y_tr = npy.vstack((y_train_folds[0:i] + y_train_folds[i+1:])).ravel()

  kmeans_ = KMeans(n_clusters=3, random_state=0).fit(x_tr)
  ypred= kmeans_.predict(xtest)
  accuracies.append(npy.mean([get_class(i) for i in ytest]==(ypred + 1)))

print("Точность на каждом из 5 фолдов: ", accuracies)

print("5.")
print("Матрица неточностей: \n", conf_mat)

print("6. Коэффициент детерминации")
y_mean = sum(y_pred + 1)/len(y_pred)
y_tot = 0.0
for test in [get_class(i) for i in y_test]:
  y_tot += (test - y_mean) ** 2
y_tot /= len(y_test)
print(1-error/y_tot)

# MaxMin
x_ = npy.genfromtxt(f_name, dtype=float, delimiter=",",
                         usecols=(0, 1, 2, 3), 
                         converters={3: lambda s: float(s)},
                         encoding = None)[1:]
y_ = npy.genfromtxt(f_name, dtype = str, delimiter=",", usecols=(4,), encoding = None)[1:]

y_ = [i[1:len(i) - 1].lower() for i in y_]
temp = list(zip(x_, y_))

random.shuffle(temp)

x_, y_ = zip(*temp)
x_train_ = x_[:120]
x_test_ = x_[121:150]
y_test_ = y_[121:150]

centers = maximin_clusters(x_train_)
y_pred = [check_image(centers, x, x_, y_) for x in x_test_]

conf_mat = conf_matrix(y_test_, y_pred)

# classes: 1, 2, 3
tp_1 = conf_mat[0][0] + conf_mat[1][1] + conf_mat[2][2]
tn_1 = conf_mat[1][1] + conf_mat[2][2] + conf_mat[1][2] + conf_mat[2][1]
fp_1 = conf_mat[1][0] + conf_mat[2][0]
fn_1 = conf_mat[0][1] + conf_mat[0][2]


tp_2 = tp_1
tn_2 = conf_mat[0][0] + conf_mat[0][2] + conf_mat[2][0] + conf_mat[2][2]
fp_2 = conf_mat[0][1] + conf_mat[2][1]
fn_2 = conf_mat[1][1] + conf_mat[1][2]


tp_3 = tp_1
tn_3 = conf_mat[0][0] + conf_mat[0][1] + conf_mat[1][0] + conf_mat[1][1]
fp_3 = conf_mat[1][2] + conf_mat[2][2]
fn_3 = conf_mat[2][1] + conf_mat[2][2]

precision = int((tp_1/(tp_1 + fp_1) + tp_2/(tp_2 + fp_2) + tp_3/(tp_3 + fp_3)) / 4 * 100)
recall = int((tp_1/(tp_1 + fn_1) + tp_2/(tp_2 + fn_2) + tp_3/(tp_3 + fn_3)) / 4 * 100)


print("1.")
print("Точность: ", precision)
print("Полнота: ", recall)
print("F1: ", int(2 * (precision * recall) / (precision + recall)))

print("3. Среднеквадратичная ошибка")
error = 0
for test, pred in zip([get_class(i) for i in y_test_], [get_class(i) for i in y_pred]):
  error += (test - pred) ** 2
error /= len(y_test_)
print(error)

print("4. Кросс-Валидация")
folds = 5
x_train_folds = npy.array_split(x, folds)
y_train_folds = npy.array_split(y, folds)
accuracies = []
for i in range(folds):
  xtest = x_train_folds[i]
  ytest = y_train_folds[i]
  x_tr = npy.vstack((x_train_folds[0:i] + x_train_folds[i+1:]))
  y_tr = npy.vstack((y_train_folds[0:i] + y_train_folds[i+1:])).ravel()
  # x_tr = [npy.array(i, dtype=npy.void) for i in x_tr]
  centers_ = maximin_clusters(tuple(x_tr))
  ypred = [check_image(centers_, x, x_, y_) for x in xtest]
  accuracies.append(npy.mean(ytest==ypred))

print("Точность на каждом из 5 фолдов: ", accuracies)

print("5.")
print("Матрица неточностей: \n", conf_mat)

print("6. Коэффициент детерминации")
y_mean = sum([get_class(i) for i in y_pred])/len(y_pred)
y_tot = 0.0
for test in [get_class(i) for i in y_test_]:
  y_tot += (test - y_mean) ** 2
y_tot /= len(y_test_)
print(1-error/y_tot)