# a-copy-of-chickenglass

This is a copy of chickenglass, I am learning how to implement this project in my undergraduate innovation and entrepreneurship project, the original author of this project is My mentor, if you are interested in the complete project you can click [here](https://github.com/chaoxu/chickenglass)
---

# My current learning situation and understanding of this project (maybe there are something wrong)
1. Function of this project：The current function of this project is to use markdown to write. After writing, a series of .md files can be converted into easy-to-read html files.
2. What I have complete：To be honest, I have some general understanding of this project, but due to limited personal ability, I don't understand it enough. 
What I have done now is mainly the Chicken Markdown Compiler part of the original technology roadmap, that is, converting md files in writing mode into html files in reading mode. The specific understanding of chickenglass.py is in the comments of chickenglass.py.
---
# What I don't understand and I'm going to learn
1. Optimize the HTML (server rendering) of the entire KaTeX output (add some css and html), and I am still using the original content of my teacher
2. File Status Monitoring Module：I know very little about this at the moment, although my teacher said in his blog that it is easy to write (I'm too lacking in basic programming skills)
3. Write a simple meta data service yourself: the information of each block to be collected. Information and cross-citations between each article.（This has not been done yet, I will try to complete the second half of the project study）
---
# How to configure in windows system
   My mentor(also the original author) has already describes how to configure the environment in linux, But I have some difficulties configuring with windows, so I will tell how to configure the environment on windows.
1. Install python editor, pandoc and related libraries.（It should be noted here that we have to turn off the proxy when installing related libraries (especially pandoc), otherwise the installation will fail easily.）
2. Configure the environment variable: Add the environment variable named LUA_PATH in the editing environment variable interface of windows, the variable is ''PATH_TO_CHICKENGLASS/chickenglass/filters/?.lua;;''
---
