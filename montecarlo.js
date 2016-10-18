/// Estimate area under curve

function f(x) {
  return 3 + Math.pow(x, 2);
}

var w = 2;
var h = 4;

var domain = w * h;
var n = 5000;

var under = 0;


for(var i = 0; i < n; ++i) {
  var x = Math.random() * 2 -1;
  var y = Math.random() * h;
  
  if(f(x) > y) {
    ++under;
  }
}

console.log("Darts approach: " + domain*(under/n));



var sum    = 0;

for(var i = 0; i < n; ++i) {
  var x = Math.random() * 2 -1;
  var y = f(x);
  
  sum += y;
}

console.log("Sum approach: " + w * (sum/n));
