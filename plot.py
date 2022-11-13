import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import seaborn as sns

# Create figure for plotting
fig, axis = plt.subplots(2, 1, figsize=(8, 8))
fig.tight_layout(pad=6.0)
xs = []
ys = []


def animate(i):
    df = pd.read_csv('data.csv')

    ax = axis[0]
    ax.clear()
    sns.lineplot(data=df, x='time', y='temp', ax=ax)
    ax.set_ylabel('Temperatura (°C)')
    ax.set_xlabel('Tiempo (s)')
    ax.set_title('(a)')

    ax = axis[1]
    ax.clear()
    sns.lineplot(data=df, x='time', y='speed', ax=ax)
    ax.set_ylabel('Velocidad (%)')
    ax.set_xlabel('Tiempo (s)')
    ax.set_title('(b)')


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
