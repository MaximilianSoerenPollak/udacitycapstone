import csv
import os
import requests as r
from time import sleep
from decouple import config

# Increase recursion limit. sys.setrecursionlimit(10**6)
# ---- CLASS DEFINITION ----


class api:
    def __init__(self, url, auth, name, *args, **kwargs):
        self.url = url
        self.auth = auth
        self.name = name
        self.extra_headers = kwargs.get("extra_headers", None)
        self.auth_method = kwargs.get("auth_method", None)

    def _make_auth_string(
        self,
    ):
        return {"Authorization": f"{self.auth_method} {self.auth}"}

    def _make_header(self):
        if self.extra_headers:
            h1 = self._make_auth_string()
            h2 = self.extra_headers
            headers = {**h1, **h2}
            return headers
        else:
            return self._make_auth_string()

    def req(self, **kwargs):
        query = kwargs.get("query", None)
        if query == None:
            url = self.url
        else:
            url = self.url + "?" + query
        request = r.request(url=url, headers=self._make_header(), method="get")
        return request


# ---- Functions ----


class github_api(api):
    def __init__(self, url, auth, name, *args, **kwargs):
        super().__init__(url, auth, name, *args, **kwargs)

    def get_next_page_query(self, query):
        since = (
            query.headers.get("Link")
            .split()[0]
            .replace("<", "")
            .replace(">", "")
            .replace(";", "")
            .split("&")[1]
        )
        return "&" + since

    def get_all_data(self, **kwargs):
        first_run = kwargs.get("first_run", True)
        if first_run:
            # Checking if file excists and first run.
            # If so we want to continue where we left of. This is what this does.
            file_exists = os.path.isfile("github_api.csv")
            if file_exists:
                with open("github_api.csv", "r") as f:
                    last_id = f.readlines()[-1].split(",")[0]
                query = "page=1&since=" + str(last_id)
            # If file doen't excists we start at 0.
            else:
                query = "page=1"
            response = super().req(query=query)
            fields = kwargs.get("fields")
            self.get_info(response=response, fields=fields)
            next_page = self.get_next_page_query(response)
            sleep(0.1)
            self.get_all_data(first_run=False, next_page=next_page, fields=fields)
        else:
            q1 = kwargs.get("next_page")
            query = "page=1" + q1
            response = super().req(query=query)
            fields = kwargs.get("fields")
            self.get_info(response=response, fields=fields)
            next_page = self.get_next_page_query(response)
            rate_limit = response.headers.get("X-RateLimit-Remaining")
            # Checking if we reached the rate limit. If so we go to sleep for 1h.
            if rate_limit == 1:
                print("Sleeping to keep under the rate limit.")
                sleep(3660)
            # Checking if we have enough Rows in our CSV.
            # If this is the case, we terminate the programm.
            if self.check_csv() >= 1000000:
                print("CSV is bigger than 1Mil. rows.")
                os._exit(0)
            sleep(0.01)
            self.get_all_data(first_run=False, next_page=next_page, fields=fields)

    def check_csv(self):
        with open("github_api.csv") as f:
            return sum(1 for row in f)

    # Gives us the remaining API calls until we hit the limit
    def get_rate_limit(self, query):
        return query.headers.get("X-RateLimit-Remaining")

    # This is the reset time when the Rate limit resets in Unix time.
    def get_rate_limit_reset(self, query):
        return query.headers.get("X-RateLimit-Reset")

    def get_info(self, **kwargs):
        info_fields = kwargs.get("fields")
        response = kwargs.get("response")
        response_dict = response.json()
        # Define all the empty lists.
        full_list = []
        for item in response_dict:
            if item == None:
                continue
            item_list = []
            for field in info_fields:
                if type(field) == list:
                    try:
                        item_list.append(item[field[0]][field[1]])
                    except KeyError:
                        item_list.append("Null")
                else:
                    try:
                        item_list.append(item[field])
                    except KeyError:
                        item_list.append("Null")
            full_list.append(item_list)
        file_exists = os.path.isfile("github_api.csv")
        with open("github_api.csv", "a") as f:
            headers = [
                "id",
                "name",
                "full_name",
                "owner_login",
                "owner_id",
                "owner_login",
                "owner_html_url",
                "owner_type",
                "html_url",
                "description",
                "fork",
                "language",
                "forks_count",
                "watchers_count",
                "open_issues_count",
                "is_template",
                "topics",
                "has_issues",
                "has_projects",
                "has_wiki",
                "has_pages",
                "has_downloads",
                "created_at",
                "updated_at",
                "template_repo",
                "archived",
                "disabled",
            ]
            writer = csv.writer(f, lineterminator="\n")
            if not file_exists:
                writer.writerow(headers)
            writer.writerows(full_list)

    def remove_file(self):
        if os.path.isfile("github_api.csv"):
            os.remove("github_api.csv")


# ---- CONFIGS ----

github_api_url = config("GITHUB_API_URL")
github_token = config("GITHUB_TOKEN")
github_header = {
    "Accept": "application/vnd.github.v3+json",
}
gh_fields_wanted = [
    "id",
    "name",
    "full_name",
    ["owner", "login"],
    ["owner", "id"],
    ["owner", "login"],
    ["owner", "html_url"],
    ["owner", "type"],
    "html_url",
    "description",
    "fork",
    "language",
    "forks_count",
    "watchers_count",
    "open_issues_count",
    "is_template",
    "topics",
    "has_issues",
    "has_projects",
    "has_wiki",
    "has_pages",
    "has_downloads",
    "created_at",
    "updated_atb",
    "template_repo",
    "archived",
    "disabled",
]

# ---- INSTANTIATE CLASS ----
gh_api = github_api(
    github_api_url,
    github_token,
    name="github",
    extra_headers=github_header,
    auth_method="token",
)


def main():
    try:
        gh_api.get_all_data(fields=gh_fields_wanted)
    except Exception as e:
        print(e)
        print("Sleeping 1min now. Then trying again")
        sleep(60)
        main()


if __name__ == "__main__":
    main()
