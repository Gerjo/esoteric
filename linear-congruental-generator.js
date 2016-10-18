
// Initial seed.
var x = 42;

function rand() {
  
  // Old random number becomes next seed.
  x = (1103515245 * x + 12345) % 2147483648;
  
  // Generate a floating point, then modulo to only keep
  // the fractional part.
  return (x * 0.001) % 1;
}


console.clear();

var grid = [];

// Generate many numbers.
for(var i = 0; i < 10000; ++i) {
  
  // Quantize random number.
  var bucket = parseInt(rand() * 100);
  
  // Cast a vote into the grid's bucket.
  grid[bucket] = grid[bucket] ? grid[bucket] + 1 : 1;
}


// Statistical reporting. The count per bucket should be
// uniform... more or less.
grid.forEach(function(bucket, i) {
  console.log("Sigfig: " + i / 100 + ", occurance: " + bucket);
});
