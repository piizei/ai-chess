'use strict';

var mongoose = require('mongoose');
mongoose.Promise = global.Promise;

var failedConnections = 0;
var autoReconnect = true;

//var db_URI = 'mongodb://localhost/ElmChessDb'
console.log('MONGO_CONNECTION: ' + process.env.MONGO_CONNECTION);
const db_URI = process.env.MONGO_CONNECTION.replace('==', '%3D%3D').replace("&replicaSet=globaldb","")
connect();

function connect() {
    mongoose.connect(db_URI);
}

/** Mongoose is connected **/
mongoose.connection.on('connected', function() {
    console.log('Mongoose database is connected on: ' + db_URI);

});

/** Mongoose is disconnected--> Tries to reconnect three times, then gives up **/
mongoose.connection.on('disconnected', function() {
    console.log('Mongoose is disconnected.');
    if(failedConnections < 3) {
        console.log('Trying to reconnect.. ');
        connect();
        failedConnections++;
    }
});

/** Mongoose error **/
mongoose.connection.on('error', function(err) {
    console.log('Mongoose encountered an error: ' + err);
});

/** Application closing **/
process.on('SIGINT', function () {
    console.log('Goodbye from mongoose! :)');
    process.exit(0);
});

/** Handles SIGUSR2 when nodemon restart **/
process.once('SIGUSR2', function() {
    console.log('Restarting mongoose.');
    process.kill(process.pid, 'SIGUSR2');

});


/** Handles SIGUTERM after Heroku restar **/
process.on('SIGTERM', function() {
    console.log('Goodbye from Heroku! :)');
    process.exit(0);

});
