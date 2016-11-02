library(DiceOptim)


# set the trend for each dimension, eg variables X1,X2, X3 are 3rd order polynomials, and X4 is a second order.
       
#         formula <- y ~ poly(X1,2,raw=TRUE)+poly(X2,2,raw=TRUE)+ poly(X3,2,raw=TRUE)+ poly(X4,2,raw=TRUE)
        formula <- y ~ (poly(X1,1,raw=TRUE)+poly(X2,1,raw=TRUE)+ poly(X3,1,raw=TRUE)+ poly(X4,1,raw=TRUE)+ poly(X7,1,raw=TRUE))
#        formula <- y ~ (poly(X7,1,raw=TRUE))
        
#        formula <- y ~ (poly(X4,2,raw=TRUE)+poly(X1,2,raw=TRUE)+poly(X2,2,raw=TRUE)+poly(X3,2,raw=TRUE))+(poly(X5,2,raw=TRUE)+poly(X1,2,raw=TRUE)+poly(X2,2,raw=TRUE)+poly(X3,2,raw=TRUE))+(poly(X6,2,raw=TRUE)+poly(X1,2,raw=TRUE)+poly(X2,2,raw=TRUE)+poly(X3,2,raw=TRUE))+(poly(X7,2,raw=TRUE)+poly(X1,2,raw=TRUE)+poly(X2,2,raw=TRUE)+poly(X3,2,raw=TRUE))+(poly(X8,2,raw=TRUE)+poly(X1,2,raw=TRUE)+poly(X2,2,raw=TRUE)+poly(X3,2,raw=TRUE))
#        formula <- y ~ (poly(X4,2,raw=TRUE)+poly(X1,2,raw=TRUE)+poly(X2,2,raw=TRUE)+poly(X3,2,raw=TRUE))+(poly(X5,2,raw=TRUE)+poly(X1,2,raw=TRUE)+poly(X2,2,raw=TRUE)+poly(X3,2,raw=TRUE))
#        formula <- y ~ (exp(X5)+exp(X6))
#        formula <- y ~ (poly(X5,1,raw=TRUE)+poly(X6,1,raw=TRUE))
 
#X1-4 are inputs, grid.z is the resultant output of the model/experiment.  
 
        suppressWarnings(repeat{#ensure variance != 0  
 
                model <- km(formula=formula , design=data.frame(X1= grid[,1], X2= grid[,2],X3=grid[,3],X4=grid[,4],X7=grid[,7]), response=data.frame(y=grid[,5]),covtype="gauss", nugget.estim=TRUE)       
 
                if (model@covariance@sd2 > 0) break              })
 
 
#to predict
#newdata is predictive input values you are interested in.  SK = standard kriging (no noise i.e. no corrections needed, there are other options for noisy data.)
 
#    pred.grid <- predict.km(object=model, newdata=data.frame(X1= testgrid[,4], X2= testgrid[,1],X3=testgrid[,2],X4=testgrid[,3]), type="UK")
    pred.grid <- predict.km(object=model, newdata=data.frame(X1= testgrid[,1], X2= testgrid[,2],X3=testgrid[,3],X4=testgrid[,4],X7=testgrid[,7]), type="UK")
    mean <- pred.grid$mean
    plot(model)
#    t=seq(1:dim(testgrid)[1]-1)
#    plot(t,testgrid[,6],type = "l")
#    lines(t, pred.grid$mean,col="blue")



 
 
 