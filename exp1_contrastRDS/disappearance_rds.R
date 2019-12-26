# List up files
files = list.files('exp1_contrastRDS/data',full.names=T)
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

contrast_diff_0 <- subset(temp, temp$trial %in% 0:4)
contrast_diff_4 <- subset(temp, temp$trial %in% 5:9)
contrast_diff_8 <- subset(temp, temp$trial %in% 10:14)
contrast_diff_16 <- subset(temp, temp$trial %in% 15:19)
contrast_diff_28 <- subset(temp, temp$trial %in% 19:24)

contrast_diff_0$cnd <- 2.4
contrast_diff_4$cnd <- 4.9
contrast_diff_8$cnd <- 7.5
contrast_diff_16$cnd <- 13.2
contrast_diff_28$cnd <- 22.9

temp <- rbind(contrast_diff_0, contrast_diff_4)
temp <- rbind(temp, contrast_diff_8)
temp <- rbind(temp, contrast_diff_16)
temp <- rbind(temp, contrast_diff_28)

# Plot indivisual data
par(mfrow=c(2,3))
for (i in 1:n){
  camp = subset(temp, temp$sub == usi[i], c("cnd", "cdt"))
  plot(camp, xlim=c(0,23), ylim=c(0,30), type="p", xlab="contrastof of left half image", ylab="cdt(sec)", main=toupper(usi[i]))
  par(new=T)
  plot(aggregate(x=camp$cdt, by=camp["cnd"], FUN=mean), type="l", col="blue", xlim=c(0,23), ylim=c(0,30), xlab="", ylab="")
  par(new=F)
}


# Reshape data for anova
ano = aggregate(x=temp$cdt, by=temp[c("cnd","sub")], FUN=mean)
library("reshape2")
dc = dcast(ano, sub ~ cnd, fun.aggregate=mean, value.var="x")
dc = subset(dc, select = -sub)
ddd = ncol(dc)

# Anovakun
source("anovakun_483.txt") # encoding = "CP932"
anovakun(dc,"sA", 5, peta=T, cm = F, holm=T)

# Calculate SD
sd = sd(temp$cdt[])
for (l in 2:ddd) {sd = cbind(sd, sd(dc[,l]))}

# Calculate SE
se = sd/sqrt(n)


# Plot all data
cdt <- aggregate(x=temp$cdt, by=temp["cnd"], FUN=mean)
par(mfrow=c(1,1))
#plot(x=temp$cnd, y=temp$cdt, xlim=c(0,23), ylim=c(0,30), type="p", xlab="contrast_diff", ylab="cumultive disapperance times(sec)")
#par(new=T)
plot(cdt, type="l", col="blue", xlim=c(0,23), ylim=c(0,30), xlab="", ylab="")
arrows(cdt$cnd, cdt$x-se, cdt$cnd, cdt$x+se, length=0.05, angle=90, code=3)
#par(new=F)
