# coding: utf-8


from the_tale.game.artifacts.prototypes import ArtifactPrototype

from the_tale.game.heroes.relations import EQUIPMENT_SLOT


class EquipmentException(Exception): pass

class Bag(object):

    __init__ = ('next_uuid', 'updated', 'bag')

    def __init__(self):
        self.next_uuid = 0
        self.updated = True
        self.bag = {}

    def deserialize(self, data):
        # return
        self.next_uuid = data.get('next_uuid', 0)
        self.bag = {}
        for uuid, artifact_data in data.get('bag', {}).items():
            artifact = ArtifactPrototype.deserialize(artifact_data)
            self.bag[int(uuid)] = artifact

    def serialize(self):
        return { 'next_uuid': self.next_uuid,
                 'bag': dict( (uuid, artifact.serialize()) for uuid, artifact in self.bag.items() )  }

    def ui_info(self):
        return dict( (int(uuid), artifact.ui_info()) for uuid, artifact in self.bag.items() )

    def put_artifact(self, artifact):
        self.updated = True
        uuid = self.next_uuid
        self.bag[uuid] = artifact
        artifact.set_bag_uuid(uuid)
        self.next_uuid += 1

    def pop_artifact(self, artifact):
        self.updated = True
        del self.bag[artifact.bag_uuid]

    def get(self, artifact_id):
        return self.bag.get(artifact_id, None)

    def items(self):
        return self.bag.items()

    def values(self):
        return self.bag.values()

    @property
    def is_empty(self):
        return not self.bag

    @property
    def occupation(self): return len(self.bag)

    @classmethod
    def _compare_drop(cls, a, b):
        if a is None:
            return True
        elif b is None:
            return False
        elif a.type.is_USELESS:
            if b.type.is_USELESS:
                return a.absolute_sell_price() > b.absolute_sell_price()
            else:
                return False

        else:
            if b.type.is_USELESS:
                return True
            else:
                return a.power > b.power

    def drop_cheapest_item(self):

        dropped_item = None

        for item in self.bag.values():
            if self._compare_drop(dropped_item, item):
                dropped_item = item

        if dropped_item is not None:
            self.pop_artifact(dropped_item)

        return dropped_item

    def __eq__(self, other):
        return (self.next_uuid == other.next_uuid and
                self.bag == other.bag)


####################################################
# Equipment
####################################################

class Equipment(object):

    __slots__ = ('equipment', 'updated')

    def __init__(self):
        self.equipment = {}
        self.updated = True

    def get_power(self):
        power = 0
        for slot in EQUIPMENT_SLOT.records:
            artifact = self.get(slot)
            if artifact:
                power += artifact.power
        return power

    def ui_info(self):
        return dict( (slot, artifact.ui_info()) for slot, artifact in self.equipment.items() if artifact )

    def serialize(self):
        return dict( (slot, artifact.serialize()) for slot, artifact in self.equipment.items() if artifact )

    def deserialize(self, data):
        self.equipment = dict( (int(slot), ArtifactPrototype.deserialize(artifact_data)) for slot, artifact_data in data.items() if  artifact_data)

    def unequip(self, slot):
        if slot.value not in self.equipment:
            return None
        self.updated = True
        artifact = self.equipment[slot.value]
        del self.equipment[slot.value]
        return artifact

    def equip(self, slot, artifact):
        if slot.value in self.equipment:
            raise EquipmentException('slot for equipment has already busy')
        if slot not in EQUIPMENT_SLOT.records:
            raise EquipmentException('unknown slot id: %s' % slot)

        self.updated = True
        self.equipment[slot.value] = artifact

    def get(self, slot):
        return self.equipment.get(slot.value, None)

    def _remove_all(self):
        for slot in EQUIPMENT_SLOT.records:
            self.unequip(slot)
        self.updated = True

    def test_equip_in_all_slots(self, artifact):
        for slot in EQUIPMENT_SLOT.records:
            if self.get(slot) is not None:
                self.unequip(slot)
            self.equip(slot, artifact)
        self.updated = True

    def __eq__(self, other):
        return (self.equipment == other.equipment)
