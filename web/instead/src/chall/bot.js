import puppeteer from "puppeteer";
import User from "./models/user.js";
import { makeJWT } from "./utils.js";
import { exec } from "child_process";
import morgan from "morgan";

const visitUserReport = async (userId) => {
  const browser = await puppeteer.launch({
    headless: true,
    ignoreHTTPSErrors: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--ignore-certificate-errors"]
  });


  const page = await browser.newPage();

  page
    .on("console", message =>
      console.log(`[BOT] ${message.type().substr(0, 3).toUpperCase()} ${message.text()}`)
    )
    .on("pageerror", ({ message }) =>
      console.error(`[BOT] ${message}`)
    )
    .on("response", response =>
      console.log(`[BOT] ${response.status()} ${response.url().substring(0, 1000)}`)
    )
    .on("requestfailed", request =>
      console.log(`[BOT] ${request.failure().errorText} ${request.url()}`)
    );

  await browser.setCookie({
    name: "jwt",
    value: makeJWT(await User.getUserWithUsername("admin")),
    domain: "127.0.0.1",
    httpOnly: true,
    secure: false,
    sameSite: "Strict"
  })

  const url = `http://127.0.0.1:5000/user/${userId}`;
  try {
    await page.goto(url, {
      waitUntil: "networkidle0",
    });
    console.log(`Visité : ${url}`);
    const content = await page.content();
    await new Promise(resolve => setTimeout(() => resolve(), 10000));
  }
  catch (e) {
    console.error("Erreur lors de l'accès à la page :", e);
  }
  finally {
    await browser.close();
  }
};

export default visitUserReport;