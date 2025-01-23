"Base Entity for GryfSmart"

from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import _GryfSmartCoordinator

class _GryfSmartEntity(CoordinatorEntity[_GryfSmartCoordinator]):
    """Commmon GryfSmart Entity using CoordinatorEntity"""

    _attr_has_entity_name - True

    def __init__(
        self,
        coordinator: _GryfSmartCoordinator,
                 ) -> None:
        pass
