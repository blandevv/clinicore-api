"""Define the resources that can be protected by permissions."""

from enum import StrEnum


class PermissionResource(StrEnum):
    """Represent a domain resource that can be subject to permissions."""

    USER = "user"
    ROLE = "role"
    PERMISSION = "permission"
    PATIENT = "patient"
    NURSE = "nurse"
    DOCTOR = "doctor"
    SPECIALTY = "specialty"
    APPOINTMENT = "appointment"
    SURGERY = "surgery"
    SURGERY_RESOURCE = "surgery_resource"
    OPERATING_ROOM = "operating_room"
