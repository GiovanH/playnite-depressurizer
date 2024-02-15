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

    setting_import: typing.Optional[ET.Element] = dprofile.getroot().find("auto_import")
    if not isinstance(setting_import, ET.Element):
        raise ValueError("Profile missing 'auto_import' setting")
    setting_import.text = "false"

    games_tree: typing.Optional[ET.Element] = dprofile.getroot().find("games") 
    if not isinstance(games_tree, ET.ElementTree):
        raise ValueError("Profile missing 'games' list")

    for status, game_ids in statuses.items():
        for game_id in game_ids:
            match: typing.Optional[ET.Element] = games_tree.find(f"game[id='{game_id}']")
            if not match:
                # Create blank game
                match = ET.SubElement(games_tree, 'game')

                matchid = ET.SubElement(match, 'id')
                matchid.text = game_id

                matchname = ET.SubElement(match, 'name')
                matchname.text = "UNKNOWN"

                matchcats = ET.SubElement(match, 'categories')

            assert isinstance(match, ET.ElementTree)
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

    profile_path: str = os.path.join(appdata, 'Depressurizer', 'playnite.profile')

    updateProfile(statuses, profile_path)
