from . import *


class NChildCollector:
    def __init__(
            self
    ) -> None:
        super(NChildCollector, self).__init__()
        self.child = []

    def add_child(self, child: any) -> None:
        if not hasattr(child, 'z_order'):
            child.z_order = 0
        return self.add_child_sorted(child, child.z_order)

    def add_child_sorted(self, child: any, z_order: int) -> None:
        self.child.append(child)
        if len(self.child) <= 0:
            return
        self.sort()

    def remove_child(self, child: any) -> None:
        self.child.remove(child)

    def has_child(self, child: any) -> bool:
        return self.child.count(child) >= 1

    def find_by_tag(self, tag: str) -> tuple:
        return tuple(_x for _x in self.child[::-1] if _x.tag == tag)

    def find_by_id(self, _id: str) -> any:
        for child in self.child[::-1]:
            if child.id == _id:
                return child
        return None

    def sort(self) -> None:
        self.child.sort(key=lambda x: x.z_order, reverse=False)

    def get_child(self) -> list:
        return self.child

    def export_child(self) -> tuple:
        return tuple(self.child)

    def import_child(self, child: tuple) -> None:
        self.child = list(child)

    def clear(self) -> None:
        self.child.clear()
