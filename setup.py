import setuptools

setuptools.setup(
    name="amtronwallbox",
    version="0.1.0",
    description="Mennekes Amtron Wallbox Xtra/Premium",
    long_description='Read and control your Mennekes Amtron Wallbox Xtra/Premium using the modbus TCP server',
    url="https://github.com/dr-waterstorm/MennekesAmtronWallbox",
    author="dr-waterstorm",
    author_email="waterstorm@acc-clan.com",
    license="MIT",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    zip_safe=False,
    python_requires='>=3.9',
    install_requires=[
        "pymodbus",
    ],
)
