##############################################################################################
############################# importing training & testing data ##############################
##############################################################################################
# read train_data
train = read.csv(file = "D:/Study/Case Studies/kaggle.com/Shelter-Animal-Outcomes-by-kaggle.com/original_data/train.csv",
                 stringsAsFactors=FALSE)
Dataset = c(rep("train", length(train[,1])))
train=data.frame(train,Dataset,
                 stringsAsFactors = FALSE)
# read test_data
test = read.csv(file = "D:/Study/Case Studies/kaggle.com/Shelter-Animal-Outcomes-by-kaggle.com/original_data/test.csv",
                stringsAsFactors=FALSE)
test$ID = as.character(test$ID)
Dataset = c(rep("test", length(test[,1])))
test=data.frame(test,Dataset,
                stringsAsFactors = FALSE)
names(test)[1]=c("AnimalID")


##############################################################################################
###################################### data preparation ######################################
##############################################################################################
# collating training & testing data for cleaning
data = bind_rows(train,test)
data = data[order(data$AnimalID),]
rownames(data) = c(1:length(data[,1]))


################################## working with age variable #################################

# splitting "AgeuponOutcome" in two different columns
library(stringr)
age_data=as.data.frame(t(as.data.frame(str_split(data$AgeuponOutcome, " "))))
age_data = cbind(data$AnimalID,
                 age_data)
colnames(age_data) = c("AnimalID", "value", "unit")
row.names(age_data) = c(1:length(age_data$value))
# calculating age in days
temp=0
for (i in 1:length(age_data$unit)){
  ifelse(((age_data$unit[i]=="year") | (age_data$unit[i]=="years")),(temp[i]=as.numeric(as.vector(age_data$value[i]))*365),
         ifelse(((age_data$unit[i]=="month") | (age_data$unit[i]=="months")),(temp[i]=as.numeric(as.vector(age_data$value[i]))*30),
                ifelse(((age_data$unit[i]=="week") | (age_data$unit[i]=="weeks")),(temp[i]=as.numeric(as.vector(age_data$value[i]))*7),
                       ifelse(((age_data$unit[i]=="day") | (age_data$unit[i]=="days")),(temp[i]=as.numeric(as.vector(age_data$value[i]))*1),
                              (temp[i]="")))))
}
# including missing values when age = 0 or blank
for (i in 1:length(temp)){
  ifelse(temp[i]==0,(temp[i]=""),(temp[i]=temp[i]))
}
age_data = cbind(age_data,
                 as.numeric(temp))
colnames(age_data) = c("AnimalID", "value", "unit", "Age_in_days")
# treating missing values in "Age_in_days" column
temp=rep("0", times=length(age_data$Age_in_days))
for(i in 1:length(age_data$Age_in_days)){
  ifelse((is.na(age_data$Age_in_days[i])),(temp[i]="ageNA"),
         ifelse(((age_data$Age_in_days[i]>0) & (age_data$Age_in_days[i]<=225)), (temp[i]="age225"),
                ifelse(((age_data$Age_in_days[i]>225) & (age_data$Age_in_days[i]<=365)), (temp[i]="age365"),
                       ifelse(((age_data$Age_in_days[i]>365) & (age_data$Age_in_days[i]<=730)), (temp[i]="age730"),
                              ifelse(((age_data$Age_in_days[i]>730) & (age_data$Age_in_days[i]<=1825)), (temp[i]="age1825"),
                                     (temp[i]="age8030"))))))
}
age_data=data.frame(age_data,
                    agecategory=temp)
# creating dummy variable for Age_in_days
temp=unique(age_data$agecategory)
for(i in temp){
  age_data[i]=as.numeric(ifelse((age_data$agecategory==i),1,0))
}
age_data=subset(x = age_data,
                select=-c(ageNA))
age_data$AnimalID = as.character(age_data$AnimalID)


############################## working with AnimalType variable ###############################

# creating dummy variable for AnimalType
animal_type_data = subset(x = data,
                          select=c(AnimalID, AnimalType))
temp=unique(animal_type_data$AnimalType)
for(i in temp){
  animal_type_data[i]=as.numeric(ifelse((animal_type_data$AnimalType==i),1,0))
}
animal_type_data=subset(x = animal_type_data,
                        select = -c(Cat))
