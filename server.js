var express = require('express');
var app = express();
const { spawn } = require('child_process');

// routes
app.get('/', (req, res) => { res.send('Corona Live updates API') })

// get update stats
app.get("/updates", (req, res) => {
    // Use child_process.spawn method from
    // child_process module and assign it to variable spawn
    const process = spawn("python", ["main.py", "updates"]);
    // Takes stdout data from script which executed
    // with arguments and send this data to res object
    process.stdout.on("data", data => {
        res.json(JSON.parse(data.toString()));
    });
    process.stderr.on("data", data => {
        res.status(400).send("There's been an error, I apologise");
    });
})





app.listen(3000)