import * as fs from "fs/promises";
import * as path from "path";

import * as yaml from "yaml";
import { danger, fail, message, results } from "danger";
import { existsSync } from "fs";

const BAD_FILES = ["node_modules", "__pycache__"];
let ROOT = __dirname;
do {
  if (ROOT === "/") {
    throw new Error("Unable to find git repository");
  }
  ROOT = path.resolve(ROOT, "..");
} while (!existsSync(path.join(ROOT, ".git")));

let failed = false;

const handleError = (err: unknown, challenge?: string) => {
  failed = true;
  if (!challenge) {
    challenge = "unknown";
  }
  if (typeof err === "string") {
    fail(`${challenge} : ${err}`);
  } else if (err instanceof Error) {
    console.error(err);
    fail(`${challenge} : Exception "${err.message}", consulter les logs`);
  } else {
    console.trace(err);
    fail(`${challenge} : Erreur inconnue, consulter les logs`);
  }
};

const getFailLogger = (challenge: string) => {
  return (err: string) => handleError(err, challenge);
};

async function* walk(dir: string): AsyncIterableIterator<string> {
  for await (const entry of await fs.opendir(dir)) {
    const entryPath = path.join(dir, entry.name);
    if (entry.isDirectory()) yield* walk(entryPath);
    else if (entry.isFile()) yield entryPath;
  }
}

// Fonction pour extraire les URLs d'images de la description
const extractImageUrls = (description: string) => {
  const regex = /!\[.*?\]\((.*?)\)/g;
  let match: RegExpExecArray | null;
  const urls: string[] = [];
  while ((match = regex.exec(description)) !== null) {
    urls.push(match[1]!);
  }
  return urls;
};

/**
 * Vérifie si un fichier/dossier existe
 * @param filePath Chemin à vérifier
 * @param isDir Si true, alors le chemin doit être un dossier
 * @returns
 */
const exists = async (filePath: string, isDir = false) => {
  try {
    const stat = await fs.stat(filePath);
    return isDir ? stat.isDirectory() : stat.isFile();
  } catch (err) {
    return false;
  }
};

/**
 * Vérifie les fichiers/dossiers obligatoires en fonction du type de challenge
 * @param folder Chemin pointant vers le dossier du challenge
 * @returns
 */
