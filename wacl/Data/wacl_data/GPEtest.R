library(DiceOptim)

read.csv("10sconcat_1112.csv")
# set the trend for each dimension, eg specie X1,X2, X3 are 3rd order polynomials, and X4 is a second order.
       
        formula <- y ~ poly(X1,5,raw=TRUE)+ poly(X2,5,raw=TRUE)+ poly(X3,5,raw=TRUE)+ poly(X4,2,raw=TRUE)
 
#X1-4 are inputs, grid.z is the resultant output of the model/experiment.  
 
        suppressWarnings(repeat{#ensure variance != 0  
 
                model <- km(formula=formula , design=data.frame(X1= grid[,1], X2= grid[,2],X3=grid[,3],X4=grid[,3]) , response=data.frame(y=grid.z),covtype="gauss", nugget.estim=TRUE)        
 
                if (model@covariance@sd2 > 0) break              })
 
 
 
#to predict
#newdata is predictive input values you are interested in.  SK = standard kriging (no noise i.e. no corrections needed, there are other options for noisy data.)
 
    pred.grid <- predict.km(object=model, newdata=newdata[60,], type="UK")
 
 
 
 
####
R from python
####
 
 
import rpy2.robjects as ro
import pandas.rpy.common as com
from rpy2.robjects import pandas2ri
pandas2ri.activate()
 
 
ro.r("source('layout.R')") # how to load files #use  library('DiceOptim') for libraries
ro.globalenv['g']= rdf #make rdf dataframe from pandas variable g in R
 
 
# r commands
ro.r("save(g,file = 'gdata')")
 
# get df of variable out3d back from R
pandas3d = com.load_data('out3d')