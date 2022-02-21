import pandas as pd

def convert_rdf_to_csv(filepath):
  rows= []
  with open(filepath) as f:
    for line in f:
      line= line.split(' ')
      if len(line) > 2:
        #print (line[:3])
        rows.append(line[:3])
  return pd.DataFrame(rows, columns=['sub',	'rel',	'obj'])

if __name__ == "__main__":
    df_train = convert_rdf_to_csv("dataset/human_kg_train.nt")
    df_train.to_csv("dataset/human_kg_train.csv", index=False)
