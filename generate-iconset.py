import sys
import pathlib
import argparse
import subprocess

# default iconset files extension, gets the value from original image
ext = ".png"


class IconParameters():
    width = 0
    scale = 1

    def __init__(self, width, scale):
        self.width = width
        self.scale = scale

    def getIconName(self):
        global ext
        if self.scale != 1:
            return f"icon_{self.width}x{self.width}{ext}"
        else:
            return f"icon_{self.width//2}x{self.width//2}@2x{ext}"


def generateImageConvertingCommand(forSips, originalPicture, ip, iconsetDir):
    if not forSips:
        return [
            "magick",
            "convert",
            originalPicture,
            "-resize",
            str(ip.width),
            iconsetDir / ip.getIconName()
        ]
    else:
        return [
            "sips",
            "-z",
            str(ip.width),
            str(ip.width),
            originalPicture,
            "--out",
            iconsetDir / ip.getIconName()
        ]


def main():
    global ext
    argParser = argparse.ArgumentParser(description="Generate an iconset.")
    argParser.add_argument(
        "image",
        metavar="/path/image.png",
        help="path to the original image"
    )
    argParser.add_argument(
        "--out",
        metavar="/path/out/",
        help=" ".join((
            "path to the output folder, where to put resulting",
            ".icns file (default: same folder as original image)"
        ))
    )
    argParser.add_argument(
        "--use-sips",
        action='store_true',
        help="use sips instead of ImageMagick (default: %(default)s)"
    )
    argParser.add_argument(
        "--force-png",
        action='store_true',
        help=" ".join((
            "force non-.png original image to be converted",
            "to .png (default: %(default)s)"
        ))
    )
    # argParser.add_argument(
    #     "--delete-tmp-iconset",
    #     action='store_true',
    #     help=" ".join((
    #         "delete temporary iconset directory,",
    #         "if it already exists (default: %(default)s)"
    #     ))
    # )
    cliArgs = argParser.parse_args()
    # print(cliArgs)

    originalPicture = pathlib.Path(cliArgs.image)
    if not (originalPicture.is_file()):
        raise SystemExit(
            f"[ERROR] There is no such image file: {cliArgs.image}"
        )

    print(f"Original image: {originalPicture}")

    if not cliArgs.use_sips:
        print("Will use ImageMagick for converting the original image")
        # check if ImageMagick is available in PATH
        magickCheckResult = subprocess.run(
            ["which", "magick"],
            capture_output=True,
            text=True
        )
        if magickCheckResult.returncode != 0:
            raise SystemExit(
                " ".join((
                    "[ERROR] Couldn't find ImageMagick in your PATH.",
                    "Perhaps, you don't have it installed?"
                ))
            )
        else:
            print(f"Found ImageMagick: {magickCheckResult.stdout.strip()}")
    else:
        print("Will use sips for converting the original image")
        print(
            " ".join((
                "[WARNING] ImageMagick provides better quality results,",
                "so do consider using it instead of sips. More details:",
                "https://decovar.dev/blog/2019/12/12/imagemagick-vs-sips-resize/"
            ))
        )
        # check if sips is available in PATH
        sipsCheckResult = subprocess.run(
            ["which", "sips"],
            capture_output=True,
            text=True
        )
        if sipsCheckResult.returncode != 0:
            raise SystemExit(
                "[ERROR] Couldn't find sips in your PATH"
            )
        else:
            print(f"Found sips: {sipsCheckResult.stdout.strip()}")

    print()

    fname = pathlib.Path(originalPicture).stem
    ext = pathlib.Path(originalPicture).suffix
    if ext != ".png":
        if not cliArgs.force_png:
            print(
                " ".join((
                    "[WARNING] Original image extension is not .png,",
                    "iconutil is likely to fail,",
                    "pass --force-png to avoid that"
                ))
            )
        else:
            ext = ".png"

    # destination path for output
    destDir = (
        pathlib.Path(originalPicture).parent if cliArgs.out is None
        else pathlib.Path(cliArgs.out)
    )
    if not (destDir.is_dir()):
        try:
            destDir.mkdir(parents=True)
        except Exception as ex:
            raise SystemExit(
                " ".join((
                    "[ERROR] The specified output folder doesn't exist",
                    f"and could not be created: {cliArgs.out}"
                ))
            )
    # path to resulting .icns file
    resultingIconset = destDir / f"{fname}.icns"

    # path to temporary iconset folder
    iconsetDir = pathlib.Path(destDir / f"{fname}.iconset")
    if not (iconsetDir.is_dir()):
        try:
            iconsetDir.mkdir()
        except Exception as ex:
            raise SystemExit(
                " ".join((
                    "[ERROR] Could not create temporary",
                    f"iconset folder: {iconsetDir}"
                ))
            )
    else:
        if False:  # cliArgs.delete_tmp_iconset:
            # not the best idea to let script delete files on disk
            print("[DEBUG] Deleting temporary iconset folder")
        else:
            raise SystemExit(
                " ".join((
                    f"[ERROR] Temporary iconset directory ({iconsetDir})",
                    "already exists, you need to",
                    "delete it first"
                    # "either delete it manually",
                    # "or provide --delete-tmp-iconset option"
                ))
            )

    # https://developer.apple.com/design/human-interface-guidelines/macos/icons-and-images/app-icon#app-icon-sizes
    ListOfIconParameters = [
        IconParameters(16, 1),
        IconParameters(16, 2),
        IconParameters(32, 1),
        IconParameters(32, 2),
        IconParameters(64, 1),
        IconParameters(64, 2),
        IconParameters(128, 1),
        IconParameters(128, 2),
        IconParameters(256, 1),
        IconParameters(256, 2),
        IconParameters(512, 1),
        IconParameters(512, 2),
        IconParameters(1024, 1),
        IconParameters(1024, 2)
    ]

    print("Converting images for iconset")

    # generate iconset
    currentImage = 0
    for ip in ListOfIconParameters:
        currentImage += 1
        convertingResult = subprocess.run(
            generateImageConvertingCommand(
                cliArgs.use_sips,
                originalPicture,
                ip,
                iconsetDir
            ),
            capture_output=True,
            text=True
        )
        if convertingResult.returncode != 0:
            raise SystemExit(
                f"[ERROR] Conversion failed. {convertingResult.stderr.strip()}"
            )
        else:
            print(f"{currentImage}/{len(ListOfIconParameters)}...")
        # print(f"Generated {ip.getIconName()}")

    print("\nGenerating .icns file...")
    # convert iconset folder to .icns file
    iconutilResult = subprocess.run(
        [
            "iconutil",
            "-c",
            "icns",
            iconsetDir,
            "-o",
            resultingIconset
        ],
        capture_output=True,
        text=True
    )
    if iconutilResult.returncode != 0:
        raise SystemExit(
            " ".join((
                "[ERROR] iconutil could not generate",
                f"an iconset. {iconutilResult.stderr.strip()}"
            ))
        )
    else:
        print(
            " ".join((
                "[SUCCESS] An iconset was successfully",
                f"generated to {resultingIconset}"
            ))
        )
        raise SystemExit(0)


if __name__ == '__main__':
    main()
