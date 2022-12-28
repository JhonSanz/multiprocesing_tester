import pandas as pd
import matplotlib.pyplot as plt



#read
df = pd.read_csv("test_results_1/results_1.csv")

#line plot
plt.plot(df["params"], df["profit"], marker='o', markersize=1)

# promedio
plt.axhline(y = df["profit"].mean() , color = 'r', linestyle = '--')

# etiquetas
plt.title("Grafico 1")
plt.xlabel("Average")
plt.ylabel("Profit")
plt.xticks(df["params"][::20],rotation = 90, fontsize=7)

plt.show()