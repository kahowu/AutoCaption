import os
import webbrowser
import numpy as np

class pyNumpyViewer():
    '''
    opens the webbrower to view numpy arrays
    '''
    def __init__(self, data):
        self.checkData(data)
        html = self.generateHTML(data)

        path = os.path.abspath('temp.html')
        with open(path, 'w') as f:
            f.write(html)
        url = 'file://' + path
        webbrowser.open(url)

    def checkData(self, data):
        if data.ndim > 2:
            raise "Can't display more than 2d arrays"

    def generateHTML(self, data):
        '''
        generates html string with table data embedded in. 
        '''
        html = '<!DOCTYPE html><html>' + self.getHeader() + self.getBody(data) + '</html>'
        return html

    def getHeader(self):
        header = '<head><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"></head>' 
        return header

    def getBody(self, data):
        body_string = '<div class="container"><div class="table-responsive"><table class="table">' + self.getTableHeader(data) + self.getTableBody(data) + '</table></div></div>'
        body_string += '<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script><script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script></body>'
        return body_string

    def getTableHeader(self, data):
        if data.ndim == 2:
            no_col = data.shape[1]
        else:
            no_col = 1
        table_header_string = '<thead><tr><th>#</th>'
        for cols in range(0, no_col):
            table_header_string += '<th> Col: ' + str(cols) + '</th>'
        return table_header_string + '</tr></thead>'

    def getTableBody(self, data):
        if data.ndim == 1:
            no_row = data.shape[0]
            no_col = 0
        else:
            no_row, no_col = data.shape
            
        table_body_string = '<tbody>'
        for row in range(0, no_row):
            table_body_string += '<tr>'
            table_body_string += '<td>' + str(row) + '</td>' # display the index
            if no_col == 0: # display the data for 1D array
                table_body_string += '<td>' + str(np.around(data[row], 1)) + '</td>'
            for col in range(0, no_col): #display the data for 2D array
                table_body_string += '<td>' + str(np.around(data[row][col], 1)) + '</td>'
            table_body_string += '</tr>'
        table_body_string += '</tbody>'
        return table_body_string








