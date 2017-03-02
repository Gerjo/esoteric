    # Run this once to install benchmark suite:
    #install.packages(c("microbenchmark", "stringr"), dependencies = TRUE)
    require(microbenchmark)
    library(parallel)
    
    # Setup parallelization particulars.
    cores <- detectCores()
    cluster <- makeCluster(cores)
    
    gerardFizzBuzz <- function(i) {
        fizz <- i %% 3
        buzz <- i %% 5
      
        if (fizz == 0 & buzz == 0) {
          return('FizzBuzz')
        }
        else if (buzz == 0) {
          return('Buzz')
        }
        else if (fizz == 0) {
          return('Fizz')
        }
      
        return(i)
    }
    
    applyFizzBuzz <- function(range) {
        return(lapply(1:range, gerardFizzBuzz))
    }
    
    parallelFizzBuzz <- function(range) {
        return(parLapply(cluster, 1:range, gerardFizzBuzz))
    }
    
    vectorizedFizzBuzz <- function(range) {
        v <- Vectorize(gerardFizzBuzz)
        return(v(1:range))
    }
    
    papasmurfFizzBuzz <- function (range) {
        res <- seq(1, range)
      
        for (i in res){
          if (i %% 3 == 0 & i %% 5 == 0){
            res[i] <- 'FizzBuzz'
          }
          else if (i %% 5 ==0){
            res[i] <- 'Buzz'
          }
          else if (i %% 3 == 0){
            res[i] <- 'Fizz'
          }
          else{
            res[i] <- i
          }
        }
        
        return(res)
    }
    
    range <- 100000;
    
    perf <- microbenchmark(applyFizzBuzz(range), vectorizedFizzBuzz(range), parallelFizzBuzz(range), papasmurfFizzBuzz(range), times=20)
    
    # note the log scale.
    boxplot(perf, names = c("lapply", "Vectorized", "parLapply", "forloop"))

    stopCluster(cluster)