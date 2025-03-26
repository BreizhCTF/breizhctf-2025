from jinja2 import Template
from pathlib import Path
import yaml
from ctfcli.core import api

api = api.API()

CATEGORIES = map(Path, Path(".categories").read_text().splitlines())
template = Template("""
## Challenges

| Challenge       | Auteur | Difficulté | Flags |
| --------------- | ------ | ---------- | ----- |
{% for challenge in challenges -%}
| [{{ challenge["name"] }}](./{{ challenge["folder"] }}) | {{ challenge["author" ]}} | {{ challenge["difficulty"] }} | {{ challenge["solves"] }} |
{% endfor %}
""")

difficulties = [
    "Très Facile",
    "Facile",
    "Moyen",
    "Difficile",
    "Très Difficile"
]

remote_challenges = api.get("/api/v1/challenges?view=admin").json().get("data")

chall_list = []
for category in CATEGORIES:
    challenges = []
    readme = category / "README.md"
    readme_content = readme.read_text().splitlines()
    start_line = readme_content.index("## Challenges")
    assert start_line is not None

    prepend = readme_content[:start_line]

    for entry in category.iterdir():
        if entry.is_dir():
            challenge = yaml.load((entry / "challenge.yml").open("r"), Loader=yaml.SafeLoader)
            name = challenge["name"]
            author = challenge["attribution"].split(":", 1)[-1].strip()
            difficulty = challenge["tags"][0]
            
            challenge_id = next(c["id"] for c in remote_challenges if c["name"] == name)
            solves = len(api.get(f"/api/v1/challenges/{challenge_id}/solves").json().get("data"))
            print(solves)

            challenges.append({
                "folder": entry.name,
                "name": name,
                "author": author,
                "difficulty": difficulty,
                "solves": solves
            })
    
    challenges.sort(key=lambda challenge: difficulties.index(challenge["difficulty"]))
    result = "\n".join(prepend) + template.render(challenges=challenges)
    readme.write_text(result)
