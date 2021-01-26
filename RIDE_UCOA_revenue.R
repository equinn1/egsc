rm(list = ls())

setwd("/home/gquinn/EG/school_committee/finance_subcommittee")

read_revenue <- function(year,dsn) {
  df = read.csv(dsn)
  Fyear = rep(year,nrow(df)) 
  df <- cbind(df, Fyear)     # Add new column to data - fiscal year
  return(df)
}

rev <- read_revenue(2019,"RIDE/94_All_Revenue_Account_Strings_with_Descriptions_2018-19.csv")
rev <- rev[ , ! names(rev) %in% c("Loc", "Location.Description", "Func", "Function.Description")]
names(rev)

tmp <- read_revenue(2018,"RIDE/94-All-Revenue-Account-Strings-with-Descriptions-FY18.csv")
tmp <- tmp[ , ! names(tmp) %in% c("Loc", "Location.Description", "Func", "Function.Description")]
names(tmp)
rev <- rbind(rev,tmp)

tmp <- read_revenue(2017,"RIDE/94-All-Revenue-Account-Strings-with-Descriptions-FY17.csv")
tmp <- tmp[ , ! names(tmp) %in% c("Loc", "Location.Description", "Func", "Function.Description")]
names(tmp)
rev <- rbind(rev,tmp)


tmp <- read_revenue(2016,"RIDE/FY16-All-Revenue-Account-Strings-with-Descriptions.csv")
tmp <- tmp[ , ! names(tmp) %in% c("Loc", "Location.Description", "Func", "Function.Description")]
names(tmp)
rev <- rbind(rev,tmp)

tmp <- read_revenue(2015,"RIDE/94-All-Revenue-Account-Strings-with-Descriptions-with-budget.csv")
tmp <- tmp[ , ! names(tmp) %in% c("Loc", "Location.Description", "Func", "Function.Description")]
names(tmp)
rev <- rbind(rev,tmp)

tmp <- read_revenue(2014,"RIDE/94-All-Revenue-Account-Strings-with-Descriptions-081415.csv")
tmp <- tmp[ , ! names(tmp) %in% c("Loc", "Location.Description", "Func", "Function.Description")]
names(tmp)
rev <- rbind(rev,tmp)

tmp <- read_revenue(2013,"RIDE/94-All-Revenue-Account-Strings-with-Descriptions-FY13.csv")
tmp <- tmp[ , ! names(tmp) %in% c("Loc", "Location.Description", "Func", "Function.Description", 
                                  "X","X.1")]
names(tmp)
rev <- rbind(rev,tmp)

tmp <- read_revenue(2012,"RIDE/FY12-Revenue.csv")
tmp <- tmp[ , ! names(tmp) %in% c("Loc", "Location.Description", "Func", "Function.Description")]
names(tmp)
rev <- rbind(rev,tmp)

tmp <- read_revenue(2011,"RIDE/FY11-94-All-Revenue-Account-Strings-with-Descriptions.csv")
tmp <- tmp[ , ! names(tmp) %in% c("Loc", "Location.Description", "Func", "Function.Description")]
names(tmp)
rev <- rbind(rev,tmp)

names(rev)

tmp <- read_revenue(2010,"RIDE/FY10-Revenue.csv")
District.ID = sprintf("%03d",tmp$Dist.No)
tmp <- cbind(tmp,District.ID)
Budget = rep(NA,nrow(tmp))
tmp <- cbind(tmp,Budget)
tmp <- tmp[ , ! names(tmp) %in% c("ID", "Loc", "Func", "Prog", "JC",
        "Location.Description","Dist.No","Sub")]

names(tmp)[2] <-"Object"
names(tmp)[4] <-"District.Name"
names(tmp)[6] <-"Revenue.Object.Description"
names(tmp)

names(rev)

rev = rbind(rev,tmp)
names(rev)

save(rev, file="RIDE_UCOA_revenue.RData")