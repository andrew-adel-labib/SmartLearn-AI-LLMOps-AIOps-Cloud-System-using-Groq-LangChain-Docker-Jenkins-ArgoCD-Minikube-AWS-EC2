from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="SmartLearn AI LLMOps AIOps Intelligent Automation System",
    version="0.1",
    author="Andrew-Adel",
    packages=find_packages(),
    install_requires = requirements,
)