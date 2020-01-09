l <- c(20.47, 17.17, 14.26, 12.09, 8.21, 0.07, 18.9)
bg <- 21.51

f <- function(x, y) (y - x) / (y + x)

c <- f(l, bg)

plot(l, c)
abline(lm(c~l))

plot(log(l), c)
abline(lm(c ~ log(l)))

dB <- function(x, y) log10(x/y)*10
b <- dB(c, c[1])
plot(c, b)

