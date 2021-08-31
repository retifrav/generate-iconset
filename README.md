# generate-iconset

Generating an iconset (`.icns`) for Mac OS application. Moved from [this repository](https://github.com/retifrav/python-scripts/tree/master/generate-iconset) to become a PyPI package.

More information in the following [article](https://decovar.dev/blog/2018/10/09/macos-convert-png-to-icns/).

<!-- MarkdownTOC -->

- [Requirements](#requirements)
- [Usage](#usage)
    - [Simple example](#simple-example)
- [License](#license)

<!-- /MarkdownTOC -->

## Requirements

- Python 3.7 or later
- image processing tool (*either of*)
    + [ImageMagick](https://imagemagick.org/) (*recommended*)
    + `sips` (*part of the standard Mac OS utilities*)
- `iconutil` tool (*part of the standard Mac OS utilities*)

## Usage

Built-in help:

``` sh
$ python generate-iconset.py --help
```

### Simple example

``` sh
$ python generate-iconset.py /path/to/original/icon.png
```

- will fail to run if it's not Mac OS
- will use ImageMagick for converting
- will not force conversion to `.png`, if original image is not `.png`
- resulting `.icns` will be saved to `/path/to/original/icon.icns`

## License

The project is licensed under [GPLv3](./LICENSE). With the project being a tool, it should not be too difficult to comply with the license terms.
