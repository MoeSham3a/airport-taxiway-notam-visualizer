const fs = require('fs');
const path = require('path');

const htmlFile = 'index.html';
const content = fs.readFileSync(htmlFile, 'utf8');

// 1. Extract base64 image
const imgMatch = content.match(/window\.CHART_IMAGES\s*=\s*\{\s*OMDB:\s*'([^']+)'\s*\}/);
if (imgMatch) {
  let b64Data = imgMatch[1];
  if (b64Data.includes(',')) {
    b64Data = b64Data.split(',')[1];
  }
  const imgBuffer = Buffer.from(b64Data, 'base64');
  fs.mkdirSync('airports/OMDB', { recursive: true });
  fs.writeFileSync('airports/OMDB/chart.jpg', imgBuffer);
  console.log("Chart extracted.");
}

// 2. Extract AIRPORTS data
const twyMatch = content.match(/window\.AIRPORTS\s*=\s*(\{[\s\S]+?\});\s*(?=<)/);
if (twyMatch) {
  let objCode = twyMatch[1];
  // evaluate the object code
  let airportsObj;
  try {
    eval('airportsObj = ' + objCode + ';');
    fs.mkdirSync('airports/OMDB', { recursive: true });
    fs.writeFileSync('airports/OMDB/taxiways.json', JSON.stringify(airportsObj.OMDB.taxiways, null, 2));
    console.log("Taxiways extracted.");
  } catch(e) {
    console.error("Eval error", e);
  }
}

// 3. Create registry.json
const registry = {
  "OMDB": {
    "name": "Dubai International",
    "iata": "DXB",
    "badge": "AE · UAE · IATA: DXB",
    "chart": "airports/OMDB/chart.jpg",
    "taxiways": "airports/OMDB/taxiways.json"
  }
};
fs.writeFileSync('airports/registry.json', JSON.stringify(registry, null, 2));
console.log("Registry created.");
