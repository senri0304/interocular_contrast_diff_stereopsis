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

#temp$cdt <- 30 - temp$cdt

#contrast_diff_0 <- subset(temp, temp$trial %in% 0:4)
#contrast_diff_4 <- subset(temp, temp$trial %in% 5:9)
#contrast_diff_8 <- subset(temp, temp$trial %in% 10:14)
#contrast_diff_16 <- subset(temp, temp$trial %in% 15:19)
#contrast_diff_28 <- subset(temp, temp$trial %in% 19:24)

contrast5 <- subset(temp, luminance %in% 5)
contrast15 <- subset(temp, luminance %in% 15)
contrast25 <- subset(temp, luminance %in% 25)
contrast35 <- subset(temp, luminance %in% 35)
contrast60 <- subset(temp, luminance %in% 60)
contrast200 <- subset(temp, luminance %in% 200)


contrast5$cnd <- 2.4
contrast15$cnd <- 4.9
contrast25$cnd <- 7.5
contrast35$cnd <- 13.2
contrast60$cnd <- 22.9
contrast200$cnd <- 0.7

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

# Anovakun
#source("anovakun_483.txt") # encoding = "CP932"
#anovakun(dc,"sA", 5, peta=T, cm = F, holm=T)

# Calculate SD
sd <- sd(temp$cdt[])
for (l in 2:ddd) {sd = cbind(sd, sd(dc[,l]))}

# Calculate SE
se = sd/sqrt(n)

# Plot all data
camp = subset(ano, ano$complementary == 0, c("cnd", "x"))
cdt <- aggregate(x=camp$x, by=camp["cnd"], FUN=mean)
par(mfrow=c(1,1))
plot(x=cdt$cnd, y=cdt$x, xlim=c(0,23), ylim=c(0,30), type="b", xlab="contrast_diff", ylab="cumultive disapperance times(sec)", col="red")
arrows(cdt$cnd, cdt$x-se[1:(length(se)/2)], cdt$cnd, cdt$x+se[1:(length(se)/2)], length=0.05, angle=90, code=3, col="red")
par(new=T)
camp = subset(ano, ano$complementary == 1, c("cnd", "x"))
cdt <- aggregate(x=camp$x, by=camp["cnd"], FUN=mean)
plot(cdt$cnd, cdt$x, type="b", col="blue", xlim=c(0,23), ylim=c(0,30), xlab="", ylab="")
arrows(cdt$cnd, cdt$x-se[(length(se)/2+1):length(se)], cdt$cnd, cdt$x+se[(length(se)/2+1):length(se)], length=0.05, angle=90, code=3, col="blue")
#par(new=F)[length(se)/2:length(se)]
