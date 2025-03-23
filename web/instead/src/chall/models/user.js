import { DataTypes } from 'sequelize';
import {sequelize} from "../db.js";
import { Op } from 'sequelize';
import crypto from 'crypto';

const User = sequelize.define('User', {
    id: {
        type: DataTypes.UUID,
        defaultValue: DataTypes.UUIDV4,
        primaryKey: true,
        unique: true
    },
    username: {
        type: DataTypes .STRING,
        allowNull: false,
        unique: true
    },
    password: {
        type: DataTypes .STRING,
        allowNull: false
    },
    role: {
        type: DataTypes .ENUM("user","administrator"),
        defaultValue: "user",
    },
    profilePicture: {
        type: DataTypes.STRING,
        defaultValue: "/static/img/pfp1.png"
    },
    resetToken: {
        type: DataTypes.STRING,
        allowNull: true
      },
    resetTokenExpiration: {
        type: DataTypes.DATE,
        allowNull: true
      }
});

User.associate = (models) => {
    User.hasMany(models.Post, { as: "posts", foreignKey: "userId", onDelete: "CASCADE" });
    User.hasMany(models.Comment, { as: "comments", foreignKey: "userId", onDelete: "CASCADE" });
    User.hasOne(models.CV, { as: "cv", foreignKey: "userId", onDelete: "SET NULL" });
};

User.createNewUser = async function (username,password,role="guest"){
    try{
        const user = await this.create({username,password,role});
    }
    catch(e){
        throw new Error("Erreur lors de la création de l'utilisateur")
    }
};

User.login = async function (username,password) {
    try {
        const user = await this.findOne({where: {username,password}});
        if(!user){
            throw new Error("Nom d'utilisateur ou mot de passe incorrect")
        }
        return user;
    }
    catch(e){
        throw new Error("Erreur lors de la connexion");
    }
};

User.getUserWithUsername = async function (username) {
    try {
        const user = await this.findOne({where: {username}});
        if(!user){
            throw new Error("Utilisateur introuvable")
        }
        return user;
    }
    catch(e){
    }
};

User.generateResetToken = async function (username) {
    try {
        const token = crypto.randomBytes(32).toString('hex');
        const expiration = new Date(Date.now() + 5 * 60 * 1000);
        const user = await this.findOne({ where: { username } });
        if (!user) {
            throw new Error("Utilisateur introuvable");
        }
        user.resetToken = token;
        user.resetTokenExpiration = expiration;
        await user.save();
    }
    catch(e){
    }
  };

User.checkResetToken = async function(username, providedToken) {
  try {
    const user = await this.findOne({
      where: {
        username,
        resetToken: { [Op.like]: providedToken },
        resetTokenExpiration: { [Op.gte]: new Date() }
      }
    });
    if (!user) {
      throw new Error("Token invalide");
    }
    return user;
  } catch (e) {
    throw new Error("Erreur lors de la vérification du token: " + e.message);
  }
};

User.resetPassword = async function(username, newHashedPassword) {
  try {
    const user = await this.findOne({ where: { username } });
    if (!user) {
      throw new Error("Utilisateur introuvé");
    }
    user.password = newHashedPassword;
    user.resetToken = null;
    user.resetTokenExpiration = null;
    await user.save();
  } catch (e) {
    console.error("Erreur dans User.resetPassword:", e);
    throw new Error("Erreur lors de la réinitialisation du mot de passe");
  }
};

export default User;