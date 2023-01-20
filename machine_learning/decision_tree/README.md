# Decision Tree (Решающие Деревья)

Данные с [kaggle о подержанных автомобилях](https://www.kaggle.com/datasets/adityadesai13/used-car-dataset-ford-and-mercedes).

```python
# соединение таблицы
import os

data_dir = './data'
data = []
for data_file in os.listdir(data_dir):
    df = pd.read_csv(os.path.join(data_dir, data_file))
    data.append(df)

df = pd.concat(data, axis=0, ignore_index=True)
df.to_csv(os.path.join(data_dir, 'data.csv'),  sep=',', index=False)
```

```python
# загрузка данных
import numpy as np
import pandas as pd
df = pd.read_csv('data/data.csv').drop(columns=['Unnamed: 0'])
df.head()
```


## EDA (Exploratory Data Analysis, Разведочный Анализ Данных)

Процесс анализа свойств данных, нахождение в них общих закономерностей, распределений и аномалий.

```python
# просмотр уникальных значений
df['model'].value_counts()

df['model'] = df['model'].apply(lambda x: x.strip()) # если нет пропущенных значений
```

```python
# посмотр распределения пропущенных значений
import seaborn as sns
from matplotlib.pyplot import figure

figure(figsize = (5, 4))
sns.heatmap(df.isnull(), cbar=False)
```

<img src="missing_heat.png" alt="Тепловая карта пропущенных значений" title="Тепловая карта пропущенных значений" style="height: 380px;"/>

```python
# обрабатка пропущенных значений
df.drop(columns = df.columns[9:], inplace=True) # удаляем столбцы
df.dropna(inplace=True) # удаляем строчки
df.reset_index(drop=True, inplace=True) # сбрасываем индексы
# просмотр пропущенных значений
df.isnull().sum()
```

```python
# просмотр общей информации
df.shape
df.info()
df.describe()
df.hist(figsize=(9, 6))
```

```python
# проверка выбросов
print(len(df[df['year'] >= 2021]))
df = df[df['year'] < 2021]
```

```python
# приведение типов
df['price'] = df['price'].astype('int')
df['year'] = df['year'].astype('object')
df['mpg'] = df['mpg'].astype('int')
df['mileage'] = df['mileage'].astype('int')
```


### Кодировка признаков числовыми значениями

```python
# подключается класс для предобработки данных
from sklearn import preprocessing

def number_encode_features(df):
    df_new = df.copy()
    #----------------------------------------------------------------
    encoders = {}
    for column in df_new.columns:
        if df_new.dtypes[column] == object:
            encoders[column] = preprocessing.LabelEncoder() # создается кодировщик
            df_new[column] = encoders[column].fit_transform(df_new[column]) # применяется кодировщик
    #----------------------------------------------------------------
    # encoders = preprocessing.OrdinalEncoder()
    # categorical_columns = df_new.select_dtypes(include=['object']).columns
    # df_new[categorical_columns] = encoders.fit_transform(df_new[categorical_columns])
    # df_new[categorical_columns] = df_new[categorical_columns].astype('int') # изначально float
    #----------------------------------------------------------------
    # encoders = preprocessing.OneHotEncoder(handle_unknown='ignore') # новые неизвестные значения игнорируем
    # categorical_columns = df_new.select_dtypes(include=['object']).columns
    # other_columns = df_new.select_dtypes(exclude=['object']).columns
    # codes = encoders.fit_transform(df_new[categorical_columns]).toarray()
    # feature_names = encoders.get_feature_names_out(categorical_columns)
    # df_new = pd.concat([df[other_columns], pd.DataFrame(codes, columns=feature_names)], axis=1)
    #----------------------------------------------------------------
    return df_new, encoders

encoded_data, encoders = number_encode_features(df)
encoded_data.head()
```

```python
# просмотр матрицы корреляций по Пирсону
import matplotlib.pyplot as plt

plt.subplots(figsize=(9, 5))
sns.heatmap(encoded_data.corr(), cmap='coolwarm', vmin=-1, vmax=1, annot=True, fmt='.2f')
plt.show()
```

<img src="corr_heat.png" alt="Тепловая карта корреляций" title="Тепловая карта корреляций" style="height: 380px;"/>

Видно, что присутствуют линейные корреляции &\rightarrow& неплохой результат выдадут даже самые простые модели.


## DecisionTreeRegressor (Решающие Деревья)

[Идея:](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html)
алгоритм моделирует реальный процесс принятий решений.

свойства:
- простой алгоритм, на его основе построены сложные алгоритмы такие как **случайный лес** и **градиентный бустинг**,
- способен отбирать важные признаки,
- склонен к переобучению,
- может обрабатывать нелинейные зависимости

$Q = L + R$, хотим, чтобы из $p_L$ и $p_R$ одно было $0$, а другое $1$

$\cfraq{L}{Q}H(p_L) + \cfraq{R}{Q}H(p_R) \rightarrow min$, где $H(0) = H(1) = 0$ 

Критерия ветвлений (подбор решающего правила):
* энтропия (чем больше, тем больше степень хаоса) \
$H(q) = -q \log_2(q) - (1 - q) \log_2(1 - q)$, где $q$ - вероятнность класса,
* индекс Джини (процентное представление коэффициента Джини)\
$H(q) = 4q(1 - q)$
* Misclassification error

```python
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, median_absolute_error

# разделение на train-test выборки
X_train, X_test, y_train, y_test = train_test_split(encoded_data.drop(columns=['price']), encoded_data['price'], test_size=0.2)

# обучение модели
tree = DecisionTreeRegressor()
tree.fit(X_train, y_train)

# оценка качества
y_pred = tree.predict(X_test)
print(f'r2 = {r2_score(y_test, y_pred):.2f}, MedAE = {median_absolute_error(y_test, y_pred):.2f}, s = {y_train.std():.2f}')
```

```python
# подбор гиперпараметров
tree = DecisionTreeRegressor()

param_grid = {
    'max_depth': np.arange(2, 15), # макс. глубина
    'min_samples_split': np.arange(2, 24, 3), # мин. кол-во "листьев"
}

from sklearn.model_selection import GridSearchCV
gs = GridSearchCV(tree, param_grid, cv=5, scoring='r2', n_jobs=-1,
                  verbose=2) # вывод процесса обучения
gs.fit(X_train, y_train)

print(gs.best_params_, gs.best_score_)

y_pred = search.best_estimator_.predict(X_test)
```

cv = 5 $\rightarrow$ выполняется кросс-валидация $\rightarrow$ на 5 фолдах обучаются 5 разных алгоритмов $\rightarrow$ результаты оценки расчитывается на всей доступной выборке $\rightarrow$ метрики качества будут более устойчивы.

```python
# просмотр важности признаков
def plot_feature_importances(gs, column_names, top_n=15):
    imp = pd.Series(gs.best_estimator_.feature_importances_, index=column_names).sort_values(ascending=False)
    plt.figure(figsize=(9, 5))
    plt.title('Важность признаков по Giny Impurity')
    sns.barplot(x=imp.values[:top_n], y=imp.index.values[:top_n], orient='h')

plot_feature_importances(alg, X_train.columns.values)
```

<img src="important_bar.png" alt="Важность признаков по примеси Джини" title="Важность признаков по примеси Джини" style="height: 380px;"/>
