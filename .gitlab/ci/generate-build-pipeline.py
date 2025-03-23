from pathlib import Path
import yaml
import logging
import os
from rich.console import Console
from rich.logging import RichHandler

logging.basicConfig(level=logging.DEBUG, format="%(message)s",
                    datefmt="[%X]", handlers=[RichHandler()])

logger = logging.getLogger("bzhctf")

ROOT = Path().absolute()
while not (ROOT / ".git").exists():
    ROOT = ROOT.parent
    assert ROOT != Path("/"), "Unable to locate git repository"


def parse_challenges():
    try:
        REGISTRY = os.environ.get("CI_REGISTRY_IMAGE", "")
        if REGISTRY == "":
            logger.warning("CI_REGISTRY_IMAGE variable is not set")
        BRANCH = os.environ.get("CI_COMMIT_BRANCH", "")

        logger.info("Found git repository at %s", ROOT.as_posix())

        categories_list = ROOT / ".categories"
        assert categories_list.exists(), ".categories file is missing"
        CATEGORIES = categories_list.read_text().splitlines()
        logger.info("Found %d categories", len(CATEGORIES))
        logger.info('/'.join(CATEGORIES))

        challenges = []
        build_pipeline = []

        for category in CATEGORIES:
            category_folder = ROOT / category

            logger.debug("Starting parsing of category \"%s\"",
                         category_folder.name)
            assert category_folder.exists(), f"Category folder {
                category} is missing"
            assert category_folder.is_dir(), f"Category {
                category} must me a folder"

            for challenge_folder in category_folder.iterdir():
                challenge_name = challenge_folder.name.lower()

                challenges.append((category_folder.name, challenge_name))

                logger.debug(
                    "Starting parsing of challenge \"%s\"", challenge_name)

                if (gitlab_ci := challenge_folder / '.gitlab-ci.yml').is_file():
                    logger.info(
                        "Found gitlab-ci.yml for %s, it will be included in the pipeline", challenge_name)
                    build_pipeline.append(
                        gitlab_ci.relative_to(ROOT).as_posix())

                else:
                    for dockerfile in challenge_folder.glob("**/*Dockerfile"):
                        if dockerfile.name == "Dockerfile":
                            logger.info("Found main Dockerfile")
                            suffix = ""
                        elif dockerfile.suffix == ".Dockerfile":
                            logger.info(
                                "Found additional Dockerfile: %s", dockerfile.name)
                            suffix = f"-{dockerfile.stem}"

                        build_pipeline.append({
                            "rules": [{
                                "changes": [
                                    (challenge_folder /
                                     "**/*").relative_to(ROOT).as_posix()
                                ]
                            }],
                            "component": f"{os.environ.get("CI_SERVER_FQDN")}/breizh-ctf-2025/challenge/ci-components/kaniko@1.2.8",
                            "inputs": {
                                "stage": f"{challenge_name}{suffix}",
                                "dockerfile": dockerfile.relative_to(ROOT).as_posix(),
                                "context": dockerfile.parent.relative_to(ROOT).as_posix(),
                                "image": f"{REGISTRY}/{challenge_name}{suffix}",
                                "kaniko_args": f"--build-arg 'REGISTRY=docker.io'"
                            }
                        })

                logger.debug("End parsing of \"%s\"", challenge_name)

            logger.debug("End parsing of category \"%s\"",
                         category_folder.name)

        gitlab_ci = {
            "include": build_pipeline
        }
        return challenges, gitlab_ci

    except AssertionError:
        Console().print_exception()


if __name__ == "__main__":
    challenges, gitlab_ci = parse_challenges()

    output_file = ROOT / "build.gitlab-ci.yml"
    with output_file.open("w") as f:
        f.write(yaml.dump({
            "stages": [
                "build"
            ],
            "workflow": {
                "rules": [{
                    "when": "always"
                }]
            }
        }))
        f.write(yaml.dump(gitlab_ci))
        f.write("\n")
        f.write(yaml.dump({
            "empty-job": {
                "stage": "build",
                "variables": {
                    "GIT_STRATEGY": "none"
                },
                "script": [
                    "echo NOP"
                ]
            }
        }))

    logger.info("Gitlab pipeline written at %s", output_file.as_posix())
