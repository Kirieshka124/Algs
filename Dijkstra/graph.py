import osmnx as ox

# Загружаем дорожный граф для Парижа
G = ox.graph_from_place('Paris, France', network_type='drive')
ox.save_graphml(G, 'Paris_road_network.graphml')
