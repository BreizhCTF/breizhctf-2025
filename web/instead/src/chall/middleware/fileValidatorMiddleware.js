import fs from 'fs';

const pdfFileValidator = (req, res, next) => {
  const file = req.file;

  if (!file) {
    return res.status(400).send("Aucun fichier uploadé.");
  }

  const originalName = file.originalname;
  const fileExtension = originalName.slice(
    ((originalName.lastIndexOf('.') - 1) >>> 0) + 2
  ).toLowerCase();

  if (fileExtension !== 'pdf') {
    if (fs.existsSync(file.path)) {
      fs.unlinkSync(file.path);
    }
    return res.status(400).send("Extension invalide, seul les fichiers PDF sont autorisés.");
  }

  if (file.mimetype !== 'application/pdf') {
    if (fs.existsSync(file.path)) {
      fs.unlinkSync(file.path);
    }
    return res.status(400).send("Mimetype invalide, seul les fichiers PDF sont autorisés.");
  }

  const allowedSizeMB = 5;
  if (file.size > allowedSizeMB * 1024 * 1024) {
    if (fs.existsSync(file.path)) {
      fs.unlinkSync(file.path);
    }
    return res.status(400).send("Fichier trop volumineux.");
  }

  return next();
};

export default pdfFileValidator;