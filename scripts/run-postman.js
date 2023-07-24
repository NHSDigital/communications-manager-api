const
    newman = require('newman'),
    fs = require('fs');

let pk = null;
if (process.env.PRIVATE_KEY.indexOf('-BEGIN PRIVATE KEY-') !== -1) {
    pk = process.env.PRIVATE_KEY;
} else if (process.env.PRIVATE_KEY) {
    pk = fs.readFileSync(process.env.PRIVATE_KEY).toString('utf8');
}

const environment = process.env.ENVIRONMENT || 'Development';

newman.run({
    collection: require('../postman/CommunicationsManager.postman_collection.json'),
    environment: require(`../postman/${environment}.postman_environment.json`),
    envVar : [{
        "key" : "api_key",
        "value" : process.env.API_KEY,
    }, {
        "key" : "private_key",
        "value" : pk,
    }],
    reporters: 'cli',
    color: 'off'
}, function (err) {
    if (err) {
        console.log(err);
    }
    console.log('collection run complete!');
});