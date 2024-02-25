from dotenv import load_dotenv
from jira import JIRA
import pandas as pd
import os

load_dotenv()
MAX_RESULTS=100
jira = JIRA(server="https://issues.redhat.com/", token_auth=os.environ["JIRA_TOKEN"])

issues = jira.search_issues('project in (RHOAIENG) AND component = "Model Registry" AND summary ~ "GH model*"', maxResults=MAX_RESULTS)

if len(issues) == MAX_RESULTS:
    print("ERROR: probably not collecting all issues")
    raise

issues = [x for x in issues if x.fields.summary.startswith("GH model-registry-bf4-kf/")]
print(len(issues))

for issue in issues:
    print('{}: {}'.format(issue.key, issue.fields.summary))
    new_description = issue.fields.description.replace("https://github.com/opendatahub-io/model-registry/", "https://github.com/opendatahub-io/model-registry-bf4-kf/")
    if new_description == issue.fields.description:
        print("INFO: nothing to replace in description, skipping")
        continue
    issue.update(description=new_description)
    print(f"{issue.key} description updated to: {new_description}")
    print("done.")
