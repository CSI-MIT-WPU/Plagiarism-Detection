import puppeteer from 'puppeteer'
import fs from 'fs' 
import pLimit from 'p-limit';


async function getCode(urlLink) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
  
    const scrollToEnd = async () => {
      const nestedDivSelector = '.relative.h-full.overflow-auto.transition-opacity';
      await page.goto(urlLink);

      let previousHeight = 0;
    
      do {
        console.log("Scrolling");
        await page.waitForSelector('.no-underline.truncate.w-full');
        // Scroll to the bottom of the page
        const currentHeight = await page.evaluate(async (nestedDivSelector) => {
          const nestedDiv = document.querySelector(nestedDivSelector);
          nestedDiv.scrollTop = nestedDiv.scrollHeight;
          return nestedDiv.scrollHeight;
        },nestedDivSelector);
        
        await page.waitForTimeout(2500);
        // Check if the page height has changed
        let heightChanged = currentHeight !== previousHeight;
        previousHeight = currentHeight;
        if(!heightChanged){
          break;
        }
      
      } while (true);
    }

  
  await scrollToEnd();

  const links = await page.evaluate(() =>
    Array.from(document.querySelectorAll('.no-underline.truncate.w-full'), (e) => e.href)
  );
  
  console.log(links)
  
  const limit = pLimit(10); 

  
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

  await browser.close();
  return format
}

async function generateSolution(answer,specificQID,finalSolution){
  
  //create solution.json file
  finalSolution.push({"qid":specificQID, "solution":answer})
  finalSolution = JSON.stringify(finalSolution,null,2)

  fs.writeFileSync('solutions.json', finalSolution);
}

async function getLink(qidArray) {
    const filePath = './Question Info/questions.json';
      // Read the JSON file
      fs.readFile(filePath, 'utf8',function (err, data) {
          if (err){
              throw new Error(`Error reading the file`);
          }
  
          try{
              // Parse the JSON data
              const jsonData = JSON.parse(data);
  
              let finalSolution=[]
              try{
                qidArray.forEach((specificQID)=>{

                  // Find the object with the specific QID
                  const specificObject = jsonData.find(item => item.QID === specificQID);
      
                  if (specificObject) {
                    const temp_link = specificObject.solutionUrl;  //Getting desired output
  
                    let a = new Promise((resolve)=>{                
                      resolve(getCode(temp_link))                
                    }).then((answer)=>{
                        generateSolution(answer,specificQID,finalSolution)
                    })
                  }
                })
              }catch(err){
                throw new Error(`QID ${specificQID} not found in the JSON data.`);
              }            
          }catch(error){
              throw new Error(`Could not parse JSON file`);
          }
      });   
  }
  
  
  getLink(['1','2']);
