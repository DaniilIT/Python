## [MatPlotLib](https://matplotlib.org/stable/index.html)

```
pip install matplotlib
```

```python
import matplotlib.pyplot as plt
import numpy as np
```


### Один график

<img src="images/plt.png" alt="plt" title="plt" style="height: 320px;"/>

```python
x = np.linspace(0, 2*np.pi, 40)
y1 = np.sin(x)
y2 = np.cos(x)

# plt.figure(figsize=(6, 4))  # 480x320 px
fig, ax = plt.subplots(figsize=(6, 4))  # явное создание фигур и осей (объектно-ориентированный стиль)

# plt.plot(x, y1, 'k--', marker='x', label='sin')  # график - линия
# plt.scatter(x, y2, c='r', label='cos')  # график - точками
ax.plot(x, y1, 'k--', marker='x', label='sin')
ax.scatter(x, y2, c='r', label='cos')

# plt.title("Title")
ax.set_title('Title')
# plt.xlabel('x')
ax.set_xlabel('x')
# plt.ylabel('y')
ax.set_ylabel('y')
# plt.legend()
ax.legend()
ax.text(4, 0.7, r'$\sigma$')

#plt.grid(True)
ax.grid(True)
# plt.yticks([-1, -0.7, 0, 0.7, 1])  # назначить занчения к оси y
plt.yticks([-1, -0.7, 0, 0.7, 1])
# plt.axvline(x=np.pi, color='k')  # вертикальная линия
ax.axvline(x=np.pi, color='k')

# plt.savefig('plt.png')  # сохранить график в файл
plt.show()
```


### Несколько графиков

```python
# fig = plt.figure()  # создадим три графика гризонтально
# ax1 = fig.add_subplot(1, 3, 1)
# ax1.plot(...)
# ax2 = fig.add_subplot(1, 3, 2)
# ax2.plot(...)
# ax3 = fig.add_subplot(1, 3, 3)
# ax3.plot(...)

fig, axs = plt.subplots(1, 3, figsize=(6, 4))
for ax in axs:
    ax.plot(...)
```


## [SeaBorn](http://seaborn.pydata.org/tutorial/introduction.html)

```python

```

```python

```

```python

```

```python

```

```python

```