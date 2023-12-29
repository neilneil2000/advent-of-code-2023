from typing import Dict, Set


class SnowMachine:
    def __init__(self, data):
        self.topology = self.__process_data(data)

    def __process_data(self, data):
        topology = {}
        for left, rights in data.items():
            rights = set(rights)
            if left in topology:
                topology[left].update(rights)
            else:
                topology[left] = set(rights)
            for right in rights:
                if right in topology:
                    topology[right].add(left)
                else:
                    topology[right] = {left}

        return topology

    def count_chunks(self, topology: dict = None):
        """Return number of discrete chunks in topology"""
        if topology is None:
            topology = self.topology
        components = set(topology.keys())
        counter = 0
        while components:
            self.remove_connected(components, list(components)[0], topology)
            counter += 1
        return counter

    def remove_connected(self, components: Set, component: str, topology: Dict = None):
        """Remove all connected components from components set"""
        if component not in components:
            return
        if topology is None:
            topology = self.topology
        components.discard(component)
        for next_component in self.topology[component]:
            self.remove_connected(components, next_component, topology)
