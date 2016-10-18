cat("\014")

library(base)


if(require(tm) == FALSE) {
    print("Attempting to install TM support...");
    install.packages("tm")
    
    library(tm);
}

if(require(RSQLite) == FALSE) {
    print("Attempting to install SQLite support...");
    install.packages("RSQLite")
    
    library(RSQLite);
}

# Run a SQLite query and capture the result as a data frame.
runQuery <- function(sql) {
    
    tries <- 10
    
    # Give it a few tries. SQLite likes to give concurrency errors, e.g., when
    # browsing the data during an insert (table level locking, not row or column).
    while(tries > 0) {
        tryCatch(
            {
                res <- dbGetQuery(db, sql)
                tries <- 0
            },
            error = function(e) {
                cat(paste("Query failed, attempts left:", tries, "\n"))    
                Sys.sleep(1)
            }
                    )

        tries <- tries - 1
    }
    return(res)
}

# SVD with diagonal trimming, i.e., reduction of dimensions.
reduce <- function(mat, trimCount) {
    
    # Appl singular value decomposition
    res <- svd(mat)
    
    # Retrieve diagonal matrix as an actual diagonal.
    s <- diag(res$d)
    
    #print(round(s, digits = 3))
    
    # Set last n diagonal values to zero
    for(i in 1 : nrow(s)) {
        if(i > nrow(s) - trimCount) {
            s[i,i] <- 0;
            cat("null")
        }
    }
    
    reconstructed <- res$u %*% s %*% t(res$v)
    
    # Hack to overcome floating point issues. Numbers randomly change sign?
    # R relies on underlying libraries, there is no unified way of dealing
    # with irrational numbers, it would seem. Random stability!
    reconstructed <- round(reconstructed, digits = 10)
    
    # Reconstruct, with reduced dimensions
    return (reconstructed)
}

# Nicely hardcoded paths.
workdir <- "~/chamber/mmr/"

if( ! file.exists(workdir)) {
    warning(paste("Working directory", workdir, "does not exist. The database must be placed in this path."))    
}

setwd(workdir)

# Connect to the database
sqlite    <- dbDriver("SQLite")
db        <- dbConnect(sqlite, "./documents.sqlite")

documents <- runQuery("SELECT tweakersid, title, document FROM documents");

for(i in 1 : nrow(documents)) {
    document <- documents[i, ]
    comments <- runQuery(paste("SELECT score, document FROM comments WHERE moderated <> '0' AND tweakersid = ", document$tweakersid, sep = ""));
    
    # Merge document and comments into one space
    documentSpace <- c(document$document, comments["document"], recursive = TRUE)
    
    corpus <- VCorpus(VectorSource(documentSpace))
    
    # Filters and such
    corpus <- tm_map(corpus, stripWhitespace)
    corpus <- tm_map(corpus, removePunctuation)
    corpus <- tm_map(corpus, tolower)
    corpus <- tm_map(corpus, removeWords, stopwords("dutch"))
    
    # Count the words
    dtm <- DocumentTermMatrix(corpus)
    
    # Reduce data to two dimensions
    dtm = reduce(dtm, nrow(dtm) - 2)   
    #dtm = reduce(dtm, 50)   
    
    # Spearman's Rho correlation matrix (Filled with empty strings)
    spearman <- matrix("", nrow(dtm), 2) # m x 1
    
    # Compute compute compute!
    for(i in 1 : nrow(spearman)) {
        
        a <- as.vector(dtm[1, ])
        b <- as.vector(dtm[i, ])
        
        if(max(a) == 0 && min(a) == 0) {
            cat("Warning: null a vector.\n")
            next;
        }
        
        # Dimension reduction yields null vectors?
        if(max(b) == 0 && min(b) == 0) {
            cat("Warning: null b vector.\n")
            next;
        }
        
        # Compute spearman's Rho correlation factor
        c <- cor(a, b, method = "spearman")
        
        # ... or use the default correlation coefficient
        #c <- cor(a, b)
        
        spearman[i, 1] <- round(c, digits = 2)
            
        if(i > 1) {
            # lookup the score according to tweakers.net
            spearman[i, 2] <- comments[i - 1, "score"]
        }
    }
    
    # Pretty column names.
    colnames(spearman) <- c("Spearman's rank correlation coefficient", "Tweakers mod-Score")
    
    # Pretty plot.
    plot(spearman, xlim=c(-1, 1), ylim=c(-1, 2))
}

