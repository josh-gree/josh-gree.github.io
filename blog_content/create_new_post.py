import sys
import os

if len(sys.argv) != 2:
    print("{} arguments: too many arguments!".format(len(sys.argv)-1))
    quit()
else:
    filename = sys.argv[1]
    f = open(filename)
    meta_dat = {}
    text = []
    for ind,l in enumerate(f):
        if ind < 3:
            k = l.split(":")
            meta_dat[k[0].strip()] = k[1].strip()
        else:
            text.append(l.strip())
    f.close()
    
    htmlfilename = "post_" + meta_dat["Date"].replace("/","") + ".html"
    prototype = open("../blog_posts/post_prototype.html","r")
    newpost = open("../blog_posts/"+htmlfilename,"w")
    changes = ["#####","%%%%%","*****","XXXXX"]
    for line in prototype:
        if line.strip() == changes[0]:
            newpost.write("<title>"+meta_dat["Title"]+"</title>\n")
        elif line.strip() == changes[1]:
            if meta_dat["Latex"] == "True":
                newpost.write('<script type="text/javascript" src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">\n')
            else:
                newpost.write("\n")
        elif line.strip() == changes[2]:
            newpost.write("<h1>"+meta_dat["Title"]+"</h1>\n")

        elif line.strip() == changes[3]:
            for line in text:
                if line != '':
                    newpost.write("<p>"+line+"</p>\n")

        else:
            newpost.write(line)
    newpost.close()
    prototype.close()
    
    csv = open("../blog_posts/posts.csv","a")
    csv.write(meta_dat["Date"]+"\t"+ meta_dat["Latex"] +"\t"+ meta_dat["Title"] +"\t"+ htmlfilename +"\n")
    csv.close()
    
    try:
        os.remove("../index.html")
    except OSError:
        pass
    
    prototype = open("../index_prototype.html","r")
    index = open("../index.html","w")
    for line in prototype:
        if line.strip() == "XXXXX":
            index.write("<h1>"+meta_dat["Title"]+"</h1>\n")
            for line in text:
                if line != '':
                    index.write("<p>"+line+"</p>\n")
        else:
            index.write(line)
    prototype.close()
    index.close()
    