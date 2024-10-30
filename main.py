import json
import argilla as rg

client = rg.Argilla(api_url="http://localhost:6900", api_key="argilla.apikey")

# create a workspace
workspace = rg.Workspace(name="argilla", client=client)
workspace.create()

settings = rg.Settings(
    guidelines="Write a commit message given a git diff.",
    fields=[
        rg.TextField(
            name="diff",
            title="Git diff",
            use_markdown=False,
        ),
    ],
    questions=[
        rg.TextQuestion(
            name="commit_message_title",
            title="Write a commit message title given a git diff.",
        ),
        rg.TextQuestion(
            name="commit_message_description",
            title="Write a commit message description given a git diff.",
        ),
    ],
)
dataset = rg.Dataset(
    name=f"git-commit-messages",
    workspace="argilla",  # change this to your workspace
    settings=settings,
    client=client,
)
dataset.create()

# load data from json file
with open("sample-data.json", "r") as f:
    data = json.load(f)

records = [
    rg.Record(
        fields={
            "diff": data["diff"],
        },
        suggestions=[
            rg.Suggestion(
                "commit_message_title",
                data["commit_message"]["title"],
            ),
            rg.Suggestion(
                "commit_message_description",
                data["commit_message"]["description"],
            ),
        ],
    )
    for data in data["samples"]
]

dataset.records.log(records)
