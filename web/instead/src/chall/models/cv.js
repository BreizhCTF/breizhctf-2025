import { DataTypes } from 'sequelize';
import {sequelize} from "../db.js";

const CV = sequelize.define('CV', {
    id: {
        type: DataTypes.UUID,
        primaryKey: true,
        defaultValue: DataTypes.UUIDV4,
        unique: true
    },
    path: {
        type: DataTypes.STRING,
        allowNull: false
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

CV.associate = (models) => {
    CV.belongsTo(models.User, { as: "user", foreignKey: "userId", onDelete: "CASCADE" });
};

export default CV;