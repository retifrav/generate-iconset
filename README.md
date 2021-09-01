# generate-iconset

Generating an iconset (`.icns`) for using as an application icon on Mac OS.

The tool converts an original image into several sizes to form an iconset, which is then converted into `.icns` file with `iconutil` tool. More information in the following [article](https://decovar.dev/blog/2018/10/09/macos-convert-png-to-icns/).

Moved from [this repository](https://github.com/retifrav/python-scripts/tree/master/generate-iconset) to become a [PyPI package](https://pypi.org/project/generate-iconset/).

## Requirements

- Python 3.7 or later
- image processing tool (*either of*)
    + [ImageMagick](https://imagemagick.org/) (*recommended*)
    + `sips` (*part of the standard Mac OS utilities*)
- `iconutil` tool (*part of the standard Mac OS utilities*)

## Usage

Below examples assume that you installed the tool from PyPI to use it as a standalone executable. Otherwise you'll need to run it as a regular Python script.

Built-in help:

``` sh
$ generate-iconset --help
```

### Basic example

``` sh
$ generate-iconset /path/to/original/icon.png
```

- will fail to run if it's not Mac OS
- will use ImageMagick for converting
- will not force conversion to `.png`, if original image is not `.png`
- resulting `.icns` will be saved to `/path/to/original/icon.icns`
