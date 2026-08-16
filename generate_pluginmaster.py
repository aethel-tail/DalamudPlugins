import json
import os
import requests
from time import time
from sys import argv

DOWNLOAD_URL = '{}/releases/download/v{}/latest.zip'
GITHUB_RELEASES_API_URL = 'https://api.github.com/repos/{}/{}/releases/tags/v{}'

DEFAULTS = {
    'IsHide': False,
    'IsTestingExclusive': False,
    'ApplicableVersion': 'any',
}

DUPLICATES = {
    'DownloadLinkInstall': ['DownloadLinkTesting', 'DownloadLinkUpdate'],
}

TRIMMED_KEYS = [
    'Author',
    'Name',
    'Punchline',
    'Description',
    'Changelog',
    'InternalName',
    'AssemblyVersion',
    'RepoUrl',
    'ApplicableVersion',
    'Tags',
    'CategoryTags',
    'DalamudApiLevel',
    'IconUrl',
    'ImageUrls',
]


def main():
    master = extract_manifests()
    master = [trim_manifest(manifest) for manifest in master]
    add_extra_fields(master)
    get_last_updated_times(master)
    write_master(master)


def extract_manifests():
    manifests = []

    for dirpath, dirnames, filenames in os.walk('./plugins'):
        plugin_name = os.path.basename(dirpath)
        if len(filenames) == 0 or f'{plugin_name}.json' not in filenames:
            continue
        with open(os.path.join(dirpath, f'{plugin_name}.json'), 'r', encoding='utf-8') as f:
            manifest = json.load(f)
            manifests.append(manifest)

    return manifests


def add_extra_fields(manifests):
    for manifest in manifests:
        manifest['DownloadLinkInstall'] = DOWNLOAD_URL.format(
            manifest['RepoUrl'], manifest['AssemblyVersion']
        )
        for k, v in DEFAULTS.items():
            if k not in manifest:
                manifest[k] = v
        for source, keys in DUPLICATES.items():
            for k in keys:
                if k not in manifest:
                    manifest[k] = manifest[source]
        owner = extract_owner(manifest['RepoUrl'])
        manifest['DownloadCount'] = get_release_download_count(
            owner, manifest['InternalName'], manifest['AssemblyVersion']
        )


def extract_owner(repo_url):
    """Extract GitHub owner from RepoUrl like https://github.com/owner/repo"""
    parts = repo_url.rstrip('/').split('/')
    if len(parts) >= 2:
        return parts[-2]
    return parts[-1]


def get_release_download_count(owner, repo, version):
    try:
        r = requests.get(GITHUB_RELEASES_API_URL.format(owner, repo, version))
        if r.status_code == 200:
            data = r.json()
            return sum(asset['download_count'] for asset in data.get('assets', []))
    except Exception:
        pass
    return 0


def get_last_updated_times(manifests):
    try:
        with open('pluginmaster.json', 'r', encoding='utf-8') as f:
            previous_manifests = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        previous_manifests = []

    for manifest in manifests:
        manifest['LastUpdate'] = str(int(time()))

        for previous_manifest in previous_manifests:
            if manifest['InternalName'] != previous_manifest['InternalName']:
                continue
            if manifest['AssemblyVersion'] == previous_manifest['AssemblyVersion']:
                manifest['LastUpdate'] = previous_manifest['LastUpdate']
            break


def write_master(master):
    with open('pluginmaster.json', 'w', encoding='utf-8') as f:
        json.dump(master, f, indent=4, ensure_ascii=False)


def trim_manifest(plugin):
    return {k: plugin[k] for k in TRIMMED_KEYS if k in plugin}


if __name__ == '__main__':
    main()
