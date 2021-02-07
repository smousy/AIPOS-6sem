from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

taskList = ['Task1', 'Task2', 'Task3']

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('tasklist'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            # self.wfile.write(self.path.encode())

            output = ''
            output += '<html><body>'
            output += '<h1>Task List</h1>'
            output += '<h3><a href="/tasklist/new">Add New Task</a></h3>'
            for task in taskList:
                output += task
                output +='<a/ href="/tasklist/%s/remove">X</a>'%task
                output += '</br>'
            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/new'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Add Task</h1>'

            output+='<form method="POST" enctype = "multipart/form-data" action="/tasklist/new">'
            output+='<input name="task" type = "text" placeholders="Add new task">'
            output+='<input type="submit" value="Add">'
            output+='</form>'
            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/remove'):
            listIDPath = self.path.split('/')[2]
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Remove task: %s</h1>' %listIDPath.replace('%20',' ')

            output +='<form method="POST" enctype="multipart/form-data" action="/tasklist/%s/remove">' %listIDPath
            output +='<input type="submit" value = "Remove"></form>'
            output +='<a href = "/tasklist">Cancel</a>'

            output += '</body></html>'
            self.wfile.write(output.encode())


    def do_POST(self):
        if self.path.endswith('/new'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary']= bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype =='multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_task = fields.get('task')
                taskList.append(new_task[0].decode('utf-8'))
            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/tasklist')
            self.end_headers()

        if self.path.endswith('/remove'):
            listIDPath = self.path.split('/')[2]
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype =='multipart/form-data':
                list_item = listIDPath.replace('%20', '')
                taskList.remove(list_item)
            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/tasklist')
            self.end_headers()





def main():
    PORT = 9000
    server = HTTPServer(('',PORT), requestHandler)
    print('Server running on port %s' %PORT)
    server.serve_forever()

if __name__=='__main__':
    main()
