import os

import orca
import pandas as pd
import yaml

from urbansim.utils import misc


@orca.injectable('net_store', cache=True)
def net_store(settings):
    return pd.HDFStore(
        os.path.join(misc.data_dir(), settings["net_store"]),
        mode='r')


@orca.table('parcels', cache=True)
def parcels(store):
    df = store['parcels']
    df['acres'] = df.parcel_acres

    # Delete duplicate index (parcel_id)
    df['rownum'] = df.index
    df = df.drop_duplicates(subset='rownum', keep='last')
    del df['rownum']

    return df


@orca.injectable('settings', cache=True)
def settings():
    with open(os.path.join(misc.configs_dir(), "settings.yaml")) as f:
        settings = yaml.load(f)
        # monkey patch on the settings object since it's pretty global
        # but will also be available as injectable
        orca.settings = settings
        return settings


@orca.injectable('store', cache=True)
def hdfstore(settings):
    return pd.HDFStore(
        os.path.join(misc.data_dir(), settings["store"]),
        mode='r')


