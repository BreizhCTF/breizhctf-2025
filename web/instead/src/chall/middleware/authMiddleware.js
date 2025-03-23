import { verifyJWT } from "../utils.js";

const authMiddleware = (req, res, next) => {
  const authentCookie = req.cookies.jwt;

  if (!authentCookie) {
    if (req.method === "GET") {
      return res.redirect("/");
    }
    return res.status(401).json({ message: "Token d'authentification manquant" });
  }

  const user = verifyJWT(authentCookie);
  if (user != false && user != undefined) {
    req.user = user;
    return next();
  }
  
  if (req.method === "GET") {
    return res.redirect("/");
  }
  return res.status(401).json({ message: "Erreur, vous n'êtes pas authentifié" });
};
  
export default authMiddleware;