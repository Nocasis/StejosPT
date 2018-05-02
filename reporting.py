#!/usr/bin/env python3

from jinja2 import Environment, PackageLoader, FileSystemLoader, select_autoescape









if __name__ == "__main__": #Еще ничего не сделано, просто тестил
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    test = env.get_template('test.html')
    print(test)

