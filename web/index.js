const options = {
  encoding: 'utf8'
};
require('dotenv').config(options);

const apiUrl = `http://${process.env.API_SERVER}:${process.env.API_PORT}/api/v1.0/status`;
const rb = document.querySelectorAll('input[type="radio"]');

Array.from(rb).forEach((b) => {
  b.addEventListener('click', e => {
    window.navigator.vibrate(200);

    const payload = {
      userId: parseInt(document.getElementById('userId').value, 10),
      metricId: parseInt(e.target.value.substring(0, 1), 10),
      metricCount: parseInt(document.getElementById('metricCount').value, 10),
      status: e.target.value.substring(1),
    };

    fetch(apiUrl, {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {}) // JSON-string from `response.json()` call
    .catch(error => console.error(error));
  });
})