
import puppeteer from 'puppeteer'
//  = require('puppeteer');
import fs from 'fs' 
// require('fs');
import pLimit from 'p-limit';

// const pLimit = require('p-limit');

async function getCode() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  const scrollNestedDiv = async () => {
    const nestedDivSelector = '.relative.h-full.overflow-auto.transition-opacity';
    await page.goto('https://leetcode.com/problems/maximum-profit-in-job-scheduling/solutions/');
    for (let j = 0; j < 10; j++) {
      console.log("Scrolling");
      await page.waitForSelector('.no-underline.truncate.w-full');
      await page.evaluate((nestedDivSelector) => {
        const nestedDiv = document.querySelector(nestedDivSelector);
        nestedDiv.scrollTop += 1000;
      }, nestedDivSelector);
      await page.waitForTimeout(2000);
    }
  };

  
  await scrollNestedDiv();

  const links = await page.evaluate(() =>
    Array.from(document.querySelectorAll('.no-underline.truncate.w-full'), (e) => e.href)
  );
  
  const limit = pLimit(5); 

  
  const fetchSolutionsPromises = links.map((link, index) =>
    limit(async () => {
      const solutionPage = await browser.newPage();
      try {
        console.log(`Fetching code from link ${index + 1}/${links.length}: ${link}`);
        await solutionPage.goto(link, { waitUntil: 'domcontentloaded' });

        await solutionPage.waitForSelector('#code');

        const code = await solutionPage.evaluate(() => {
          const codeElement = document.querySelector('#code');
          return codeElement ? codeElement.nextElementSibling.getElementsByTagName('code')[0].innerText : null;
        });

        //Scrape language of solution
        const lang = await solutionPage.evaluate(()=> {
          const codeElement = document.querySelector('#code');
          return codeElement ? codeElement.nextElementSibling.getElementsByTagName('code')[0].className.split('-')[1] : null;
        })

        return code ? {language: lang, data :[{url: link, code: code}] } : null;
      } catch (err) {
        console.error(`Error fetching code from ${link}: ${err.message}`);
        return null;
      } finally {
        await solutionPage.close();
      }
    })
  );

  const solutions = await Promise.all(fetchSolutionsPromises);
  const filteredSolutions = solutions.filter((solution) => solution !== null);

  let format =
    Object.values(filteredSolutions.reduce((a, { language, data }) => {
      if (!a[language]) a[language] = { language, data: [] };
      a[language].data.push(data[0]);
      return a;
    }, {}))

  format = JSON.stringify(format,null,2)

  fs.writeFileSync('solutions.json', format);

  await browser.close();
}

getCode();
