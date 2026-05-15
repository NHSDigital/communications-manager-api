#!/usr/bin/env node
'use strict';

const fs = require('fs');
const Handlebars = require('handlebars');

const [,, dataFile, templateFile] = process.argv;

if (!dataFile || !templateFile) {
  console.error('Usage: node scripts/render_hbs.js <data.json> <template.hbs>');
  process.exit(1);
}

const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
const templateSource = fs.readFileSync(templateFile, 'utf8');
const template = Handlebars.compile(templateSource);

// @generated is a data-frame variable used in the nunit template
const output = template(data, { data: { generated: new Date().toISOString() } });
process.stdout.write(output);