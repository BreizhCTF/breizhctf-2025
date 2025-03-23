# BreizhCTF 2025 | Write-up : AutHentification 1 [Crypto]

L'objectif de ce challenge est de forger un cookie admin afin d'accéder à l'espace administrateur. Pour cela, il faut réussir à chiffrer du JSON contenant la charge utile : `"role": "super_admin"`.

Pour le chiffrement, c'est de l'AES-GCM 128 qui est utilisé. Dans notre cas, nous pouvons voir ce chiffrement comme de l'AES-CTR, en effet, l'authenticité n'est pas vérifiée ; on le remarque dans le code `crypto.py` en faisant du diffing avec le même challenge de difficulté supérieure.

Nous pouvons également remarquer que la clé AES est constante et l'IV est fixé à 0, le keystream sera donc toujours le même. En combinant cela au fait que nous pouvons nous créer un compte en choisissant le nom d'utilisateur (appelons-le compte 1, et notons `C1` son cookie), nous sommes capables de forger un cookie admin (appelons le compte 2, et notons `C2` son cookie) !

En effet, le cookie user vaut : `C1 = keystream XOR JSON_user`, nous connaissons `JSON_user`, nous pouvons alors récupérer le keystream, car : `keystream = C1 XOR JSON_user`.
Nous pouvons maintenant forger `C2` en faisant : `C2 = keystream XOR JSON_admin`, avec `JSON_admin` un JSON de notre choix contenant le rôle `super_admin`.

Une implémentation complète de cette solution est disponible en Python dans le fichier `solve.py`.
