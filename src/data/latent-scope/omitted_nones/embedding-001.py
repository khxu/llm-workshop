import h5py
import numpy as np
import pandas as pd

with h5py.File('src/data/latent-scope/omitted_nones/embedding-001.h5', 'r') as emb_file:
  embeddings = np.array(emb_file["embeddings"])
  print(embeddings.shape)
  print(embeddings[:5])  # Print the first 5 embeddings to verify content

df = pd.read_parquet('src/data/latent-scope/omitted_nones/scopes-001-input.parquet')
print(df.shape)  # Print the shape of the DataFrame to verify dimensions
print(df.head())  # Display the first few rows of the DataFrame to verify content

# zip the embeddings with the DataFrame
df['embeddings'] = list(embeddings)
print(df.head())  # Display the DataFrame with embeddings to verify the addition

df.to_parquet('src/data/latent-scope/omitted_nones/scopes-001-embeddings.parquet', index=False)
print("DataFrame with embeddings saved successfully.")