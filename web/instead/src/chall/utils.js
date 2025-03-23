import jwt from "jsonwebtoken";
import crypto from "crypto";

const KEY = crypto.randomBytes(64).toString("hex");

export const makeJWT = (user) => {
  return jwt.sign({ username: user.username, role: user.role }, KEY, {
    expiresIn: "2h",
  });
};

export const verifyJWT = (token) => {
  return jwt.verify(token, KEY, (err, decoded) => {
    if (err) return false;
    return decoded;
  });
};

export const hashPassword = (password) => {
  return crypto.createHash("sha256").update(password).digest("hex");
};

export const availableProfiles = [
  "/static/img/pfp1.png",
  "/static/img/pfp2.png",
  "/static/img/pfp3.png",
  "/static/img/pfp4.png"
];

export const SafeMerge = (target, source) => {
  Object.keys(source).forEach(Key => {
    if (["__proto__", "prototype", "constructor"].includes(Key)) return;
    const escKey = Key.normalize("NFKC");
    const sourceValue = source[Key];
    if (typeof target[escKey] !== "undefined" && typeof sourceValue === "object" && sourceValue !== null) {
      target[escKey] = SafeMerge(target[escKey], sourceValue);
    } else {
      target[escKey] = sourceValue;
    }
  });
  return target;
}