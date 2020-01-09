source('facilitationRDS/contrast.R')

# List up files
files = list.files('facilitationRDS/data',full.names=T)
f = length(files)

si = gsub(".*(..)DATE.*","\\1", files)
n = length(table(si))
usi = unique(si)

# Load data and store
temp = read.csv(files[1])
temp$sub = si[1]
temp$sn <- 1 
for (i in 2:f) {
  d = read.csv(files[[i]])
  d$sub = si[i]
  d$sn <- i
  temp = rbind(temp, d)
}

contrast5 <- subset(temp, luminance %in% 5)
contrast15 <- subset(temp, luminance %in% 15)
contrast25 <- subset(temp, luminance %in% 25)
contrast35 <- subset(temp, luminance %in% 35)
contrast60 <- subset(temp, luminance %in% 60)
contrast200 <- subset(temp, luminance %in% 200)

contrast5$cnd <- 2.4
contrast15$cnd <- 11.2
contrast25$cnd <- 20.2
contrast35$cnd <- 28.0
contrast60$cnd <- 44.7
contrast200$cnd <- 99.3

temp <- rbind(contrast5, contrast15)
temp <- rbind(temp, contrast25)
temp <- rbind(temp, contrast35)
temp <- rbind(temp, contrast60)

# Plot indivisual data
par(mfrow=c(2,3))
for (i in 1:n){
  camp = subset(temp, temp$sub == usi[i] & temp$complementary == 0, c("luminance", "cdt"))
  plot(camp, xlim=c(0,60), ylim=c(0,30), type="p", xlab="contrastof of left half image", ylab="cdt(sec)", main=toupper(usi[i]))
  par(new=T)
  plot(aggregate(x=camp$cdt, by=camp["luminance"], FUN=mean), type="l", col="blue", xlim=c(0,60), ylim=c(0,30), xlab="", ylab="")
  par(new=F)
  camp = subset(temp, temp$sub == usi[i] & temp$complementary == 1, c('luminance', "cdt"))
  plot(camp, xlim=c(0,60), ylim=c(0,30), type="p", xlab="contrastof of left half image", ylab="cdt(sec)", main=toupper(usi[i]))
  par(new=T)
  plot(aggregate(x=camp$cdt, by=camp["luminance"], FUN=mean), type="l", col="blue", xlim=c(0,60), ylim=c(0,30), xlab="", ylab="")
  par(new=F)
}

# Reshape data for anova
ano = aggregate(x=temp$cdt, by=temp[c("cnd","sub", "complementary")], FUN=mean)
library("reshape2")
dc = dcast(ano, sub ~ cnd + complementary, fun.aggregate=mean, value.var="x")
dc = subset(dc, select = -sub)
ddd = ncol(dc)

c200 <- c(0, 0, 0, 0, 0)
dc2 <- c200
dc2 <- cbind(dc2, c200)
colnames(dc2) <- c("0.99_0", "0.99_1")

dc2 <- cbind(dc, dc2)

# Anovakun
source("anovakun_483.txt") # encoding = "CP932"
anovakun(dc2,"sAB", 6, 2, peta=T, cm = T, holm=T)

# Calculate SD
sd <- sd(temp$cdt[])
for (l in 2:ddd) {sd = cbind(sd, sd(dc[,l]))}
sd200 <- sd(contrast200$cdt)

# Calculate SE
se = sd/sqrt(n)
se200 <- sd200/sqrt(n)


# Plot all data(function as contrast of left halves)
camp = subset(ano, ano$complementary == 0, c("cnd", "x"))
cdt <- aggregate(x=camp$x, by=camp["cnd"], FUN=mean)
par(mfrow=c(1,1))
plot(x=cdt$cnd, y=cdt$x, xlim=c(0,50), ylim=c(0,30), type="b", xlab="contrast of left halves", ylab="cumultive response times(sec)", 
     col="red", cex.lab=1.5)
