import os

import orca
import pandas as pd
import yaml

from urbansim.utils import misc


#####################
# INJECTABLES
#####################


@orca.injectable('settings', cache=True)
def settings():
    with open(os.path.join(misc.configs_dir(), "settings.yaml")) as f:
        settings = yaml.load(f)
        orca.settings = settings
        return settings


@orca.injectable('store', cache=True)
def hdfstore(settings):
    return pd.HDFStore(
        os.path.join(misc.data_dir(), settings["store"]),
        mode='r')


@orca.injectable('net_store', cache=True)
def net_store(settings):
    return pd.HDFStore(
        os.path.join(misc.data_dir(), settings["net_store"]),
        mode='r')


#####################
# TABLES
#####################


@orca.table('households', cache=True)
def households(store):
    df = store['households']
    df = df[df.building_id > 0]

    p = store['parcels']
    b = store['buildings']
    b['luz'] = misc.reindex(p.luz_id, b.parcel_id)
    df['base_luz'] = misc.reindex(b.luz, df.building_id)
    df['segmentation_col'] = 1

    return df


@orca.table('buildings', cache=True)
def buildings(store):
    df = store['assessor_transactions']
    df["index"] = df.index
    df.drop_duplicates(subset='index', keep='last', inplace=True)
    del df["index"]
    df.index.name = 'building_id'
    return df


@orca.table('parcels', cache=True)
def parcels(store):
    df = store['parcels']
    df['acres'] = df.parcel_acres

    # Delete duplicate index (parcel_id)
    df['rownum'] = df.index
    df = df.drop_duplicates(subset='rownum', keep='last')
    del df['rownum']

    return df


@orca.table('jobs', cache=True)
def jobs(store):
    df = store['jobs']
    df = df[df.building_id > 0]
    return df


#####################
# BROADCASTS
#####################


orca.broadcast('parcels', 'buildings', cast_index=True, onto_on='parcel_id')
orca.broadcast('buildings', 'households', cast_index=True, onto_on='building_id')
orca.broadcast('buildings', 'jobs', cast_index=True, onto_on='building_id')
orca.broadcast('nodes', 'buildings', cast_index=True, onto_on='node_id')


#####################
# VIRTUAL COLUMNS
#####################


@orca.column('households', 'node_id', cache=True)
def node_id(households, buildings):
    return misc.reindex(buildings.node_id, households.building_id)


@orca.column('buildings', 'node_id', cache=True)
def node_id(buildings, parcels):
    return misc.reindex(parcels.node_id, buildings.parcel_id)


@orca.column('jobs', 'node_id', cache=True)
def node_id(jobs, buildings):
    return misc.reindex(buildings.node_id, jobs.building_id)