animal_type_data$AnimalID = as.character(animal_type_data$AnimalID)


################################# working with sex variable ##################################

# splitting "SexuponOutcome" in two different columns
library(stringr)
sex_data=as.data.frame(t(as.data.frame(str_split(data$SexuponOutcome, " "))))
sex_data = cbind(data$AnimalID, sex_data)
colnames(sex_data) = c("AnimalID", "sex_subtype", "sex")
row.names(sex_data) = c(1:length(sex_data$sex))
# including missing values when sex = 0 or blank or "Unknown"
for (i in 1:length(sex_data$AnimalID)){
  ifelse(((sex_data$sex_subtype[i]==0)),(sex_data$sex[i]="Unknown"),(sex_data$sex[i]=sex_data$sex[i]))
  ifelse(((sex_data$sex_subtype[i]== "")),(sex_data$sex[i]="Unknown"),(sex_data$sex[i]=sex_data$sex[i]))
  ifelse(((sex_data$sex_subtype[i]==0)),(sex_data$sex_subtype[i]="Unknown"),(sex_data$sex_subtype[i]=sex_data$sex_subtype[i]))
  ifelse(((sex_data$sex_subtype[i]== "")),(sex_data$sex_subtype[i]="Unknown"),(sex_data$sex_subtype[i]=sex_data$sex_subtype[i]))
}
# creating dummy variables for sex, sex=Unknown as reference
temp=unique(sex_data$sex)
for(i in temp){
  sex_data[i]=as.numeric(ifelse((sex_data$sex==i),1,0))
}
sex_data=subset(sex_data, select = -c(Unknown))
# creating dummy variables for sex_subtype, sex_subtype=Unknown as reference
temp=unique(sex_data$sex_subtype)
for(i in temp){
  sex_data[i]=as.numeric(ifelse((sex_data$sex_subtype==i),1,0))
}
sex_data=subset(sex_data, select = -c(Unknown))
sex_data$AnimalID = as.character(sex_data$AnimalID)


################################# working with color variable #################################

# splitting "Color" in two different columns
library(stringr)
color_data=as.data.frame(str_split(data$Color, "/"),
                         stringsAsFactors=FALSE)
temp=matrix(c(0),nrow(color_data),ncol(color_data))
for(i in 1:ncol(color_data)){
  temp[,i]=as.matrix(sort(color_data[,i]))
}
color_data=data.frame(data$AnimalID,
                      t(temp),
                      stringsAsFactors=FALSE);
colnames(color_data) = c("AnimalID", "color1", "color2")
for(i in 1:length(color_data$AnimalID)){
  ifelse(color_data$color1[i]==color_data$color2[i], (color_data$color2[i]=""),(color_data$color2[i]=color_data$color2[i]))
}
# creating color groups for same shade of colors. eg: blue tabby, blue cream and blue will belong to color group blue.
temp1=as.data.frame(str_split_fixed(color_data$color1, " ",2),
                    stringsAsFactors=FALSE)
temp1=as.data.frame(temp1[,-2],
                    stringsAsFactors=FALSE)
temp2=as.data.frame(str_split_fixed(color_data$color2, " ",2),
                    stringsAsFactors=FALSE)
temp2=as.data.frame(temp2[,-2],
                    stringsAsFactors=FALSE)
color_data=data.frame(color_data$AnimalID,
                      temp1, temp2)
colnames(color_data) = c("AnimalID", "color1", "color2")
# including missing values wherever applicable
for (i in 1:length(temp)){
  ifelse(color_data$color1[i]=="",(color_data$color1[i]=NA),(color_data$color1[i]=color_data$color1[i]))
  ifelse(color_data$color2[i]=="",(color_data$color2[i]=NA),(color_data$color2[i]=color_data$color2[i]))
}
# creating dummy variables for colors, color=White as reference
temp=unique(c(color_data$color1,color_data$color2))
temp=temp[!is.na(temp)]
for(i in temp){
  color_data[i]=as.numeric(ifelse((color_data$color1==i | color_data$color2==i),1,0))
}
temp = data.frame(AnimalID=color_data$AnimalID,
                  color_data[,4:length(color_data)])
