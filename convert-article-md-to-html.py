import argparse
import markdown
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Convert article.md to article.html.')
    parser.add_argument(
        'path',
        action='store',
        type=Path,
        help='path to the directory with the .md')
    parser.add_argument(
        '-a',
        '--addclasses',
        action='store_true',
        help='whether or not to add predefined classes when converting from .md to .html. False by default (without this option)')
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

def clean_up_html(html):
    lines = html.split('\n')
    html_cleaned_up = lines[0]
    for line in lines[1:]:
        if line[:4] in ['<h1>', '<h2>', '<h3>', '<h4>', '<h5>', '<h6>']:
            line = '\n' + line
        elif line == '<p><br></p>':
            line = '<br>'
        elif line[:4] == '<li>':
            line = '\t' + line
        elif line[:12] == '<p><img src=' and line[-4:] == '</p>':
            line = line[3:-4]
        html_cleaned_up += '\n' + line
    return html_cleaned_up

def add_classes_to_html(html):
    lines = html.split('\n')
    line_0_with_class = lines[0][:3] + ' class="short-margin-bottom"' + lines[0][3:]
    line_1_with_class = lines[1][:2] + ' class="subtle"' + lines[1][2:]
    html_with_classes = line_0_with_class + '\n' + line_1_with_class
    for line in lines[2:]:
        html_with_classes += '\n' + line
    return html_with_classes

def check_for_write_authorization():
    confirmation = input('Perform write? This is destructive if there is an existing article.html. [y/n]\n')
    if not confirmation.lower() in ['y', 'ye', 'yes']:
        raise Exception('User did not authorize write. Action canceled.')

def write_to_html(path, html):
    html_path = path / 'article.html'
    with open(html_path, 'r+') as file:
        file.seek(0)
        file.write(html)
        file.truncate()
    print('Write completed.')

def main():
    arguments = parse_arguments()
    path = arguments['path']
    check_if_argument_is_a_directory(path)
    md_path = get_md_path(path)
    html = convert_md_to_html(md_path)
    html = clean_up_html(html)
    add_classes = arguments['addclasses']
    if add_classes:
        html = add_classes_to_html(html)
    check_for_write_authorization()
    write_to_html(path, html)

if __name__ == '__main__':
    main()
