import User from "../models/user.js";
import {makeJWT, hashPassword} from"../utils.js";

const register = async (req, res) => {
    const {username, password} = req.body;
    try {
        const existingUser = await User.getUserWithUsername(username);
        if (existingUser) {
            return res.status(409).json({message: "Ce nom d'utilisateur n'est pas disponible", status: 409});
        }
        await User.createNewUser(username, hashPassword(password));
        return res.status(201).json({message: "Utilisateur enregistré avec succès"});
    }
    catch (e) {
        return res.status(500).json({message: e.message, status: 500});
    }
};

const login = async (req, res) => {
    const {username, password} = req.body;
    try{
        const user = await User.login(username, hashPassword(password));
        const jwt = makeJWT(user);
        res.cookie("jwt", jwt, {
            httpOnly: true,
            secure: false,
            sameSite: "Strict",
            maxAge: 60 * 60 * 1000
        });
        return res.status(200).json({
            message: "Connexion réussie"
        });
    }
    catch(e){
        return res.status(403).json({message: e.message, status: 403});
    }
};

const logout =(req, res) => {
    res.clearCookie("jwt", {path: "/"});
    res.redirect("/");
};

const resetPassword = async (req, res) => {
    const newPassword = req.body.newPassword;
    const username = req.user.username;
    const providedToken  = req.body.resetToken;
    try{
        await User.generateResetToken(username);
        /* TODO : Réaliser un envoie de mail pour le reset du mot de passe
          On attends que les mails soient pris en compte dans la création de l'utilisateur */
        await User.checkResetToken(username, providedToken);
        await User.resetPassword(username, hashPassword(newPassword));
        return res.redirect("/profile");
    }
    catch(e){
        if (e.message.includes("Token invalide")) {
            return res.status(400).json({ message: "Token invalide" });
        }
        return res.status(500).json({message: "Erreur lors de la réinitialisation du mot de passe"});
    }
};

export default {register, login, logout, resetPassword};