temp[is.na(temp)]=0
temp1=temp[c(2:length(temp))]
temp1=subset(x = temp1,
             select = -c(White))
color_data=data.frame(AnimalID=temp$AnimalID,
                      color1=color_data$color1,
                      color2=color_data$color2,
                      temp1)
color_data$AnimalID = as.character(color_data$AnimalID)


################################# working with Breed variable #################################

# splitting "Breed" in 3 different columns
breed_data=data.frame(data$AnimalID,
                      data$AnimalType,
                      data$Breed)
colnames(breed_data)=c("AnimalID", "AnimalType", "Breed")
breed_data$Breed=as.character(breed_data$Breed)
# working with Dog Breeds
library(dplyr)
library(stringr)
temp1=breed_data %>%
  filter(str_detect(breed_data$AnimalType, "Dog"))
# grouping dog breeds using AKC grouping system
temp1$Breed=sub("Nova Scotia Duck Tolling Retriever","Sporting",temp1$Breed)
temp1$Breed=sub("St. Bernard Rough Coat","Working",temp1$Breed)
temp1$Breed=sub("American Pit Bull Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Wire Hair Fox Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Soft Coated Wheaten Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("St. Bernard Smooth Coat","Working",temp1$Breed)
temp1$Breed=sub("Greater Swiss Mountain Dog","Working",temp1$Breed)
temp1$Breed=sub("Smooth Fox Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Jack Russell Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Parson Russell Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Australian Cattle Dog","Herding",temp1$Breed)
temp1$Breed=sub("Bernese Mountain Dog","Working",temp1$Breed)
temp1$Breed=sub("Cardigan Welsh Corgi","Herding",temp1$Breed)
temp1$Breed=sub("German Shorthair Pointer","Sporting",temp1$Breed)
temp1$Breed=sub("Pembroke Welsh Corgi","Herding",temp1$Breed)
temp1$Breed=sub("American Staffordshire Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("American Pit Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Flat Coat Retriever","Sporting",temp1$Breed)
temp1$Breed=sub("Black Mouth Cur","Herding",temp1$Breed)
temp1$Breed=sub("Dogue De Bordeaux","Working",temp1$Breed)
temp1$Breed=sub("Chesa Bay Retr","Sporting",temp1$Breed)
temp1$Breed=sub("German Wirehaired Pointer","Sporting",temp1$Breed)
temp1$Breed=sub("Old English Bulldog","Unknown",temp1$Breed)
temp1$Breed=sub("Treeing Walker Coonhound","Hound",temp1$Breed)
temp1$Breed=sub("Bull Terrier Miniature","Terrier",temp1$Breed)
temp1$Breed=sub("English Springer Spaniel","Sporting",temp1$Breed)
temp1$Breed=sub("Glen Of Imaal","Terrier",temp1$Breed)
temp1$Breed=sub("Port Water Dog","Working",temp1$Breed)
temp1$Breed=sub("Old English Sheepdog","Herding",temp1$Breed)
temp1$Breed=sub("Toy Fox Terrier","Toy",temp1$Breed)
temp1$Breed=sub("Welsh Springer Spaniel","Sporting",temp1$Breed)
temp1$Breed=sub("Wirehaired Pointing Griffon","Sporting",temp1$Breed)
temp1$Breed=sub("English Cocker Spaniel","Sporting",temp1$Breed)
temp1$Breed=sub("Treeing Tennesse Brindle","Unknown",temp1$Breed)
temp1$Breed=sub("Spanish Water Dog","Herding",temp1$Breed)
temp1$Breed=sub("Cardigan Welsh Corgi","Herding",temp1$Breed)
temp1$Breed=sub("Spinone Italiano","Sporting",temp1$Breed)
temp1$Breed=sub("Shetland Sheepdog","Herding",temp1$Breed)
temp1$Breed=sub("Miniature Schnauzer","Terrier",temp1$Breed)
temp1$Breed=sub("Border Collie","Herding",temp1$Breed)
temp1$Breed=sub("German Shepherd","Herding",temp1$Breed)
temp1$Breed=sub("American Eskimo","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Doberman Pinsch","Working",temp1$Breed)
temp1$Breed=sub("Chihuahua Shorthair","Toy",temp1$Breed)
temp1$Breed=sub("Australian Shepherd","Herding",temp1$Breed)
temp1$Breed=sub("Rat Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Siberian Husky","Working",temp1$Breed)
temp1$Breed=sub("Chow Chow","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Cocker Spaniel","Sporting",temp1$Breed)
temp1$Breed=sub("Lhasa Apso","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Boston Terrier","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Manchester Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Miniature Pinscher","Toy",temp1$Breed)
temp1$Breed=sub("Golden Retriever","Sporting",temp1$Breed)
temp1$Breed=sub("Cairn Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("American Bulldog","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Shih Tzu","Toy",temp1$Breed)
temp1$Breed=sub("Basset Hound","Hound",temp1$Breed)
temp1$Breed=sub("Chihuahua Longhair","Toy",temp1$Breed)
temp1$Breed=sub("Miniature Poodle","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Chinese Sharpei","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Silky Terrier","Toy",temp1$Breed)
temp1$Breed=sub("Yorkshire Terrier","Toy",temp1$Breed)
temp1$Breed=sub("Australian Kelpie","Working",temp1$Breed)
temp1$Breed=sub("Shiba Inu","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Plott Hound","Hound",temp1$Breed)
temp1$Breed=sub("Great Dane","Working",temp1$Breed)
temp1$Breed=sub("Belgian Malinois","Herding",temp1$Breed)
temp1$Breed=sub("Toy Poodle","Toy",temp1$Breed)
temp1$Breed=sub("Podengo Pequeno","Hound",temp1$Breed)
temp1$Breed=sub("Dutch Shepherd","Sporting",temp1$Breed)
temp1$Breed=sub("Great Pyrenees","Working",temp1$Breed)
temp1$Breed=sub("English Bulldog","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Carolina Dog","Unknown",temp1$Breed)
temp1$Breed=sub("Dogo Argentino","Unknown",temp1$Breed)
temp1$Breed=sub("Blue Lacy","Herding",temp1$Breed)
temp1$Breed=sub("Alaskan Husky","Unknown",temp1$Breed)
temp1$Breed=sub("Border Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Collie Rough","Herding",temp1$Breed)
temp1$Breed=sub("Norwich Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Italian Greyhound","Toy",temp1$Breed)
temp1$Breed=sub("English Coonhound","Hound",temp1$Breed)
temp1$Breed=sub("Afghan Hound","Hound",temp1$Breed)
temp1$Breed=sub("Bluetick Hound","Hound",temp1$Breed)
temp1$Breed=sub("Anatol Shepherd","Sporting",temp1$Breed)
temp1$Breed=sub("Airedale Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Dachshund Wirehair","Hound",temp1$Breed)
temp1$Breed=sub("Cavalier Span","Toy",temp1$Breed)
temp1$Breed=sub("English Pointer","Sporting",temp1$Breed)
temp1$Breed=sub("Bull Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Patterdale Terr","Terrier",temp1$Breed)
temp1$Breed=sub("Norfolk Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Rhod Ridgeback","Hound",temp1$Breed)
temp1$Breed=sub("Chinese Crested","Toy",temp1$Breed)
temp1$Breed=sub("American Foxhound","Hound",temp1$Breed)
temp1$Breed=sub("Collie Smooth","Herding",temp1$Breed)
temp1$Breed=sub("Standard Poodle","Non-Sporting",temp1$Breed)
temp1$Breed=sub("West Highland","Terrier",temp1$Breed)
temp1$Breed=sub("Finnish Spitz","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Bruss Griffon","Toy",temp1$Breed)
temp1$Breed=sub("Cane Corso","Working",temp1$Breed)
temp1$Breed=sub("Dachshund Longhair","Hound",temp1$Breed)
temp1$Breed=sub("Irish Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Queensland Heeler","Herding",temp1$Breed)
temp1$Breed=sub("Scottish Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("German Pinscher","Working",temp1$Breed)
temp1$Breed=sub("Alaskan Malamute","Working",temp1$Breed)
temp1$Breed=sub("Ibizan Hound","Hound",temp1$Breed)
temp1$Breed=sub("Japanese Chin","Toy",temp1$Breed)
temp1$Breed=sub("Welsh Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Skye Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("English Setter","Sporting",temp1$Breed)
temp1$Breed=sub("Pharaoh Hound","Hound",temp1$Breed)
temp1$Breed=sub("Standard Schnauzer","Working",temp1$Breed)
temp1$Breed=sub("Bearded Collie","Herding",temp1$Breed)
temp1$Breed=sub("Bichon Frise","Non-Sporting",temp1$Breed)
temp1$Breed=sub("French Bulldog","Non-Sporting",temp1$Breed)
temp1$Breed=sub("English Foxhound","Hound",temp1$Breed)
temp1$Breed=sub("Canaan Dog","Working",temp1$Breed)
temp1$Breed=sub("Tibetan Terrier","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Irish Wolfhound","Hound",temp1$Breed)
temp1$Breed=sub("Belgian Sheepdog","Herding",temp1$Breed)
temp1$Breed=sub("Swiss Hound","Hound",temp1$Breed)
temp1$Breed=sub("Boykin Span","Sporting",temp1$Breed)
temp1$Breed=sub("Swedish Vallhund","Herding",temp1$Breed)
temp1$Breed=sub("Tibetan Spaniel","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Presa Canario","Unknown",temp1$Breed)
temp1$Breed=sub("Belgian Tervuren","Herding",temp1$Breed)
temp1$Breed=sub("Irish Setter","Sporting",temp1$Breed)
temp1$Breed=sub("English Shepherd","Herding",temp1$Breed)
temp1$Breed=sub("Australian Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Sealyham Terr","Terrier",temp1$Breed)
temp1$Breed=sub("Treeing Cur","Unknown",temp1$Breed)
temp1$Breed=sub("Bedlington Terr","Terrier",temp1$Breed)
temp1$Breed=sub("Schnauzer Giant","Working",temp1$Breed)
temp1$Breed=sub("Spanish Mastiff","Unknown",temp1$Breed)
temp1$Breed=sub("Picardy Sheepdog","Herding",temp1$Breed)
temp1$Breed=sub("Neapolitan Mastiff","Working",temp1$Breed)
temp1$Breed=sub("Mexican Hairless","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Field Spaniel","Sporting",temp1$Breed)
temp1$Breed=sub("Norwegian Elkhound","Hound",temp1$Breed)
temp1$Breed=sub("Tan Hound","Hound",temp1$Breed)
temp1$Breed=sub("Labrador Retriever","Sporting",temp1$Breed)
temp1$Breed=sub("Redbone Hound","Hound",temp1$Breed)
temp1$Breed=sub("Dachshund","Hound",temp1$Breed)
temp1$Breed=sub("Newfoundland","Working",temp1$Breed)
temp1$Breed=sub("Pug","Toy",temp1$Breed)
temp1$Breed=sub("Catahoula","Herding",temp1$Breed)
temp1$Breed=sub("Harrier","Hound",temp1$Breed)
temp1$Breed=sub("Pointer","Sporting",temp1$Breed)
temp1$Breed=sub("Rottweiler","Working",temp1$Breed)
temp1$Breed=sub("Beagle","Hound",temp1$Breed)
temp1$Breed=sub("Keeshond","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Bullmastiff","Working",temp1$Breed)
temp1$Breed=sub("Weimaraner","Sporting",temp1$Breed)
temp1$Breed=sub("Pekingese","Toy",temp1$Breed)
temp1$Breed=sub("Vizsla","Sporting",temp1$Breed)
temp1$Breed=sub("Boxer","Working",temp1$Breed)
temp1$Breed=sub("Maltese","Toy",temp1$Breed)
temp1$Breed=sub("Akita","Working",temp1$Breed)
temp1$Breed=sub("Basenji","Hound",temp1$Breed)
temp1$Breed=sub("Pbgv","Hound",temp1$Breed)
temp1$Breed=sub("Bulldog","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Staffordshire","Terrier",temp1$Breed)
temp1$Breed=sub("Brittany","Sporting",temp1$Breed)
temp1$Breed=sub("Boerboel","Working",temp1$Breed)
temp1$Breed=sub("Black","Herding",temp1$Breed)
temp1$Breed=sub("Whippet","Hound",temp1$Breed)
temp1$Breed=sub("Feist","Terrier",temp1$Breed)
temp1$Breed=sub("Beauceron","Herding",temp1$Breed)
temp1$Breed=sub("Pomeranian","Toy",temp1$Breed)
temp1$Breed=sub("Schipperke","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Greyhound","Hound",temp1$Breed)
temp1$Breed=sub("Kuvasz","Working",temp1$Breed)
temp1$Breed=sub("Saluki","Hound",temp1$Breed)
temp1$Breed=sub("Leonberger","Working",temp1$Breed)
temp1$Breed=sub("Affenpinscher","Toy",temp1$Breed)
temp1$Breed=sub("Hovawart","Unknown",temp1$Breed)
temp1$Breed=sub("Havanese","Toy",temp1$Breed)
temp1$Breed=sub("Bloodhound","Hound",temp1$Breed)
temp1$Breed=sub("Mastiff","Working",temp1$Breed)
temp1$Breed=sub("Entlebucher","Herding",temp1$Breed)
temp1$Breed=sub("Papillon","Toy",temp1$Breed)
temp1$Breed=sub("Landseer","Unknown",temp1$Breed)
temp1$Breed=sub("Dalmatian","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Jindo","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Samoyed","Working",temp1$Breed)
temp1$Breed=sub("Otterhound","Hound",temp1$Breed)
temp1$Breed=sub("Lowchen","Non-Sporting",temp1$Breed)
temp1$Breed=sub("Yorkshire","Toy",temp1$Breed)
temp1$Breed=sub("Borzoi","Hound",temp1$Breed)
temp1$Breed=sub("Cardigan Welsh Corgi","Herding",temp1$Breed)
temp1$Breed=sub("Labrador Retriever","Sporting",temp1$Breed)
temp1$Breed=sub("Redbone Hound","Hound",temp1$Breed)
temp1$Breed=sub("American Pit Terrier","Terrier",temp1$Breed)
temp1$Breed=sub("Dachshund","Hound",temp1$Breed)
temp1$Breed=sub("Whippet","Hound",temp1$Breed)
temp1$Breed=sub(" Mix","/Unknown",temp1$Breed)
# final spliting of dog breeds
temp=as.data.frame(str_split_fixed(temp1$Breed, "/",3),
                   stringsAsFactors=FALSE)
temp1=data.frame(temp1$AnimalID,
                 temp1$AnimalType,
                 temp)
colnames(temp1) = c("AnimalID","AnimalType", "Breed1", "Breed2", "Breed3")

# working with Cat Breeds
library(dplyr)
library(stringr)
temp2=breed_data %>%
  filter(str_detect(breed_data$AnimalType, "Cat"))
# grouping cat breeds based on origin
temp2$Breed=sub(" Shorthair","",temp2$Breed)
temp2$Breed=sub(" Longhair","",temp2$Breed)
temp2$Breed=sub(" Medium Hair","",temp2$Breed)
temp2$Breed=sub(" Wirehair","",temp2$Breed)
temp2$Breed=sub(" Rough","",temp2$Breed)
temp2$Breed=sub(" Smooth Coat","",temp2$Breed)
temp2$Breed=sub(" Smooth","",temp2$Breed)
temp2$Breed=sub(" Black/Tan","",temp2$Breed)
temp2$Breed=sub("Black/Tan ","",temp2$Breed)
temp2$Breed=sub(" Flat Coat","",temp2$Breed)
temp2$Breed=sub("Flat Coat ","",temp2$Breed)
temp2$Breed=sub("Devon Rex","Rex",temp2$Breed)
temp2$Breed=sub("Cornish Rex","Rex",temp2$Breed)
temp2$Breed=sub(" Mix","/Unknown",temp2$Breed)
temp2$Breed=sub(" Shorthair","",temp2$Breed)
# final spliting of cat breeds
temp=as.data.frame(str_split_fixed(temp2$Breed, "/",2),
                   stringsAsFactors=FALSE)
temp2=data.frame(temp2$AnimalID,
                 temp2$AnimalType,
                 temp)
colnames(temp2) = c("AnimalID","AnimalType", "Breed1", "Breed2")

# merging cats and dogs table as breed_data
breed_data = bind_rows(temp1,temp2)
breed_data = breed_data[order(breed_data$AnimalID),]
rownames(breed_data) = c(1:length(breed_data[,1]))

# including missing values when breed = blank
for (i in 1:length(breed_data$AnimalID)){
  ifelse(breed_data$Breed1[i]=="",(breed_data$Breed1[i]=NA),(breed_data$Breed1[i]=breed_data$Breed1[i]))
  ifelse(breed_data$Breed2[i]=="",(breed_data$Breed2[i]=NA),(breed_data$Breed2[i]=breed_data$Breed2[i]))
  ifelse(breed_data$Breed3[i]=="",(breed_data$Breed3[i]=NA),(breed_data$Breed3[i]=breed_data$Breed3[i]))
}
# creating dummy variables for breed, breed=Unknown as reference
temp=unique(c(breed_data$Breed1,breed_data$Breed2,breed_data$Breed3))
temp=temp[!is.na(temp)]
for(i in temp){
  breed_data[i]=as.numeric(ifelse((breed_data$Breed1==i | breed_data$Breed2==i | breed_data$Breed3==i),1,0))
}
temp = data.frame(AnimalID=breed_data$AnimalID,
                  breed_data[,6:length(breed_data)])
temp[is.na(temp)]=0
temp1=temp[c(2:length(temp))]
temp1=subset(x = temp1,
             select = -c(Unknown))
breed_data=data.frame(AnimalID=temp$AnimalID,
                      AnimalType=breed_data$AnimalType,
                      breed1=breed_data$Breed1,
                      breed2=breed_data$Breed2,
                      breed3=breed_data$Breed3,
                      temp1)
breed_data$AnimalID = as.character(breed_data$AnimalID)


########################### preparing final datasets for modelling ############################
data=data.frame(subset(x = data,
                       select = c(AnimalID, OutcomeType)),
                Dog = animal_type_data$Dog,
                subset(x = age_data,
                       select = c(age225, age365, age730, age1825, age8030)),
                subset(x = sex_data,
                       select = -c(AnimalID, sex_subtype, sex)),
                subset(x = color_data,
                       select = -c(AnimalID, color1, color2)),
                subset(x = breed_data,
                       select = -c(AnimalID, AnimalType, breed1, breed2,breed3)),
                Dataset = data$Dataset)
# converting categorical variables into factors
for (i in c(1:91)){
  data[,i] = as.character(data[,i])
  data[,i] = factor(data[,i],levels=sort(unique(data[,i]))) 
}
# building training_data from data
training_data=subset(data, data$Dataset == "train")
training_data=subset(training_data, select=-c(Dataset))
rownames(training_data)=c(1:length(training_data$AnimalID))
# building testing_data from data
testing_data=subset(data, data$Dataset == "test")
testing_data=subset(testing_data, select=-c(Dataset))
rownames(testing_data)=c(1:length(testing_data$AnimalID))
testing_data=testing_data[,c(-2)]
names(testing_data)[1]=c("ID")
testing_data$ID=as.integer(testing_data$ID)
testing_data = testing_data[order(testing_data$ID),]

# removing all temporary objects created
remove(i, temp, temp1, temp2, Dataset)


##############################################################################################
####################################### Data Modeling ########################################
##############################################################################################

# building a model on training_data
library(randomForest)
set.seed(1)
forest = randomForest(x = training_data[,c(3:90)],
                      y = training_data[,2],
                      data = training_data,
                      ntree = 1000,
                      importance = TRUE)
print(forest)

# predict using testing_data
prediction = predict(object=forest,
                     newdata=testing_data[,c(2:89)],
                     type = "vote")

# creating the solution dataframe
solution = data.frame(ID = testing_data$ID,
                      prediction)

# exporting solution to solution.csv
write.csv(x = solution
          file = "D:/Study/Case Studies/kaggle.com/Shelter-Animal-Outcomes-by-kaggle.com/solution.csv",
          row.names=FALSE)
