import { DataTypes } from 'sequelize';
import {sequelize} from "../db.js";

const Post = sequelize.define('Post', {
    id: {
        type: DataTypes.UUID,
        defaultValue: DataTypes.UUIDV4,
        primaryKey: true,
        unique: true
    },
    title: {
        type: DataTypes.STRING,
        allowNull: false
    },
    content: {
        type: DataTypes.TEXT,
        allowNull: false
    },
    likes: {
        type: DataTypes.INTEGER,
        defaultValue: 0
    }
});

Post.associate = function (models) {
    Post.belongsTo(models.User, { as: "author", foreignKey: "userId", onDelete: "CASCADE" });
    Post.hasMany(models.Comment, { as: "comments", foreignKey: "postId", onDelete: "CASCADE" });
};

export default Post;