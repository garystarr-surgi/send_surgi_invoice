from setuptools import setup, find_packages

setup(
    name='send_surgi_invoice',
    version='0.0.1',
    description='Automate Sales Invoices',
    author='SurgiShop',
    author_email='gary.starr@surgishop.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=['frappe']
)
