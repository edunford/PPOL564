# Slack logo Icon for class 

require(tidyverse)

lab_dat <- 
  tibble(x = 0,
         y = 0,
         label = 'DS1')

set.seed(1234)
N = 10000
ds1_icon <- 
  tibble(x = rnorm(N,sd=1),
         y = rnorm(N,sd=1)) %>% 
  ggplot(aes(x,y)) +
  geom_hex(show.legend = F) +
  # scico::scale_fill_scico(palette = "vik") +
  scale_fill_viridis_c() +
  geom_text(data=lab_dat,aes(x,y,label=label),size=100,inherit.aes = F,
            color="white",family="serif") +
  theme_void()

# Export
ggsave("syllabus/slack_icon.png",ds1_icon,width = 10,height=10)
