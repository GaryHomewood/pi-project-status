const Sqrl = require("squirrelly");
const fs = require('fs')
const projectData = require('./project-data.json')

console.log('Generating the site...');

// create index page
fs.readFile('templates/index.html', "utf8", (err, indexTemplate) => {
  if (err) throw err;
  const indexPage = Sqrl.Render(indexTemplate, {
    team: projectData['team']
  })
  fs.writeFileSync('index.html', indexPage);
})

// create user pages
fs.readFile('templates/user.html', "utf8", (err, userTemplate) => {
  if (err) throw err;
  Array.from(projectData['team']).forEach((user, idx) => {
    const userPage = Sqrl.Render(userTemplate, {
      userId: idx,
      userName: user['name'],
      metricCount: projectData['metrics'].length,
      metrics: projectData['metrics'],
    })
    const userPageName = `${user['name'].toLowerCase()}.html`.replace(' ', '-');
    fs.writeFileSync(userPageName, userPage)
  })
})
