master_doc = "index"  # for Sphinx <2.0
extensions = [
    "sphinx_example_index"
]
exclude_patterns = ["_build", "_includes"]
suppress_warnings = ["app.add_directive", "app.add_node"]
default_role = "obj"
templates_path = ["_templates"]