arrows(cdt$cnd, cdt$x-se[1:(length(se)/2)], cdt$cnd, cdt$x+se[1:(length(se)/2)], length=0.05, angle=90, code=3, col="red")
par(new=T)
camp = subset(ano, ano$complementary == 1, c("cnd", "x"))
cdt2 <- aggregate(x=camp$x, by=camp["cnd"], FUN=mean)
plot(cdt2$cnd, cdt2$x, type="b", col="blue", xlim=c(0,50), ylim=c(0,30), xlab="", ylab="")
arrows(cdt2$cnd, cdt2$x-se[(length(se)/2+1):length(se)], cdt2$cnd, cdt2$x+se[(length(se)/2+1):length(se)], length=0.05, angle=90, code=3, col="blue")


# Plot all data(function as contrast difference)
plot(x=b[1:6], y=c(cdt$x, mean(contrast200$cdt)), type='b',xlim=c(0,max(b[1:6])), ylim=c(0,30), xlab="contrast difference(dB)", ylab="cumultive response times(sec)", 
     col="red", cex.lab=1.5)
arrows(b[1:5], c(cdt$x)-se[1:(length(se)/2)], b[1:5], c(cdt$x)+se[1:(length(se)/2)],
       length=0.05, angle=90, code=3, col="red")
par(new=T)
plot(b[1:6], c(cdt2$x, mean(contrast200$cdt)), type="b", col="blue", xlim=c(0,max(b[1:6])),
     ylim=c(0,30), xlab="", ylab="")
arrows(b[1:5], c(cdt2$x)-se[(length(se)/2+1):length(se)], b[1:5],
       c(cdt2$x)+se[(length(se)/2+1):length(se)], length=0.05, angle=90, code=3, col="blue")
#arrows(b[6], mean(contrast200$cdt)-se200, b[6],
#       mean(contrast200$cdt)+se200, length=0.05, angle=90, code=3)
legend('topleft', legend = c('No noise', 'Noised'), col=c('red', 'blue'), lty=c(1, 1))
lines(c(4.15, 4.15), c(-1, 20), col='cyan')
par(new=F)


# polynomial regression
camp <- rbind(temp, contrast200)
g <- aggregate(cdt ~ cnd + complementary + sub, data=camp, FUN=mean)
g$db <- rep(b[1:6], 10)
g1 <- subset(g, complementary!=1)
g2 <- subset(g, complementary!=0)

g1mod1 <- glm(cdt ~ poly(db, 1), data=g1)
g1mod2 <- glm(cdt ~ poly(db, 2), data=g1)
g1mod3 <- glm(cdt ~ poly(db, 3), data=g1)
g1mod4 <- glm(cdt ~ poly(db, 4), data=g1)
g1mod5 <- glm(cdt ~ poly(db, 5), data=g1)

AIC(g1mod1)
AIC(g1mod2)
AIC(g1mod3)
AIC(g1mod4)
AIC(g1mod5)

anova(g1mod4)
summary(g1mod4)
plot(cdt ~ db, g1,  col="red", xlim=c(0,max(b[1:6])), ylim=c(0,30), main='polynomial regression')

g3 <- aggregate(cdt ~ db, g1, mean)
line1 <- glm(cdt ~ poly(db, 4), data=g3)
lines(fitted(line1) ~ db, g3, col='red')

par(new=T)

g2mod1 <- glm(cdt ~ poly(db, 1), data=g2)
g2mod2 <- glm(cdt ~ poly(db, 2), data=g2)
g2mod3 <- glm(cdt ~ poly(db, 3), data=g2)
g2mod4 <- glm(cdt ~ poly(db, 4), data=g2)
g2mod5 <- glm(cdt ~ poly(db, 5), data=g2)

AIC(g2mod1)
AIC(g2mod2)
AIC(g2mod3)
AIC(g2mod4)
AIC(g2mod5)

anova(g2mod3)
summary(g2mod3)
plot(cdt ~ db, g2,  col="blue", xlim=c(0,max(b[1:6])), ylim=c(0,30))

g3 <- aggregate(cdt ~ db, g2, mean)
line2 <- glm(cdt ~ poly(db, 3), data=g3)
lines(fitted(line2) ~ db, g3, col='blue')

