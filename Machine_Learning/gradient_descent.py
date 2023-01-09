import time
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.sin(x) + 0.5*x

def df(x):
    return np.cos(x) + 0.5

N = 20  # число итераций
xi = 2.5  # начальное значение
lmd = 0.2  # шаг сходимости

x_plt = np.arange(-5, 5, 0.1)
f_plt = [f(x) for x in x_plt]

plt.ion()  # Интерактивный режим отображения графика
fig, ax = plt.subplots()
ax.grid(True)

ax.plot(x_plt, f_plt)
point = ax.scatter(xi, f(xi), c='red')

mn = 100
for i in range(N):
    lmd = 1 / min(i+1, mn)
    xi = xi - lmd * np.sign(df(xi))  # Делает скорость постоянной (не зависит от величины градиента)
    point.set_offsets([xi, f(xi)])

    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.02)

plt.ioff()
ax.scatter(xi, f(xi), c='blue')
plt.show()

