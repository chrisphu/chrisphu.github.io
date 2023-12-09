import argparse
import markdown
from pathlib import Path
import re

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='convert-article-md-to-html',
        description='Convert article.md to article.html.')
    parser.add_argument(
        '-p',
        '--path',
        nargs=1,
        required=True,
        type=Path)
    args = parser.parse_args()
    return vars(args)

def check_if_argument_is_a_directory(path):
    if not path.is_dir():
        raise Exception('Argument is not a directory path.')

def get_md_path(path):
    md_path = path / 'article.md'
    if not md_path.is_file():
        raise Exception('article.md does not exist at the provided path.')
    return md_path

def convert_md_to_html(path):
    with open(path, 'r') as file:
        text = file.read()
        html = markdown.markdown(text)
    return html

def add_classes_to_html(html):
    lines = html.split('\n')
    line_0_with_class = lines[0][:3] + ' class="short-margin-bottom"' + lines[0][3:]
    line_1_with_class = lines[1][:2] + ' class="subtle"' + lines[1][2:]
    html_with_classes = line_0_with_class + '\n' + line_1_with_class
    for line in lines[2:]:
        if line == '<p><br></p>':
            line = '<br>'
        html_with_classes += '\n' + line
    return html_with_classes

def write_to_html(path, html):
    html_path = path / 'article.html'
    with open(html_path, 'r+') as file:
        file.seek(0)
        file.write(html)
        file.truncate()

def main():
    arguments = parse_arguments()
    path = arguments['path'][0]
    check_if_argument_is_a_directory(path)
    md_path = get_md_path(path)
    html = convert_md_to_html(md_path)
    html_with_classes = add_classes_to_html(html)
    confirmation = input('Perform write? This is destructive if there is an existing article.html. [y/n]\n')
    if not confirmation.lower() in ['y', 'ye', 'yes']:
        print('Action canceled.')
        return
    write_to_html(path, html_with_classes)
    print('Write completed.')

if __name__ == '__main__':
    main()
