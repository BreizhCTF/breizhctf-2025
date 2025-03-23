import Post from"../models/post.js";
import User from"../models/user.js";
import Comment from"../models/comment.js";
import { Op } from "sequelize";

const homePage = async (req, res) => {
    try {
        const user = await User.getUserWithUsername(req.user.username);
        const posts = await Post.findAll({
            include: [
                { model: User, as: 'author', attributes: ['username', 'profilePicture', 'id'] },
                {
                    model: Comment,
                    as: "comments",
                    include: [{ model: User, as: "user", attributes: ['username','profilePicture', 'id'] }]
                }
            ],
            order: [["createdAt", "DESC"]]
        });
        return res.render("home", { posts, user: user});
    } catch (e) {
        return res.status(500).send("Erreur interne");
    }
}

const searchPosts = async (req, res) => {
  const query = req.query.query || "";
  try {
    const user = await User.getUserWithUsername(req.user.username);
    const posts = await Post.findAll({
      where: {
        [Op.or]: [
          { title: { [Op.like]: `%${query}%` } },
          { content: { [Op.like]: `%${query}%` } }
        ]
      },
      include: [
        { model: User, as: 'author', attributes: ['username', 'profilePicture'] },
        {
          model: Comment,
          as: "comments",
          include: [{ model: User, as: "user", attributes: ["username"] }]
        }
      ],
      order: [["createdAt", "DESC"]]
    });
    return res.render("home", { posts, user: user });
  } catch (e) {
    console.error(e);
    return res.status(500).send("Erreur lors de la recherche");
  }
};

const newPost = async (req, res) => {
    try {
      const title = req.body.title;
      const content = req.body.content;
      const user = await User.getUserWithUsername(req.user.username);
      if (!user) return res.status(404).send("Utilisateur non trouvé");
      
      const post = await Post.create({
        title,
        content,
        userId: user.id
      });
      res.redirect('/home');
    } catch (e) {
      res.status(500).json({ message: "Erreur lors de la création du post" });
    }
  };

  const newComment = async (req, res) => {
    try {
      const content = req.body.comment;
      const postId = req.params.id;
      const user = await User.getUserWithUsername(req.user.username);
      if (!user) return res.status(404).send("Utilisateur non trouvé");
      
      const comment = await Comment.create({
        content,
        postId,
        userId: user.id
      });
      res.redirect('/home');
    } catch (e) {
      console.error(e);
      res.status(500).json({ message: "Erreur lors de l'ajout du commentaire" });
    }
  };
  
  const addLike = async (req, res) => {
    try {
      const postId = req.params.id;
      const post = await Post.findOne({ where: { id: postId } });
      if (!post) return res.status(404).json({ message: "Post non trouvé" });
      
      post.likes = post.likes + 1;
      await post.save({ fields: ['likes', 'updatedAt'] });
      res.redirect('/home');
    } catch (e) {
      console.error(e);
      res.status(500).json({ message: "Erreur lors de l'ajout du like" });
    }
  };

export default {homePage,searchPosts,newPost,newComment,addLike};