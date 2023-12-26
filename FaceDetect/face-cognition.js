'use strict';

var express =  require("express");
var app     =  express();

var server = require('http').createServer(app);
var io = require('socket.io')(server);

var request = require('request');
var fs = require('fs');
var Fdata=[{faceId:'......',
            faceAttributes:{gender:'....',age:0}}];

var exec = require('child_process').exec;
var exec2 = require('child_process').exec;
var hasOwnProperty = Object.prototype.hasOwnProperty;


app.use(express.static('static'));

//-----child_process-----//
exec('mjpg_streamer -i "input_uvc.so -f 20 -d /dev/video0" -o "output_http.so" ', function(error, stdout, stderr) {
  console.log('stdout: ' + stdout);
  console.log('stderr: ' + stderr);
  if (error !== null) {
    console.log('exec error: ' + error);
  }
});
  console.log('camera on!');

app.get('/',function(req,res){
      res.sendFile(__dirname+'/static/face.html');
});

//-----socket on -----//
io.on('connection',function (socket) {
  console.log("Linked");
  });

server.listen(3000,function(){
    console.log("Working on port 3000");
    setInterval(function () {
//-----take snapshot,modify linkit Ip here -----//
      console.log("New readFile...");
      exec2('wget http://172.20.10.3:8080/?action=snapshot -O output.jpg', function(error, stdout, stderr) {
        console.log('stdout: ' + stdout);
        console.log('stderr: ' + stderr);
        if (error !== null) {
          console.log('exec error: ' + error);
        }
      });

//-----read jpg and post to cognitive API,modify api key here-----//
      fs.readFile("./output.jpg", function(err, data) {

      request({
          method: 'POST',
          url: 'https://ccc/face/v1.0/detect?returnFaceId=true&returnFaceAttributes=headPose,glasses,accessories',
          headers: {
              'Content-Type': 'application/json',
              'Ocp-Apim-Subscription-Key': ''
          },
          body:data

      }, function (error, response, body) {
          if (!error && response.statusCode == 200) {
              Fdata =JSON.parse(body);
              console.dir(Fdata, {depth: null, colors: true});
              if (isEmpty(Fdata)) {
                console.log("No face detect!");
                io.emit('message',{'id':'No Face'});
              }
              else {
                console.log('Face Detect');
                io.emit('message',{'id':Fdata[0].faceId});
              }
          }
      });
	
      /*--------emotion API-----------*/
    //   request({
    //       method: 'POST',
    //       url: 'https://api.projectoxford.ai/emotion/v1.0/recognize',
    //       headers: {
    //           'Content-Type': 'application/octet-stream',
    //           'Ocp-Apim-Subscription-Key': 'my-emotion-api-key'
    //       },
    //       body: data
    //   }, function (error, response, body) {
    //       if (!error && response.statusCode == 200) {
    //           var object = JSON.parse(body);
    //           console.dir(object, {depth: null, colors: true});
    //       }
    //   });
      });
    },3000)
});

function isEmpty(obj) {

    // null and undefined are "empty"
    if (obj == null) return true;

    // Assume if it has a length property with a non-zero value
    // that that property is correct.
    if (obj.length > 0)    return false;
    if (obj.length === 0)  return true;

    // Otherwise, does it have any properties of its own?
    // Note that this doesn't handle
    // toString and valueOf enumeration bugs in IE < 9
    for (var key in obj) {
        if (hasOwnProperty.call(obj, key)) return false;
    }

    return true;
}