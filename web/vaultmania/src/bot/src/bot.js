const puppeteer = require("puppeteer");

async function visit_vault() {
    let url = process.env.VAULTMANIA_URL || "http://vaultmania:8000/vaults";
    let pin = process.env.VAULT_PIN || "1234";
    try {
        console.log(`Launching Puppeteer to visit: ${url}, with PIN: ${pin}`);

        const browser = await puppeteer.launch({
            //executablePath: process.env.CHROMIUM_PATH || "/usr/bin/chromium",
            headless: true,
            args: [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--enable-logging",
            ]
        });

        const page = await browser.newPage();
        await page.setViewport({ width: 1920, height: 1080 });

        await page.goto(url, { waitUntil: 'domcontentloaded' });

        await page.waitForSelector("#openUnlockModal");
        await page.click("#openUnlockModal");

        await page.waitForSelector("#unlockVaultModal", { visible: true });

        await page.waitForSelector("#vaultId");
        await page.select("#vaultId", await page.evaluate(() => {
            let select = document.querySelector("#vaultId");
            return select.options.length > 1 ? select.options[1].value : null;
        }));

        for (let digit of pin) {
            //console.log(`Clicking pin ${digit}`);
            await page.click(`#pin${digit}`);
            await new Promise(resolve => setTimeout(resolve, 1000));
        }

        await page.click("#unlockVaultForm button[type=submit]");

        await new Promise(resolve => setTimeout(resolve, 1000));

        //const content = await page.content();
        //console.log(content);

        await browser.close();
    } catch (error) {
        console.error(`Error visiting ${url}:`, error);
    }
}

function launch_bot() {
    visit_vault();
    setInterval(() => {
        visit_vault();
    }, 1000 * 60 * 2);
}

console.log("Bot is starting, waiting 10 seconds before launching...");
setTimeout(() => {
    console.log("Launching bot.");
    launch_bot();
}, 10000);