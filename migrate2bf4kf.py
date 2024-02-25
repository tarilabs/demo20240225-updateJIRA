from dotenv import load_dotenv
from jira import JIRA
import os

load_dotenv()
MAX_RESULTS=100

jira = JIRA(server="https://issues.redhat.com/", token_auth=os.environ["JIRA_TOKEN"])

issues = jira.search_issues('project in (RHOAIENG) AND component = "Model Registry" AND summary ~ "GH model*"', maxResults=MAX_RESULTS)

if len(issues) == MAX_RESULTS:
    print("ERROR: probably not collecting all issues")
    raise

for issue in issues:
    print('{}: {}'.format(issue.key, issue.fields.summary))
    if not issue.fields.summary.startswith("GH model-registry/"):
        print("INFO: not starting with GH model-registry/, skipping.")
        continue
    new_summary = issue.fields.summary.replace("GH model-registry/", "GH model-registry-bf4-kf/")
    new_description = issue.fields.description.replace("https://github.com/opendatahub-io/model-registry/", "https://github.com/opendatahub-io/model-registry-bf4-kf/")
    issue.update(summary=new_summary, description=new_description)
    print(f"{issue.key} updated to: {new_summary}")
    print("done.")