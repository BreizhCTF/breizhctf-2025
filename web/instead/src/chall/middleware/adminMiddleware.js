const adminMiddleware = (req, res, next) => {
    if (!req.user) {
      if (req.method === "GET") {
        return res.redirect("/");
      }
      return res.status(401).json({ message: "Vous n'êtes pas authentifié" });
    }
    if (req.user.role === "administrator") {
      return next();
    }
    if (req.method === "GET") {
      return res.redirect("/home");
    }
    return res.status(403).json({ message: "Vous n'avez pas les droits pour effectuer cette action" });
};

export default adminMiddleware;