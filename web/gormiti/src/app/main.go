package main

import (
	"fmt"
	"net/http"
	"os"
	"strings"
	"regexp"

	"github.com/gin-gonic/gin"
	"golang.org/x/net/http2"
	"golang.org/x/net/http2/h2c"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type Post struct {
	ID      uint   `gorm:"primaryKey" json:"id"`
	Title   string `json:"title"`
	Image   string `json:"image"`
	Teaser  string `json:"teaser"`
	Content string `json:"content"`
}

type Secret struct {
	ID   uint   `gorm:"primaryKey" json:"id"`
	Flag string `json:"flag"`
}

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

func main() {
	gin.SetMode(gin.ReleaseMode)

	db, err := gorm.Open(sqlite.Open("gormiti.db"), &gorm.Config{})
	if err != nil {
		fmt.Println("Erreur de connexion à la base :", err)
		os.Exit(1)
	}
	if err := db.AutoMigrate(&Post{}, &Secret{}); err != nil {
		fmt.Println("Erreur lors de la migration :", err)
		os.Exit(1)
	}

	flagValue := os.Getenv("FLAG")
	if flagValue == "" {
		flagValue = "BZHCTF{FAKE_FLAG}"
	}

	var secretCount int64
	db.Model(&Secret{}).Count(&secretCount)
	if secretCount == 0 {
		db.Create(&Secret{Flag: flagValue})
	}

	var postCount int64
	db.Model(&Post{}).Count(&postCount)
	if postCount == 0 {
		db.Create(&Post{
			Title:   "Bienvenue dans le monde de Gormiti",
			Image:   "/static/img/affiche.jpg",
			Teaser:  "Un site web dédié à l'univers des Gormiti, pour les fans et par les fans.",
			Content: "Quand j'étais encore petit il y a quelques années maintenant, je regardais toujours un dessin animé super cool : Gormiti ! " +
				"Après tant d'années à penser à cela tous les jours... j'ai décidé de créer un site web pour partager ma passion avec tous les fans de Gormiti. " +
				"Vous y trouverez des articles sur les différents personnages, des images, des vidéos et bien plus encore. " +
				"Le site n'est qu'en béta pour le moment, mais j'espère qu'il vous plaira ! "+
				"Signé : Un fan caché de Gormiti qui pense que c'est le meilleur dessin animé de tous les temps !",
		})
		db.Create(&Post{
			Title:  "Gormiti : Les Seigneurs de la Nature – Une épopée légendaire !",
			Image:  "/static/img/affiche2.jpg",
			Teaser: "Découvrez la série animée qui a enflammé une génération, mêlant héros mythiques et redoutables adversaires dans une lutte épique pour la nature !",
			Content: "Plongez dans l'univers captivant de Gormiti : Les Seigneurs de la Nature, une série animée absolument inoubliable ! Chaque épisode vous transporte dans un monde où la nature est vivante et vibrante, où des héros aux pouvoirs ancestraux se dressent contre des forces obscures pour protéger notre planète. Imaginez des batailles épiques, des alliances inattendues et des intrigues remplies de mystères et d'émotions fortes ! En tant que fan passionné, je peux vous garantir que cette série est un véritable chef-d'œuvre, mêlant action, suspense et une esthétique qui vous fera vibrer. Préparez-vous à être transporté dans une aventure extraordinaire, où chaque moment est une célébration de l'esprit, du courage et de la beauté de la nature !",
		})
		db.Create(&Post{
			Title:   "Le Maître de l'Eau",
			Image:   "/static/img/eau.jpg",
			Teaser:  "Découvrez le maître de l'eau, gardien des abysses.",
			Content: "Issu d'une ancienne lignée, le Maître de l'Eau contrôle les courants et détient les secrets des profondeurs. " +
				"Sa sagesse et sa maîtrise des éléments aquatiques font de lui un leader naturel. Plongez dans son univers mystique et apprenez ses secrets.",
		})
		db.Create(&Post{
			Title:   "Le Gardien de la Terre",
			Image:   "/static/img/terre.jpg",
			Teaser:  "Plongez dans l'univers du Gardien de la Terre, symbole de force et résilience.",
			Content: "Né au cœur d'une terre ancestrale, le Gardien de la Terre incarne la robustesse et la stabilité. " +
				"Sa connexion intime avec la nature lui permet de protéger les secrets du sol et de maintenir l'équilibre écologique. " +
				"Découvrez son histoire, sa force tranquille et son engagement pour la préservation de l'environnement.",
		})
	}

	router := gin.Default()

	router.Static("/static", "./static")
	router.LoadHTMLGlob("templates/*")

	router.GET("/", func(c *gin.Context) {
		var posts []Post
		if err := db.Find(&posts).Error; err != nil {
			c.String(http.StatusInternalServerError, "Erreur de chargement des posts")
			return
		}
		c.HTML(http.StatusOK, "index.html", gin.H{"posts": posts})
	})

	router.GET("/post/:id", func(c *gin.Context) {
		id := c.Param("id")
		safeID := Sanitize(id)
		var post Post
		if err := db.First(&post, safeID).Error; err != nil {
			c.String(http.StatusNotFound, "Post introuvable")
			return
		}
		c.HTML(http.StatusOK, "post.html", gin.H{"post": post})
	})

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

	server := &http.Server{
		Addr:    "127.0.0.1:8080",
		Handler: h2c.NewHandler(router, &http2.Server{}),
	}
	if err := server.ListenAndServe(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
