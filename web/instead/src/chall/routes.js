import express from "express";
import authMiddleware from "./middleware/authMiddleware.js";
import adminMiddleware from "./middleware/adminMiddleware.js";
import fileValidatorMiddleware from "./middleware/fileValidatorMiddleware.js";
import multerConfig from "./middleware/multerConfig.js";
import authController from "./controller/authController.js";
import postController from "./controller/postController.js";
import profileController from "./controller/profileController.js";
import publicController from "./controller/publicController.js";
import adminController from "./controller/adminController.js";
import { verifyJWT } from "./utils.js";

const router = express.Router();

const authentPanel = (req, res) => {
  const token = req.cookies.jwt;
  if (token) {
    const user = verifyJWT(token);
    if (user) {
      return res.redirect("/home");
    }
  }
  return res.render("auth");
};

router.get("/", authentPanel);
router.get("/logout", authMiddleware, authController.logout);
router.post("/register", authController.register);
router.post("/login", authController.login);
router.get("/home", authMiddleware, postController.homePage);
router.get("/search", authMiddleware, postController.searchPosts);
router.post("/post/new", authMiddleware, postController.newPost);
router.post("/comment/new/:id", authMiddleware, postController.newComment);
router.post("/post/like/:id", authMiddleware, postController.addLike);
router.get("/profile", authMiddleware, profileController.profilePage);
router.post("/profile/reset-password", authMiddleware, authController.resetPassword);
router.post(
  "/cv/upload",
  authMiddleware,
  multerConfig.single("cv"),
  fileValidatorMiddleware,
  profileController.uploadCV
);
router.get("/cv/:id", authMiddleware, profileController.previewCV);
router.post("/cv/:id/delete", authMiddleware, profileController.deleteCV);
router.post("/profile/changePfP", authMiddleware, profileController.changeProfilePicture);
router.get("/user/:id",authMiddleware, publicController.publicProfilePage);
router.get("/user/report/:id",authMiddleware, publicController.reportUser);
router.get("/admin/dashboard",authMiddleware, adminMiddleware, adminController.adminDashboard);
router.post("/admin/dashboard/config",authMiddleware, adminMiddleware, adminController.updateConfig);
router.get('/health', (req, res) => {
  res.send("OK");
});

export default router;