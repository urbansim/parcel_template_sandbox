import orca
import pandana as pdna

from urbansim.utils import networks


@orca.step('build_networks')
def build_networks(parcels, net_store):
    st = net_store
    nodes, edges = st.nodes, st.edges
    net = pdna.Network(nodes["x"], nodes["y"], edges["from"], edges["to"],
                       edges[["weight"]])
    net.precompute(3000)
    orca.add_injectable("net", net)

    p = parcels.to_frame(parcels.local_columns)
    p['node_id'] = net.get_node_ids(p['x'], p['y'])
    orca.add_table("parcels", p)


@orca.step('neighborhood_vars')
def neighborhood_vars(net):
    nodes = networks.from_yaml(net, "legacy_neighborhood_vars.yaml")
    nodes = nodes.fillna(0)
    print(nodes.describe())
    orca.add_table("nodes", nodes)


