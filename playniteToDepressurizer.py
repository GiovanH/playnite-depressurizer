#!/bin/python3

import csv
import argparse
import collections
import xml.etree.ElementTree as ET
import shutil
import os

import typing

def parseCsv(csv_path: str) -> typing.Iterable:
    with open(csv_path, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return filter(lambda d: d['Source'] == 'Steam', list(reader))


def updateProfile(statuses: dict[str, list[str]], profile_path: str) -> None:
    dprofile: ET.ElementTree = ET.parse(profile_path)

    dprofile.getroot().find("auto_import").text = "false"  # type: ignore[union-attr]

    games_tree: ET.Element = dprofile.getroot().find("games")  # type: ignore[assignment]
    for status, game_ids in statuses.items():
        for game_id in game_ids:
            match: ET.Element = games_tree.find(f"game[id='{game_id}']")  # type: ignore[assignment]
            if not match:
                # Create blank game
                match = ET.SubElement(games_tree, 'game')

                matchid = ET.SubElement(match, 'id')
                matchid.text = game_id

                matchname = ET.SubElement(match, 'name')
                matchname.text = "UNKNOWN"

                matchcats = ET.SubElement(match, 'categories')

            print(status, game_id, str(match))

            categories: ET.Element = match.find("categories")  # type: ignore[assignment]
            categories.clear()

            newcat = ET.SubElement(categories, 'category')
            newcat.text = str(status)

    shutil.copy(profile_path, profile_path + ".bak")
    dprofile.write(profile_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csvfile", help="path to CSV output from the playnite advanced library export plugin")
    # parser.add_argument("dprofile")
    args = parser.parse_args()

    statuses = collections.defaultdict(list)
    games = list(parseCsv(args.csvfile))
    for game in games:
        statuses[game['CompletionStatus']].append(game['GameId'])

    print(f"Gathered {len(games)} Steam games with {len(statuses.keys())} completion statuses")

    appdata = os.getenv('APPDATA')
    assert appdata is not None

    profile_path = os.path.join(appdata, 'Depressurizer', 'playnite.profile')

    updateProfile(statuses, profile_path)
