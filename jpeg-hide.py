#!/usr/bin/env python

import sys
from rich.console import Console

console = Console()

def main():
    if len(sys.argv) <= 1:
        show_usage()

    command = sys.argv[1]
    if (len(command) <= 0) or (command not in ['--clear', '-c', '--write', '-w', '--read', '-r', '--about', '--help']):
        show_usage()

    if command not in ['--about', '--help']:
        try:
            image_path = sys.argv[2]
        except:
            printError('Error: no image path.')

        if len(image_path) <= 0:
            printError('Error: no image path.')

    if command == '--clear' or command == '-c':
        clear_image(image_path)
        printSuccess('Image cleared.')
    elif command == '--write' or command == '-w':
        try:
            text_to_write = sys.argv[3]
        except:
            printError('Error: no text to write.')
        
        if len(text_to_write) <= 0:
            printError('Error: no text to write.')

        clear_image(image_path)
        write_to_image(image_path, text_to_write)
        printSuccess("Wrote: " + read_from_image(image_path))
    elif command == '--read' or command == '-r':
        console.print(read_from_image(image_path))
    elif command == '--about':
        show_about()
    else:
        show_usage()


def printSuccess(text):
    console.print(f"✓ {text}", style="bold green")


def printError(text):
    console.print(text, style="bold red")
    sys.exit()


def show_about():
    console.print('[bold]Created by Carlos E. Torres (cetorres@cetorres.com)[/bold]')
    sys.exit()


def show_usage():    
    console.print('[bold]Usage: jpeg-hide [OPTIONS][/bold]\n')
    console.print('  [bold]Program to hide text into JPEG images.[/bold]\n')
    console.print('[bold]Options:[/bold]')
    console.print('  -c, --clear IMAGE_PATH       Clear the text in a image')
    console.print('  -w, --write IMAGE_PATH TEXT  Write text to an image')
    console.print('  -r, --read IMAGE_PATH        Read text from an image')
    console.print('  --about                      Show about info')
    console.print('  --help                       Show this message')
    sys.exit()


def write_to_image(image_path, text):
    try:
        with open(image_path, 'ab') as f:
            f.write(text.encode('utf-8'))
    except FileNotFoundError:
        printError('Error: file not found.')
    except:
        printError('Error: could not write image.')


def clear_image(image_path):
    try:
        with open(image_path, 'rb+') as f:
            content = f.read()
            offset = content.index(bytes.fromhex('FFD9'))
            f.seek(offset + 2)        
            f.truncate()
    except FileNotFoundError:
        printError('Error: file not found.')
    except:
        printError('Error: could not clear image.')


def read_from_image(image_path):
    try:
        with open(image_path, 'rb') as f:
            content = f.read()
            offset = content.index(bytes.fromhex('FFD9'))
            f.seek(offset + 2)
            text = f.read()
            return text.decode('utf-8')
    except FileNotFoundError:
        printError('Error: file not found.')
    except:
        printError('Error: could not read image.')


if __name__ == "__main__":
    main()
