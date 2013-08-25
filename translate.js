var querystring = require('querystring');
var http = require('http');

var text = process.argv.slice(2).join(" ").trim();

var data = querystring.stringify({
	text: text,
	from: "ru",
	to: "en"
});

var options = {
	host: "useful-functions.eu01.aws.af.cm",
	port: 80,
	path: "/google-translate",
	method: "POST",
	headers: {
		"Content-Type": "application/x-www-form-urlencoded",
		"Content-Length": data.length
	}
};

var request = http.request(options, function(response) {
	response.setEncoding("utf8");
	result = "";
	response.on("data", function (chunk) {
		result += chunk;
	});
	response.on("end", function() {
		process.stdout.write(result);
	});
});

request.write(data);
request.end();