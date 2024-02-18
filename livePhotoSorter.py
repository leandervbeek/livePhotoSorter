import argparse
from os import path, listdir, rename, makedirs, remove

version = 0.1

# Setup the argument parsing
parser = argparse.ArgumentParser(
    description='livePhotoSorter help page. This script helps sort live photos made on an iPhone from the rest of the '
                'image library. The distinction between regular videos and live photos is based on the filename '
                'without considering the extension.',
    epilog=f'livePhotoSorter v{version}'
)

parser.add_argument('-d', '--delete', help='Deletes the live photos', action="store_true")
parser.add_argument('-v', '--verbose', help='Print all operations to the terminal.', action="store_true")
parser.add_argument('-f', '--force', help='Do not confirm deletion', action="store_true")
parser.add_argument('--path', type=str, metavar='PATH', help='Path to sort live photos if not current one.', default='.')
parser.add_argument('--dest', type=str, metavar="DESTINATION", default="live_photos", help="Directory to move the live photos to.")
parser.add_argument('--prefix', type=str,  help="Add a prefix to the live photo filename.")

args = parser.parse_args()

def main(args):
    """
    Main loop
    :param args: Command line arguments
    :return: None
    """

    # Determine the directory to sort the live photos from
    sort_dir = path.abspath(args.path)
    # Check if the path exists, crash if it doesn't
    if not path.exists(sort_dir):
        raise FileNotFoundError(f"The specified path {path} does not exist!")

    log(f"Sorting live photos for {sort_dir}")
    
    # Determine the directory to move the photos to
    dest = path.abspath(args.dest)

    # Find all live photos in the directory
    live_photos = get_live_photos(sort_dir)
    if len(live_photos) == 0:
        log("No live photos found! Exiting...")
        return

    vlog(f"Detected live photos: {live_photos}")

    # Delete files if requested
    if args.delete:
        if not args.force:
            user_is_sure = input("Are you sure about deleting files? (y/N): ")
            if user_is_sure.lower() == 'y':
                user_is_sure = True
        else:
            user_is_sure = True

        if user_is_sure:
            # User is sure

            delete_live_photos(live_photos, sort_dir)
            log("Done deleting files")

            # Nothing more to do here
            return

    # Move the photos to their new directory
    vlog(f"Moving live photos to {dest}")
    move_live_photos(live_photos, sort_dir, dest)

    log("Done!")

def get_live_photos(sort_dir):
    """
    method get_live_photos
    :param sort_dir: Directory to search for the photos in.
    :return live_photos: list of live photos
    """

    # Get all file names in the provided directory
    all_files = [file for file in listdir(sort_dir) if path.isfile(path.join(sort_dir, file))]
    all_files_lower = [file.lower() for file in all_files]

    live_photos = []
    for file in all_files:
        # Iterate over al files

        if file[-4:].lower() == ".mov":
            # Check if the file is a movie file (live photo extension)

            # Match the .mov file to pictures in one of the following formats
            possible_exts = ['.png', '.jpg', '.jpeg', '.heic']
            possible_photos = [file[:-4] + ext for ext in possible_exts]

            if any(photo.lower() in all_files_lower for photo in possible_photos):
                # If any photo exists with the same filename

                log(f"Live photo found: {file}")
                live_photos.append(file)

    return live_photos

def move_live_photos(live_photos, source, dest):
    """
    method move_live_photos
    :param live_photos: Pictures to move
    :parama source: Where to find the pictures
    :param dest: Where to move the pictures to
    :return: None
    """

    # Check if the destination exists, otherwise create it
    if not path.exists(dest):
        makedirs(dest)

    for f in live_photos:
        # Set the source path
        f_source = path.join(source, f)

        # Set the destination path
        if args.prefix != None:
            prefix = str(args.prefix)
            f_dest = path.join(dest, prefix + f)
        else:
            f_dest = path.join(dest, f)

        vlog(f"Moving {f} to {f_dest}")
        rename(f_source, f_dest)

def delete_live_photos(live_photos, source):
    """
    method delete_live_photos
    :param live_photos: Live photos to delete
    :param source: Location of live photos
    :return: None
    """

    for f in live_photos:
        f_source = path.join(source, f)

        vlog(f"Deleting {f_source}")
        remove(f_source)

def vlog(msg):
    """
    method vlog
    Prints a message to the terminal if verbose mode is enabled
    :param msg: Message to print
    :return: None
    """

    if args.verbose:
        log(msg)

def log(msg):
    """
    method log
    Prints a message to the terminal
    :param msg: Message to print
    :return: None
    """

    print(msg)

main(args)