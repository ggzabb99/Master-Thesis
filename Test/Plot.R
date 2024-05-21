library(ggplot2)
#####     請將底線處修改為要繪製的檔案     #####
load("../../Result/_/_.RData")             #
############################################
dataset$x <- as.numeric(dataset$x)
dataset$y <- as.numeric(dataset$y)



p <- ggplot(dataset, aes(x=x, y=y, color=`Political leanings`)) + 
  geom_point(shape = 21, aes(color=`Political leanings`, fill=`Political leanings`), size = 5, stroke = 1.7) + 
  theme_minimal() +
  labs(x="Dim 1", y="Dim 2", size = 20) + 
  scale_color_manual(values=c("Pan-green celebrities" = "#79BD77",
                              "Pan-blue celebrities" = "#5F84B8",
                              "KMT" = "#263685",
                              "DPP" = "#467046",
                              "NPP" = "#C2AF21",
                              "TPP" = "#56AAB0",
                              "Neutral celebrities" = "#D991B6")) + 
  scale_fill_manual(values = c("Pan-green celebrities" = "#9CF59B",
                               "Pan-blue celebrities" = "#84B7FF",
                               "KMT" = "#4B6BEB",
                               "DPP" = "#80C97F",
                               "NPP" = "#E6CF27",
                               "TPP" = "#71DCD3",
                               "Neutral celebrities" = "#FFABD7")) +
  theme(axis.text.x = element_text(size = 18), 
        axis.text.y = element_text(size = 18),
        axis.title.x = element_text(size = 18),
        axis.title.y = element_text(size = 18),
        legend.title = element_blank(),
        legend.text = element_text(size = 18))
print(p)