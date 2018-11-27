//get the data files
var args = process.argv.splice(2);
var inputFile = '';
var outputFile = '';

console.log('Processing data and output to json file with args length: ' + args.length);
if (args.length == 0) {		//first argument is the input file name
	inputFile = 'tmp.js';
} else {
	inputFile = args[0]
}

if (args.length >= 2) {		//second arg is the output json file name
	outputFile = args[1];
} else {
	outputFile = 'jout.json';
	// console.log(outputFile);
}

var data = require('./' + inputFile).data.rows;
// console.log(data.total);
data = JSON.stringify(data);
// console.log('------');
// console.log(data);

//write the data as json
var fs = require('fs');

fs.writeFile(outputFile, data + '\n', {flag : 'a'}, function(err){
	if (err) {
		console.error('Can not open the file: ' + outputFile + '!');
		console.error(err);
	}
	console.log('Finishing process data and output it to ' + outputFile);
	//throw err;
});