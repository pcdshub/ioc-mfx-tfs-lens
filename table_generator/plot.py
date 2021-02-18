import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


for fn in sys.argv[1:]:
    if fn.endswith('.pdf'):
        continue
    df = pd.read_csv(fn)
    df = df.set_index(df.energy)
    print(df)
    plt.figure()
    plt.plot(df.energy, df.low)
    plt.plot(df.energy, df.high)
    plt.yscale('log')
    plt.title(fn)
    plt.savefig(f'{fn}.pdf')
