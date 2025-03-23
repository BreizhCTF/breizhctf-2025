import path from "path";
import express from "express";
import cookieParser from "cookie-parser";
import morgan from "morgan";
import { fileURLToPath } from "url";
import routes from "./routes.js";
import db from "./db.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

app.use(morgan("tiny"));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use("/static", express.static(path.join(__dirname, "static")));
app.use('/bootstrap-icons', express.static(path.join(__dirname, 'node_modules/bootstrap-icons')));
app.use("/pdf.mjs", express.static(path.join(__dirname, "node_modules/pdfjs-dist/legacy/build/pdf.mjs")));
app.use("/pdf.worker.mjs", express.static(path.join(__dirname, "node_modules/pdfjs-dist/legacy/build/pdf.worker.mjs")));
app.use(routes);

(async () => {
  try {
    await db.connect();
    await db.migrate();
    app.listen(5000, "0.0.0.0", () =>
      console.log("Serveur lancé sur http://localhost:5000")
    );
  } catch (e) {
    console.error("Erreur lors du démarrage de l'application :", e);
    process.exit(1);
  }
})();
