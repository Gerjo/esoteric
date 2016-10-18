var n = 9; // Group modulo

var out = "     ";
for(var i = 0; i < n; ++i) {
    out += Pad(i) + " ";
}

console.log(out);
console.log(Array(out.length).join("-"));

for(var i = 0; i < n; ++i) {
    
    var out = Pad(i) + "|  ";
    
    for(var j = 0; j < n; ++j) {
         out += Pad((j*i) % n) + " ";   
         //out += Pad((j + i) % n, p) + " ";   
    }
    
    out += "   " + i + "^" + n + "=" + (Math.pow(i, n) % n) + "    " +
     i + "*" + n + "=" + ((i*n)%n);
    
    console.log(out);
}

/// Prefix numbers with spaces.
function Pad(n) {
    var digits = 2;
    
    var d = Math.floor(Math.log(n) / Math.log(10));
    
    if(Math.abs(d) == Infinity) {
        d = 0;
    }
        
    if(d < digits) {
        return Array(digits - d).join(" ") + n;
    }
    
    return n;
}
