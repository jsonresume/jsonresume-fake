const express = require("express");
const _ = require("lodash");
const fs = require("fs");
const axios = require("axios");
const glob = require("glob");
const app = express();
const port = process.env.PORT || 3000;

const themes = [
  "jsonresume-theme-class",
  "jsonresume-theme-classy",
  "jsonresume-theme-eloquent",
  "jsonresume-theme-flat",
  "jsonresume-theme-keloran",
  "jsonresume-theme-kendall",
  "jsonresume-theme-kwan",
  "jsonresume-theme-mantra",
  "jsonresume-theme-short",
  "jsonresume-theme-spartan",
  "jsonresume-theme-stackoverflow",
];

const INDEX_HTML = fs.readFileSync("./index.html", "utf8");

const resumeFiles = glob.sync("./resumes/*.json");
const sampleResumes = [];

_.each(resumeFiles, (resumePath) => {
  sampleResumes.push(JSON.parse(fs.readFileSync(resumePath)));
});

app.get("/", (req, res) => {
  res.send(INDEX_HTML);
});

app.get("/resume", (req, res) => {
  const resumeFiles = glob.sync("./resumes/*.json");
  const sampleResumes = [];

  _.each(resumeFiles, (resumePath) => {
    sampleResumes.push(JSON.parse(fs.readFileSync(resumePath)));
  });
  const randomResume = _.sample(sampleResumes);
  const randomTheme = _.sample(themes).replace("jsonresume-theme-", "");
  const themeRendererUrl = `https://registry.jsonresume.org/theme/${randomTheme}`;
  console.log("Loading theme", themeRendererUrl);
  axios
    .post(themeRendererUrl, {
      resume: randomResume,
    })
    .then(function (response) {
      let content = response.data;
      res.send(content);
    })
    .catch(function (error) {
      res.send({ error });
    });
});

app.listen(port, () => {
  console.log(`Listening at http://localhost:${port}`);
});
