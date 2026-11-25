"""Report the presence of license metadata in CycloneDX JSON component entries."""


VERSIONS = ("1.5", "1.6", "1.7")
PLACEHOLDERS = {"NONE", "NOASSERTION", "UNKNOWN", "UNLICENSED"}


def _license_values(values, path):
    if not isinstance(values, list):
        raise ValueError(f"{path}.licenses must be an array")
    result = []
    for index, selection in enumerate(values):
        if not isinstance(selection, dict):
            raise ValueError(f"{path}.licenses[{index}] must be an object")
        if "expression" in selection and "license" not in selection and len(values) == 1:
            value = selection["expression"]
        elif "expression" not in selection and isinstance(selection.get("license"), dict):
            license_ = selection["license"]
            value = license_.get("id") if "id" in license_ else license_.get("name")
        else:
            raise ValueError(f"{path}.licenses[{index}] has an unsupported license choice")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{path}.licenses[{index}] contains no usable text")
        result.append(value.strip())
    return sorted(set(result))


def _entries(components, path):
    if not isinstance(components, list):
        raise ValueError(f"{path} must be an array")
    return [(node, f"{path}[{index}]") for index, node in enumerate(components)]


def audit(document, include_root=False):
    if not isinstance(document, dict) or document.get("bomFormat") != "CycloneDX":
        raise ValueError("expected a CycloneDX JSON document")
    if document.get("specVersion") not in VERSIONS:
        raise ValueError("supported CycloneDX versions are 1.5, 1.6, and 1.7")
    pending = list(reversed(_entries(document.get("components", []), "components")))
    if include_root:
        metadata = document.get("metadata", {})
        if not isinstance(metadata, dict):
            raise ValueError("metadata must be an object")
        if "component" in metadata:
            pending.append((metadata["component"], "metadata.component"))

    rows = []
    while pending:
        component, path = pending.pop()
        if not isinstance(component, dict) or not isinstance(component.get("name"), str) or not component["name"].strip():
            raise ValueError(f"{path} must have a component name")
        licenses = _license_values(component.get("licenses", []), path)
        substantive = [value for value in licenses if value.upper() not in PLACEHOLDERS]
        status = "recorded" if substantive else "placeholder" if licenses else "missing"
        rows.append({"path": path, "name": component["name"], "status": status, "licenses": licenses})
        children = _entries(component.get("components", []), f"{path}.components")
        pending.extend(reversed(children))
    return rows
