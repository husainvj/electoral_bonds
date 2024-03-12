import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
bonds=pd.read_csv('assets/bond_details.csv', sep=';')
party=pd.read_csv('assets/party_details.csv', sep=';')

party