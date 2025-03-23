import { Sequelize } from "sequelize";
import { hashPassword } from "./utils.js";
import crypto from "crypto";

class Database {
  constructor() {
    this.sequelize = new Sequelize({
      dialect: "sqlite",
      storage: "./database.sqlite",
      logging: false,
    });
  }

  async connect() {
    try {
      await this.sequelize.authenticate();
      console.log("Connexion à la bdd réussie.");
    } catch (error) {
      console.error("Erreur lors de la connexion à la bdd", error);
    }
  }

  async migrate() {
    try {
      const { default: User } = await import("./models/user.js");
      const { default: Post } = await import("./models/post.js");
      const { default: Comment } = await import("./models/comment.js");
      const { default: CV } = await import("./models/cv.js");

      User.associate({ Post, Comment, CV });
      Post.associate({ User, Comment });
      Comment.associate({ User, Post });

      await this.sequelize.sync({ force: true });
      console.log("Synchronisation de la bdd réussie.");
      const [admin, user1, user2] = await User.bulkCreate(
        [
          {
            username: "admin",
            password: hashPassword(crypto.randomBytes(64).toString("hex")),
            role: "administrator",
            profilePicture: "/static/img/admin.jpg"
          },
          {
            username: "user1",
            password: hashPassword(crypto.randomBytes(64).toString("hex")),
            role: "guest",
            profilePicture: "/static/img/user1.jpg",
          },
          {
            username: "user2",
            password: hashPassword(crypto.randomBytes(64).toString("hex")),
            role: "guest",
            profilePicture: "/static/img/user2.jpg",
          },
        ],
        { returning: true }
      );

      const post1 = await Post.create({
        title: "Bienvenue sur Instead",
        content: "Notre plateforme est prête pour vous accueillir et nous espérons que vous y trouverez ce que vous cherchez !",
        userId: admin.id,
      });

      await Comment.bulkCreate([
        { content: "Bravo pour l'initiative !", userId: user2.id, postId: post1.id },
        { content: "Merci à vous ! J'ai hâte que les offres d'emplois soient mises en ligne", userId: user1.id, postId: post1.id },
      ]);

      const post2 = await Post.create({
        title: "Ma journée au travail",
        content: "Aujourd'hui, j'ai rencontré un problème avec le serveur de l'entreprise. J'ai passé la journée à le réparer. Je ne comprends pas pourquoi il a planté et je n'ai toujous pas réussi à le relancer...",
        userId: user2.id,
      });

      await Comment.create({
        content: "Comment puis-je aider ?",
        userId: user1.id,
        postId: post2.id,
      });
    } 
    catch (error) {
      console.error("Erreur lors de la migration de la base", error);
    }
  }
}

const db = new Database();

export default db;
export const sequelize = db.sequelize;