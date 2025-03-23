const express = require("express");
const puppeteer = require("puppeteer");

const app = express();
const PORT = process.env.PORT || 8000; 

app.use(express.json());

app.post("/report", async (req, res) => {
    var { url } = req.body;

    if (!url) {
        return res.status(400).json({ error: "Missing 'url' parameter" });
    }

    res.json({ message: "OK" });

    if(!process.env.DESIGNER_ENDPOINT.endsWith("/")){
        process.env.DESIGNER_ENDPOINT += "/";
    }

    if(url.startsWith("/")) {
        url = url.substring(1);
    }

    full_url = process.env.DESIGNER_ENDPOINT + url;
    visitURL(full_url);
});

async function visitURL(url) {
    try {
        console.log(`Launching Puppeteer to visit: ${url}`);

        const browser = await puppeteer.launch({
            // executablePath: process.env.CHROMIUM_PATH || "/usr/bin/chromium",
            headless: true,
            args: [
                "--no-sandbox", 
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--enable-logging",
            ]
        });

        console.log("New page");
        const page = await browser.newPage();

        if (process.env.FLAG) {
            await page.setUserAgent(process.env.FLAG);
        }

        await page.setViewport({ width: 1366, height: 768 });

        console.log("Opening URL");
        await page.goto(url, {waitUntil: 'domcontentloaded'});

        await new Promise(resolve => setTimeout(resolve, 3000));

        await page.close();

        console.log("Closing browser");
        await browser.close();
    } catch (error) {
        console.error(`Error visiting ${url}:`, error);
    }
    console.log("End of session");
}

app.listen(PORT, () => {
    console.log(`Admin running on port ${PORT}`);
});