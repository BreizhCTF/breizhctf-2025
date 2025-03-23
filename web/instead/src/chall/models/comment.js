import { DataTypes } from 'sequelize';
import {sequelize} from "../db.js";

const Comment = sequelize.define('Comment', {
    id: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true
    },
    content: {
        type: DataTypes.TEXT,
        allowNull: false
    },
    postId: {
        type: DataTypes.UUID,
        allowNull: false,
        references: {
            model: 'Posts',
            key: 'id'
        },
        onDelete: 'CASCADE'
    },
    userId: {
        type: DataTypes.INTEGER,
        allowNull: false,
        references: {
            model: 'Users',
            key: 'id'
        },
        onDelete: 'CASCADE'
    }
});

Comment.associate = (models) => {
    Comment.belongsTo(models.User, { as: "user", foreignKey: "userId", onDelete: "CASCADE" });
    Comment.belongsTo(models.Post, { as: "post", foreignKey: "postId", onDelete: "CASCADE" });
};

export default Comment;