import configparser
from aws_startup import iam, DWH_IAM_ROLE_NAME
from sys import argv

# ---- LOAD CONFIGS ----

config = configparser.ConfigParser()
config.read_file(open("dwh.cfg"))
rolearn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)["Role"]["Arn"]

# ---- Drop table commands ----
drop_table_gh = "DROP TABLE IF EXISTS github CASCADE;"
drop_table_libio = "DROP TABLE IF EXISTS libio CASCADE;"

# ---- Create Table commands ----
create_table_gh = """
CREATE TABLE IF NOT EXISTS 
gh(
    id BIGINT IDENTITY(1, 1),
    gh_id BIGINT,
    name VARCHAR,
    full_name VARCHAR,
    owner_login VARCHAR,
    owner_id BIGINT,
    owner_html_url VARCHAR(MAX),
    owner_type VARCHAR,
    html_url VARCHAR(MAX),
    description VARCHAR(MAX),
    fork VARCHAR(MAX));
"""

create_table_libio = """
CREATE TABLE IF NOT EXISTS lib(
  id BIGINT IDENTITY(1, 1),
  host_type VARCHAR,
  name_with_owner VARCHAR,
  description VARCHAR(MAX),
  fork VARCHAR,
  created_at Timestamp,
  updated_at Timestamp,
  last_pushed Timestamp,
  homepage_url VARCHAR(MAX),
  stars_count REAL,
  language VARCHAR(MAX),
  issues_enabled VARCHAR,
  wiki_enabled VARCHAR,
  pages_enabled VARCHAR,
  forks_count REAL,
  mirror_url VARCHAR(MAX),
  default_branch VARCHAR(MAX),
  watchers REAL,
  uuid VARCHAR,
  fork_source VARCHAR(MAX),
  contributors VARCHAR(MAX),
  readme_filename VARCHAR(MAX),
  changelog_filename VARCHAR(MAX),
  source_rank REAL,
  display_name VARCHAR(MAX));
"""
# ---- INSERT DATA INTO TABLES -----
insert_gh_data = (
    """
COPY gh (gh_id, name, full_name, owner_login, owner_id, owner_html_url, owner_type, html_url, description, fork)
FROM 's3://{}/gh_clean.csv'
iam_role '{}'
CSV
IGNOREHEADER 1;
"""
).format(config["S3"]["BUCKETNAME"], rolearn)

insert_libio_data = (
    """ 
COPY lib (
  host_type,
  name_with_owner,
  description,
  fork,
  created_at,
  updated_at,
  last_pushed,
  homepage_url,
  stars_count,
  language,
  issues_enabled,
  wiki_enabled,
  pages_enabled,
  forks_count,
  mirror_url,
  default_branch,
  watchers,
  uuid,
  fork_source,
  contributors,
  readme_filename,
  changelog_filename,
  source_rank,
  display_name)
FROM 's3://{}/clean_'
iam_role '{}'
CSV
IGNOREHEADER 1;
"""
).format(config["S3"]["BUCKETNAME"], rolearn)

# ---- Query List -----
drop_tables = [drop_table_gh, drop_table_libio]
create_tables = [create_table_gh, create_table_libio]
insert_data = [insert_gh_data, insert_libio_data]
