# generate-iconset

Generating an iconset (`.icns`) for Mac OS application. Moved from [this repository](https://github.com/retifrav/python-scripts/tree/master/generate-iconset) to become a PyPI package.

More information in the following [article](https://decovar.dev/blog/2018/10/09/macos-convert-png-to-icns/).

## Requirements

- Python 3.6 or later
- image processing tool
    + [ImageMagick](https://imagemagick.org/)
    + [sips](https://ss64.com/osx/sips.html) (*part of the standard Mac OS utilities*)
- `iconutil` tool (*part of the standard Mac OS utilities*)

## Usage

``` sh
$ python generate-iconset.py /path/to/original/icon.png
```

Resulting (`icon.icns`) will be saved to `/path/to/original/`.

## License

The project is licensed under [GPLv3](./LICENSE). With the project being a tool, it should not be too difficult to comply with the license terms.
