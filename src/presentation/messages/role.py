"""Define user-facing message templates for role domain errors."""

MESSAGES: dict[str, str] = {
    "role_not_found": "Role with ID '{role_id}' was not found.",
    "role_already_exists": "Role with name '{role_name}' already exists.",
    "role_already_deleted": "Role with ID '{role_id}' has already been deleted.",
}