const checkRequiredFilesAndFolders = async (folder: string) => {
  const logFail = getFailLogger(folder);
  const folderPath = path.join(ROOT, folder);

  // Vérification de la présence du fichier README.md
  if (!(await exists(path.join(folderPath, "README.md")))) {
    logFail("Le fichier `README.md` est absent");
  }

  // Vérification de la présence du dossier solve
  if (!(await exists(path.join(folderPath, "solve"), true))) {
    logFail('Le dossier "solve" est absent');
  } else if (!(await exists(path.join(folderPath, "solve", "WRITEUP.md")))) {
    logFail("Un writeup doit être rédigé dans le fichier solve/WRITEUP.md");
  }

  // Vérification de la présence du dossier src
  if (!(await exists(path.join(folderPath, "src"), true))) {
    logFail('Le dossier "src" est absent');
  }

  let haveDockerfile = false;
  for await (const entry of walk(folderPath)) {
    const filename = path.basename(entry);

    if (filename === "Dockerfile") haveDockerfile = true;

    let badFile: string | undefined;
    if ((badFile = BAD_FILES.find((f) => f === filename)) !== undefined) {
      logFail(`Le dossier ${badFile} ne doit pas être commit`);
    }
  }

  // Vérification de la présence du fichier challenge.yml ou challenge.yaml
  const challengeYmlPath = path.join(folderPath, "challenge.yml");
  const challengeYamlPath = path.join(folderPath, "challenge.yaml");

  let yamlContent = null;
  if (await exists(challengeYmlPath)) {
    yamlContent = await fs.readFile(challengeYmlPath, "utf8");
  } else if (await exists(challengeYamlPath)) {
    yamlContent = await fs.readFile(challengeYamlPath, "utf8");
  } else {
    logFail(`Le fichier "challenge.yml" ou "challenge.yaml" absent`);
    return;
  }

  // Vérifier le contenu du fichier YAML
  const yamlData = yaml.parse(yamlContent) ?? {};

  // 1. Title + maj
  if ((yamlData["name"] ?? "").trim() === "") {
    logFail(' Le champ "name" (titre du challenge) ne doit pas être vide');
  } else if (!/^[A-ZÀ-Ÿ]/.test(yamlData["name"].trim())) {
    logFail(" Le titre du challenge doit commencer par une majuscule");
  }


  //1.5 Catégorie du Challenge 
  
  if ((yamlData["category"] ?? "").trim() === "") {
    logFail(' Le champ "category" (catégorie du challenge) ne doit pas être vide');
  } else if (!/^[A-ZÀ-Ÿ]/.test(yamlData["category"].trim())) {
    logFail(" La catégorie du challenge doit commencer par une majuscule");
  }
 

  // 2. Auteur
  if ((yamlData["author"] ?? "").trim() === "") {
    logFail('Le champ "author" ne doit pas être vide');
  }

  if ((yamlData["attribution"] ?? "").trim() === "") {
    logFail('Le champ "attribution" ne doit pas être vide');
  }

  if ((yamlData["attribution"] ?? "").trim() === "") {
    logFail('Le champ "attribution" ne doit pas être vide');
  }

  // 3. Description et présence d'image(s)
  if ((yamlData["description"] ?? "").trim() === "") {
    logFail('Le champ "description" ne doit pas être vide');
  } else {
    const imageUrls = extractImageUrls(yamlData["description"]);
    if (imageUrls.length === 0) {
      logFail(" La description doit contenir au moins une image");
    } else {
      await Promise.all(
        imageUrls.map(async (url) => {
          try {
            const response = await fetch(url);
            if (response.status >= 400) {
              logFail(
                `L'image à l'URL "${url}" n'existe pas ou n'est pas accessible`
              );
            }
          } catch (err) {
            logFail(`Impossible d'accéder à l'image à l'URL "${url}"`);
          }
        })
      );
    }
  }

  // 4. Info de connexion
  if (yamlData["type"] === "dynamic") {
    if (haveDockerfile && yamlData["connection_info"]?.trim() === "") {
      logFail(
        'Le champ "connection_info" doit être renseigné lorsque le type est "dynamic"'
      );
    }
    if (yamlData["extra"]?.template_name) {
      logFail(
        'Le champ "extra.template_name" ne doit pas être présent pour les challenges du type "dynamic"'
      );
    }
  } else if (yamlData["type"] === "ctfkit") {
    if (yamlData["connection_info"]) {
      logFail(
        'Le champ "connection_info" ne doit pas être présent pour les challenges du type "ctfkit"'
      );
    }
    if (yamlData["extra"]?.template_name?.trim() === "") {
      logFail(
        'Le champ "extra.template_name" doit être renseigné pour les challenges du type "ctfkit"'
      );
    }
  } else {
    logFail('Le type du challenge doit être "ctfkit" ou "dynamic"');
  }

  // 5. Flag non null
  if (!(yamlData["flags"]?.length > 0)) {
    logFail('Le champ "flags" doit être une liste contenant au moins un flag');
  } else {
    for (const flag of yamlData["flags"]) {
      if (typeof flag !== "string") {
        logFail("Le flag doit être une chaine de caractères");
      }
      if (!flag.match(/^BZHCTF{.+}$/)) {
        logFail('Le flag ne correspond pas au format "BZHCTF{.*}"');
      }
    }
  }

  // 6. Difficulte
  const validDifficulties = [
    "Très Facile",
    "Facile",
    "Moyen",
    "Difficile",
    "Très Difficile",
  ];
  const hasDifficultyTag = yamlData["tags"]?.some((tag: string) =>
    validDifficulties.includes(tag)
  );
  if (!hasDifficultyTag) {
    logFail(
      `Le champ "tags" doit contenir au moins une difficulté parmi : ${validDifficulties.join(
        ", "
      )}`
    );
  }

  // 7. Fichiers
  if (yamlData["files"]) {
    for (const file of yamlData["files"]) {
      if (!(await exists(path.join(folderPath, file)))) {
        logFail(`Le fichier ${file} est introuvable`)
      }
    }
  }

  // 8. Version == "0.1"
  if (yamlData["version"] !== "0.1") {
    logFail('Le champ "version" doit être égal à "0.1"');
  }
};

// Fonction principale
const main = async () => {
  try {
    const CATEGORIES = await fs
      .readFile(path.join(ROOT, ".categories"), "utf8")
      .then((file) =>
        file.split("\n").filter((line) => line.trim().length > 0)
      );

    const modifiedFiles = [
      ...danger.git.modified_files,
      ...danger.git.created_files,
    ];

    const challenges = new Set(
      modifiedFiles
        .map((path) => path.split("/").slice(0, 3))
        .filter(
          (components): components is [string, string] => components.length > 2
        )
        .filter(([category]) => CATEGORIES.includes(category))
        .map((components) => components.slice(0, 2).join("/"))
    );

    if (challenges.size === 0) {
      message("Aucun fichier modifié détecté dans cette PR.");
    } else {
      message(
        "Challenges modifiés :\n\n - " + [...challenges.values()].join("\n - ")
      );
    }

    await fs.writeFile(path.join(ROOT, 'changes.env'), 'REVIEW_CHALLENGES=' + [...challenges.values()].join(' '))

    // Vérification de chaque fichier YAML modifié
    for (const folder of challenges.values()) {
      await checkRequiredFilesAndFolders(folder);
    }

    if (results.fails.length === 0) {
      message("Toutes les vérifications ont été passées avec succès.");
    }
  } catch (err) {
    handleError(err);
  }
};

const unapprove = async () => {
  try {
    await danger.gitlab.api.MergeRequestApprovals.unapprove(
      danger.gitlab.mr.project_id,
      danger.gitlab.mr.iid
    );
  } catch {}
}

const approve = async () => {
  try {
    await danger.gitlab.api.MergeRequestApprovals.approve(
      danger.gitlab.mr.project_id,
      danger.gitlab.mr.iid
    );
  } catch {}
}

main()
  .catch(async (err: Error) => {
    handleError(err);
    await unapprove();
  })
  .then(async () => {
    if (failed) {
      await unapprove();
    } else {
      await approve();
    }
  });
