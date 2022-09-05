from pyspark.sql import SparkSession
from pyspark.sql.functions import isnan, when, count, col

# Have to set the Memory allocation higher to enable saving via CSV.
spark = (
    SparkSession.builder.appName("DataExploraiton")
    .config("spark.executor.memory", "7g")
    .config("spark.driver.memory", "7g")
    .getOrCreate()
)
# ---- Cleaning GH CSV ----
df_gh = spark.read.csv(path="data/github/raw/gh_raw.csv", header=True, sep=",")
# Rows we want to check for "Null" (according to the data acquisiton).
check_cols = [
    "language",
    "topics",
    "template_repo",
    "archived",
    "disabled",
    "forks_count",
    "watchers_count",
    "open_issues_count",
    "is_template",
    "has_issues",
    "has_projects",
    "has_wiki",
    "has_pages",
    "has_downloads",
    "created_at",
    "updated_at",
]
# Dropping the duplicate column + rows
# Checking which rows have a lot of "Null" in them. And dropping them
df_gh_clean = df_gh.drop("owner_login5")
df_gh_clean = df_gh_clean.withColumnRenamed("owner_login3", "owner_login")
df_gh_clean = df_gh_clean.dropna(
    subset=["id", "name", "full_name", "owner_login", "owner_id", "owner_html_url"],
)
# df_gh_clean = df_gh_clean.filter(col("owner_id") == "Null")

rows_to_filter = df_gh_clean.filter(df_gh_clean.fork.like("Null"))
rows_to_filter2 = df_gh_clean.filter(df_gh_clean.owner_type.like("Null"))
rows_to_filter3 = df_gh_clean.filter(df_gh_clean.id.startswith("Planning"))
df_clean = df_gh_clean.join(rows_to_filter, on=["id"], how="left_anti")
df_clean = df_clean.join(rows_to_filter2, on=["id"], how="left_anti")
df_clean = df_clean.join(rows_to_filter3, on=["id"], how="left_anti")
df_clean = df_clean.drop(
    "forks_count",
    "language",
    "topics",
    "disabled",
    "template_repo",
    "archived",
    "watchers_count",
    "open_issues_count",
    "is_template",
    "has_issues",
    "has_projects",
    "has_wiki",
    "has_pages",
    "has_downloads",
    "created_at",
    "updated_at",
)


df_clean = df_clean.dropDuplicates()


df_clean.toPandas().to_csv("data/github/clean/gh_clean.csv", index=False)
