library(DiceOptim)
library(hydroGOF)

grid <- read.csv("neuralnetworknorm.csv")
#testgrid <- read.csv("neuralnetworknorm.csv")

pt_range <- dim(grid)[1]-1

testgrid <- grid[ceiling(pt_range*0.7):pt_range, 1:6]

grid <- grid[1:ceiling(pt_range*0.7), 1:5]

pt_range <- dim(grid)[1]-1

pt_max <- dim(testgrid)[1]-50

# set the trend for each dimension, eg variables X1,X2, X3 are 3rd order polynomials, and X4 is a second order.
       
        formula <- y ~ poly(X1,1,raw=TRUE)+ poly(X2,2,raw=TRUE)+ poly(X3,2,raw=TRUE)+ poly(X4,2,raw=TRUE)
 
#X1-4 are inputs, grid.z is the resultant output of the model/experiment.  
 
        suppressWarnings(repeat{#ensure variance != 0  
 
                model <- km(formula=formula , design=data.frame(X1= grid[2:pt_range,1], X2= grid[2:pt_range,2],X3=grid[2:pt_range,3],X4=grid[2:pt_range,4]) , response=data.frame(y=grid[2:pt_range,5]),covtype="gauss", nugget.estim=TRUE)       
 
                if (model@covariance@sd2 > 0) break              })
 
 
 
#to predict
#newdata is predictive input values you are interested in.  SK = standard kriging (no noise i.e. no corrections needed, there are other options for noisy data.)
 
    pred.grid <- predict.km(object=model, newdata=data.frame(X1= testgrid[1:pt_max,1], X2= testgrid[1:pt_max,2],X3=testgrid[1:pt_max,3],X4=testgrid[1:pt_max,4]), type="UK")
    
    
    t=seq(1:pt_max)
    
    g_range <- range(pred.grid$lower95,pred.grid$upper95)
    
    plot(t,testgrid[1:pt_max,5],type = "l")
    lines(t, testgrid[1:pt_max,4],col="blue")
    lines(t, testgrid[1:pt_max,6],col="green")
	lines(t,pred.grid$lower95,col="red")
    sim_gp <- pred.grid$lower95
    obs <- testgrid[1:pt_max,5]
    sim_nn <- testgrid[1:pt_max,6]
    mse(sim_gp, obs)
    mse(sim_nn, obs)

	#lines(t,pred.grid$upper95,col="red")

 
 
 