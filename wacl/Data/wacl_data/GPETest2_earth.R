library(DiceOptim)

grid <- read.csv("5sconcat_1123.csv")

# set the trend for each dimension, eg specie X1,X2, X3 are 3rd order polynomials, and X4 is a second order.
       
        formula <- y ~ poly(X1,2,raw=TRUE)+ poly(X2,2,raw=TRUE)+ poly(X3,2,raw=TRUE)+ poly(X4,2,raw=TRUE)+ poly(X5,2,raw=TRUE) + poly(X6,2,raw=TRUE)
 
#X1-4 are inputs, grid.z is the resultant output of the model/experiment.  
 
        suppressWarnings(repeat{#ensure variance != 0  
 
                model <- km(formula=formula , design=data.frame(X1= grid[0:12000,7], X2= grid[0:12000,9],X3=grid[0:12000,15],X4=grid[0:12000,16],X5=grid[0:12000,18],X6=grid[0:12000,20]) , response=data.frame(y=grid[0:12000,12]),covtype="gauss", nugget.estim=TRUE)       
 
                if (model@covariance@sd2 > 0) break              })
 
 
 
#to predict
#newdata is predictive input values you are interested in.  SK = standard kriging (no noise i.e. no corrections needed, there are other options for noisy data.)
 
    pred.grid <- predict.km(object=model, newdata=data.frame(X1= grid[12001:15466,7], X2= grid[12001:15466,9],X3=grid[12001:15466,15],X4=grid[12001:15466,16],X5=grid[12001:15466,18],X6=grid[12001:15466,20]), type="UK")
    
    
    t=seq(12001,15466)
    
    plot(t,grid[12001:15466,12],col='green')
    lines(t,pred.grid$mean)
	lines(t,pred.grid$lower95,col="red")
	lines(t,pred.grid$upper95,col="red")
 
 
 