
frequency = 3
samples = 16;
ts = 1 / samples

x <- seq(0, samples, by=1) * (2 * pi / samples)
y <- sin(x * frequency)
n <- seq(0, samples, by=1)

freq <- samples / ts * n
freq

plot(x, y)

out <- fft(y)

plot(abs(out), type="l")
plot(atan2(Re(out), Im(out)), type="l")
#lines(abs(out))
