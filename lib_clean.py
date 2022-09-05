from sys import getsizeof
from sys import argv
import pandas as pd

# Readin: first CSV for headers in.
df_first = pd.read_csv(("data/libcsv/lib_repo.csv"), index_col=False, nrows=1)
headers = df_first.columns.to_list()

# Should work #Pray
df1 = pd.read_csv(argv[1], index_col=False, header=0, names=headers, dtype=str)
df2 = df1[(df1["Readme filename"].str.len() <= 20) | (df1["Readme filename"].isnull())]
df2_clean = df2[(df2["Homepage URL"].str.len() <= 70) | (df2["Homepage URL"].isnull())]
df2_clean = df2_clean[~(df2_clean["Readme filename"].str.startswith("t", na=False))]
df2_clean = df2_clean[~(df2_clean["Created Timestamp"].str.lower() == "false")]
df2_clean = df2_clean[~(df2_clean["Host Type"].isnull())]
df2_clean["sizedescription"] = df2_clean["Description"].apply(lambda x: getsizeof(x))
df2_clean["sizedescription"].astype(int)
df2_clean.sort_values("sizedescription", ascending=False, inplace=True)
df2_clean = df2_clean[df2_clean["sizedescription"] <= 65534]
df2_clean = df2_clean.drop(
    [
        "Size",
        "ID",
        "Open Issues Count",
        "License",
        "Contributing guidelines filename",
        "License filename",
        "Code of Conduct filename",
        "Security Threat Model filename",
        "Security Audit filename",
        "Status",
        "Last Synced Timestamp",
        "Pull requests enabled",
        "Keywords",
        "SCM type",
        "Logo URL",
    ],
    axis=1,
)
# Here we check if we want to also compare it. If we don't want to comprae.
# We will drop the "sizedescription" column so we can send it to Redshift as is.
if argv[3] == "Yes":
    df2_clean = df2_clean.drop("sizedescription", axis=1)
df2_clean = df2_clean.drop_duplicates()
df2_clean.to_csv(("data/libcsv/clean/clean_" + str(argv[2]) + ".csv"), index=False)
