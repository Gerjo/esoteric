// Quick test to see who converges quicker

// squared error
function e(w, t, x, y) {
  return Math.pow(t - w * x - w*w*y, 2);
}

// e's derivative
function d(w, t, x, y) {
  return 2 * (t - w * x - w*w * y) * (-x - 2*w*y);
}

// Initial values
var newton_w     = 0;
var gradient_w   = newton_w;

// Learn rate
var ita = 0.005;

console.clear();

// Iterate!
for(var i = 0; i < 20; ++i) {
  // Sum the errors
  var sum_d_newton = d(newton_w, 8, 2, 1) + d(newton_w, 10, 1, 2);
  var sum_e_newton = e(newton_w, 8, 2, 1) + e(newton_w, 10, 1, 2);
 
  var sum_d_gradient = d(gradient_w, 8, 2, 1) + d(gradient_w, 10, 1, 2);

  
  gradient_w -= ita * sum_d_gradient;
  newton_w -= sum_e_newton/sum_d_newton;
  
  console.log("Gradient: " + gradient_w.toFixed(6) + " Newton: " +  newton_w.toFixed(6));
}
