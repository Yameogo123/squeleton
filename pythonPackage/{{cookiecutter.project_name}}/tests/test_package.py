import {{ cookiecutter.package_slug }}


def test_package_is_importable():
    assert {{ cookiecutter.package_slug }}.__version__
