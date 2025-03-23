import User from '../models/user.js';
import Post from '../models/post.js';
import Comment from '../models/comment.js';
import { SafeMerge } from '../utils.js';
import { exec } from 'child_process';

let adminConfig = {
    stats: {
        totalUsers: 0,
        totalPosts: 0,
        totalComments: 0,
        lastRegistration: null,
    },
    showOption: {
        display: true,
    },
    debug: false,
};

let service = {
    /* On suit les bonnes pratiques et on commentes le debug juste au cas ou
       debugHealthcheck: "echo 'Service en cours de maintenance'" */
};

const healthcheck = "curl -s http://localhost:5000/health";

const updateStats = async () => {
    try {
        const totalUsers = await User.count();
        const totalPosts = await Post.count();
        const totalComments = await Comment.count();
        const lastRegistration = (await User.findOne({ order: [['createdAt', 'DESC']] })).createdAt;

        adminConfig.stats = {
            totalUsers: totalUsers,
            totalPosts: totalPosts,
            totalComments: totalComments,
            lastRegistration: lastRegistration ? lastRegistration : "N/A",
        };
    }
    catch(e) {
        console.error("Erreur dans updateStats:", e);
    }
};

const getHealthcheckCommand = (req, res) => {
    if (!adminConfig.showOption.display) {
        return "echo Service désactivé";
    }
    if(adminConfig.debug) {
        if (service.debugHealthcheck && service.debugHealthcheck !== "") {
            return service.debugHealthcheck;
        }
    }
    return healthcheck;
};

const updateConfig = async (req, res) => {
    try {
        adminConfig = SafeMerge( adminConfig, req.body);
        await updateStats();
        res.json({ message: "Configuration mise à jour", config: adminConfig });
    }
    catch(e){
        res.status(500).json({ message: "Erreur lors de la mise à jour de la configuration", error: e.message });
    }
};

const adminDashboard = async (req, res) => {
    try {
        const user = await User.getUserWithUsername(req.user.username);
        await updateStats();
        const services = getHealthcheckCommand();
        exec(services, { timeout: 5000 }, (error, stdout, stderr) => {
            if (error) {
                return res.status(500).send("Erreur lors du chargement du dashboard: " + error.message);
            }
            const result = stdout.trim();
            return res.render('adminDashboard', { user: user,stats: adminConfig.stats, healthcheck: result });
            });
    }
    catch (e) {
        console.error("Erreur dans adminDashboard:", e);
        return res.status(500).send("Erreur lors du chargement du dashboard: " + e.message);
    }
};

export default { adminDashboard, updateConfig };