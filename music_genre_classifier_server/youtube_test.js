const {google} = require('googleapis');
var youtube = google.youtube({
    version: 'v3',
    auth: "AIzaSyAH-RkBb_JeY_9NOv-7xYFPp7W-9STbo7Q"
});

youtube.search.list({
    part: 'snippet',
    q: 'resident evil village'
  }, function (err, data) {
    if (err) {
      console.error('Error: ' + err);
    }
    if (data) {
      console.log(data)
    }
  });
