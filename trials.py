import pandas as pd

df = pd.read_excel("DDBB.xlsx", index_col=0)
slug = "reupholster-and-paint-6-wooden-dining-chairs-x01hzbx9hw9df1gvnfhbwgdz1g1"

df.loc[df["slug"] == slug, "applied"] = "Modified"
        
df.to_excel("DDBB.xlsx")
    