const Sqrl = require("squirrelly");
const fs = require('fs')
const projectData = require('./project-data.json')

console.log('Generating the site...');

// create index page
fs.readFile('templates/index.html', "utf8", (err, indexTemplate) => {
  if (err) throw err;
  const indexPage = Sqrl.Render(indexTemplate, {
    project: projectData['project'],
    pixelCount: projectData['team'].length * projectData['metrics'].length,
    team: projectData['team']
  })
  fs.writeFileSync('index.html', indexPage);
})

// create team member pages
fs.readFile('templates/team-member.html', "utf8", (err, teamMemberTemplate) => {
  if (err) throw err;
  Array.from(projectData['team']).forEach((user, idx) => {
    const teamMemberPage = Sqrl.Render(teamMemberTemplate, {
      project: projectData['project'],
      userId: idx,
      userName: user['name'],
      metricCount: projectData['metrics'].length,
      metrics: projectData['metrics'],
    })
    const teamMemberPageName = `${user['name'].toLowerCase()}.html`.replace(' ', '-');
    fs.writeFileSync(teamMemberPageName, teamMemberPage)
  })
})

// create label page
fs.readFile('templates/label.html', "utf8", (err, labelTemplate) => {
  if (err) throw err;
  const labelPage = Sqrl.Render(labelTemplate, {
    project: projectData['project'],
    teamSize: projectData['team'].length,
    metrics: projectData['metrics'],
  })
  fs.writeFileSync('label.html', labelPage)
})