var mysql = require('mysql');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.set('view engine', 'ejs');
app.use(express.static('./public'))
app.use(bodyParser.urlencoded({ extended: true })); 

var connection = mysql.createConnection({
  	host: "localhost",
	user: "root",
	password: "Harshit77",
	database: "nutom",
	insecureAuth : true
});

connection.connect(function(err){
if(!err) {
    console.log("Database is connected ...");
} else {
    console.log(err.code);
}
});


app.get('/', function (req, res) {
    res.sendfile('views/index.html');
});

app.post('/results', (req, res) => {
  var college = req.body.college;
  var department = req.body.department;

  connection.query('SELECT NAME, SPECIALIZATION FROM PROFESSOR_DATA WHERE COLLEGE = ? AND DEPARTMENT = ?',[college, department], function (error, results, fields) {
  if (error) {
    console.log("error ocurred",error);
    res.send({
      "code":400,
      "failed":"error ocurred"
    })
  }else{
    res.render('index', {college: college, department: department, results: results});
  }
  });

});

const port = 8080;

app.listen(port, () => {
  console.log(`Server running on port${port}`);
});