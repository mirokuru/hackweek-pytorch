from my_aws_functions import *

import sys
import argparse


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def handle_versions(new_version):
    if not check_for_model(new_version):
        print(f'Requested version {new_version} not found yet as expected')
        previous_version = new_version - 1
        if check_for_model(previous_version):
            print(f'Previous version {previous_version} found as expected')
            # download_model(previous_version)
        else:
            print(f'Version {previous_version} not found! Cannot continue!')
            sys.exit()
    else:
        print(f'Version {new_version} already found! Will not continue!')
        sys.exit()


def retrieve_model():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', type=int, required=True)
    args = parser.parse_args()
    print(f'Requested version is {args.version}...')
    handle_versions(args.version)


def main():
    retrieve_model()


if __name__ == "__main__":
    main()
