const puppeteer = require('puppeteer');
const domains = process.argv.slice(2);

(async () => {
  let errorCounter = 0;
  const browser = await puppeteer.launch({ headless: 'new' });

  for (const domain of domains) {
    const page = await browser.newPage();
    const blockedResources = [];

    page.on('requestfailed', request => {
      const reason = request.failure()?.errorText || '';
      if (reason.includes('blocked')) {
        blockedResources.push({ url: request.url(), reason });
      }
    });

    try {
      const url = `https://${domain}`;
      await page.goto(url, { waitUntil: 'networkidle2', timeout: 20000 });
    } catch (e) {
      console.error(`${domain}: ERROR visiting site - ${e.message}`);
      errorCounter++;
      continue;
    }

    if (blockedResources.length > 0) {
      console.warn(`${domain}: Blocked resources detected:`);
      blockedResources.forEach(r =>
        console.log(`  BLOCKED by CSP: ${r.url} (${r.reason})`)
      );
      errorCounter++;
    } else {
      console.log(`${domain}: ✅ No CSP blocks detected.`);
    }

    await page.close();
  }

  await browser.close();
  process.exit(errorCounter);
})();
