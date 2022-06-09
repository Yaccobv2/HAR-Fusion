"""
Human activity recognition app.
"""
import argparse

from src.data_processor import main_loop

PARSER = argparse.ArgumentParser()

PARSER.add_argument('-cs', '--camera_source', type=int, choices=range(0, 5), default=2, help='Select camera source')

PARSER.add_argument('-m', '--mode', choices=['dataset', 'run'], help='dataset: colect data for dataset, run:'
                                                                     'run live classification ')

PARSER.add_argument('-c', '--class_name', type=str, default="None", nargs='*',
                    help='Set class to save')

PARSER.add_argument('-f', '--frames', type=int, choices=range(1, 40), help='Set number of frames to process before '
                                                                           'saving or running detection')

ARGS = PARSER.parse_args()


def main() -> None:
    """
    Main
    :return: None
    """
    main_loop(camera_source=ARGS.camera_source, mode=ARGS.mode, class_name=ARGS.class_name[0], frames_num=ARGS.frames)


if __name__ == "__main__":
    main()
