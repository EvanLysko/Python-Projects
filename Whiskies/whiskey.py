import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster.bicluster import SpectralCoclustering

whisky = pd.read_csv("/Users/evanlysko/Desktop/PythonforResearch/Whiskies/whiskies.txt")
whisky["Region"] = pd.read_csv("/Users/evanlysko/Desktop/PythonforResearch/Whiskies/regions.txt")

flavors = whisky.iloc[:, 2:14]
corr_flavors = pd.DataFrame.corr(flavors)
print(corr_flavors)

plt.figure(figsize=(10, 10))
plt.pcolor(corr_flavors)
plt.colorbar()
plt.savefig("corr_flavors.pdf")

corr_whisky = pd.DataFrame.corr(flavors.transpose())
plt.figure(figsize=(10, 10))
plt.pcolor(corr_whisky)
plt.axis("tight")
plt.colorbar()
plt.savefig("corr_whisky.pdf")
model = SpectralCoclustering(n_clusters=6, random_state=0)
print(model.fit(corr_whisky))
print(np.sum(model.rows_, axis=1))
print(np.sum(model.rows_, axis=0))

whisky['Group'] = pd.Series(model.row_labels_, index=whisky.index)
whisky = whisky.iloc[np.argsort(model.row_labels_)]
whisky = whisky.reset_index(drop=True)
correlations = pd.DataFrame.corr(whisky.iloc[:,2:14].transpose())
correlations = np.array(correlations)

plt.figure(figsize = (14,7))
plt.subplot(121)
plt.pcolor(corr_whisky)
plt.title("Original")
plt.axis("tight")
plt.subplot(122)
plt.pcolor(correlations)
plt.title("Rearranged")
plt.axis("tight")
plt.savefig("correlations.pdf")
