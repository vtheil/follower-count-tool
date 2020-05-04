#!/usr/bin/env python3
import argparse

from follower_count import instagram

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Follower Count Tool is a tool that looks up Instagram profile information for a requested user."
    )

    parser.add_argument('--username', '-u', 
        required=True,
        help="The Instagram username to look up"
    )

    args = parser.parse_args()

    instagram.print_influence(args.username)
