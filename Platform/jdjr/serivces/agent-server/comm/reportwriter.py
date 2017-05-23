# -*- coding: utf-8 -*-
#
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#  
#  This file is part of Multi-Mechanize
#


class Report(object):
    def __init__(self, results_dir):
        self.results_dir = results_dir
        self.fn = results_dir + '.html'
        self.write_head_html()

    
    def write_line(self, line):
        with open(self.fn, 'a') as f:
            f.write('%s\n' % line)


    def write_head_html(self):
        with open(self.fn, 'w') as f:
            f.write("""\
        <!DOCTYPE html>
        <html>
            <head>
	            <meta charset="utf-8">
	            <title>研发 - 测试部 - 移动端测试报告</title>
	            <link rel="stylesheet" href="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/css/bootstrap.min.css">
	            <script src="http://cdn.static.runoob.com/libs/jquery/2.1.1/jquery.min.js"></script>
	            <script src="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/js/bootstrap.min.js"></script>
            </head>
            <body>""")
  

    def write_closing_html(self):
        with open(self.fn, 'a') as f:
            f.write("""\
</body>
</html>
""")





