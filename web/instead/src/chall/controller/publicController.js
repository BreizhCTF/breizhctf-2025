import User from "../models/user.js";
import Post from "../models/post.js";
import Comment from "../models/comment.js";
import visitUserReport from "../bot.js";

const publicProfilePage = async (req, res) => {
  try {
    const user = await User.getUserWithUsername(req.user.username);
    if (!user) return res.status(404).send("Vous n'êtes pas connecté");
    const userId = req.params.id;
    const Profileuser = await User.findOne({ where: { id: userId } });
    if (!Profileuser) return res.status(404).send("Utilisateur non trouvé");

    const posts = await Post.findAll({
      where: { userId: Profileuser.id },
      order: [["createdAt", "DESC"]]
    });

    const comments = await Comment.findAll({
      where: { userId: Profileuser.id }
    });
    const postCount = posts.length;
    const commentCount = comments.length;

    res.render("publicProfile", { user, Profileuser, posts, postCount, commentCount });
  } catch (e) {
    console.error(e);
    res.status(500).send("Erreur lors du chargement du profil public");
  }
};

const reportUser = async (req, res) => {
  const id = req.params.id;
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i.test(id)) {
    return res.status(400).json({ error: 'L\'ID doit être un UUIDv4.' });
  }
  try {
    visitUserReport(id);
    return res.redirect(`/user/${id}`);
  } 
  catch (e) {
    return res.status(500).json({ error: 'Erreur lors de la visite du profil.' });
  }
};

export default { publicProfilePage, reportUser };