import path from "path";
import fs from"fs";
import CV from"../models/cv.js";
import User from"../models/user.js";
import { availableProfiles } from"../utils.js";

const profilePage = async (req, res) => {
  try {
    const user = await User.getUserWithUsername(req.user.username);
    if (!user) return res.status(404).send("Utilisateur non trouvé");
    const cv = await CV.findOne({ where: { userId: user.id } });
    res.render("profile", { user, cv, availableProfiles });
  } catch (e) {
    res.status(500).send("Erreur lors du chargement du profil");
  }
};

const uploadCV = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).send("Aucun fichier uploadé.");
    }
    const user = await User.getUserWithUsername(req.user.username);
    if (!user) return res.status(404).send("Utilisateur non trouvé");

    let cv = await CV.findOne({ where: { userId: user.id } });
    const randomFilePath = req.file.path;

    if (cv) {
      if (fs.existsSync(cv.path)) {
        fs.unlinkSync(cv.path);
      }
      cv.path = randomFilePath;
      await cv.save();
    } else {
      cv = await CV.create({
        userId: user.id,
        path: randomFilePath,
      });
    }
    res.redirect("/profile");
  } catch (err) {
    console.error(err);
    res.status(500).send("Erreur lors de l'upload du CV.");
  }
};  

const previewCV = async (req, res) => {
    try {
      const cv = await CV.findOne({ where: { id: req.params.id } });
      if (!cv) return res.status(404).send("CV non trouvé");
      const pdfPath = path.resolve(cv.path);
    if (!fs.existsSync(pdfPath))
      return res.status(404).send("Fichier PDF introuvable");

    const fileBuffer = fs.readFileSync(pdfPath);
    const base64Data = fileBuffer.toString('base64');
    const dataURL = `data:application/pdf;base64,${base64Data}`;
    
    res.render("preview", { dataURL });
  } 
  catch (e) {
    console.error(e);
    res.status(500).send("Erreur lors de la génération de la preview du CV.");
  }
};

const deleteCV = async (req, res) => {
  try {
    const cv = await CV.findOne({ where: { id: req.params.id } });
    if (!cv) return res.status(404).send("CV non trouvé");
    if (fs.existsSync(cv.path)) {
      fs.unlinkSync(cv.path);
    }
    await cv.destroy();
    res.redirect("/profile");
  } catch (e) {
    console.error(e);
    res.status(500).send("Erreur lors de la suppression du CV.");
  }
};

const changeProfilePicture = async (req, res) => {
  try {
    const newPicture = req.body.profilePicture;
    if (!availableProfiles.includes(newPicture)) {
      return res.status(400).send("Image de profil non autorisée");
    }
    const user = await User.getUserWithUsername(req.user.username);
    if (!user) return res.status(404).send("Utilisateur non trouvé");
    user.profilePicture = newPicture;
    await user.save();
    res.redirect("/profile");
  } catch (e) {
    console.error(e);
    res.status(500).send("Erreur lors de la mise à jour de l'image de profil");
  }
};

export default { profilePage, uploadCV, previewCV, deleteCV, changeProfilePicture };
  