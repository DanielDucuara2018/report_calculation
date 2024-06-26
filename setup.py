from setuptools import find_packages, setup

VERSION = "0.1"

INSTALL_REQUIRES = [
    "alembic==1.9.4",
    "apischema==0.15.6",
    "asyncio==3.4.3",
    "bcrypt==4.1.2",
    "configparser==5.3.0",
    "fastapi[all]==0.92.0",
    "fastapi-utils==0.2.1",
    "psycopg2==2.9.1",
    "python-binance==1.0.16",
    "python-jose[cryptography]==3.3.0",
    "python-telegram-bot==20.0a2",
    "SQLAlchemy==1.4.37",
]

setup(
    name="report-calculation",
    version=VERSION,
    python_requires=">=3.9.0",
    packages=find_packages(exclude=["tests"]),
    author="Daniel Ducuara",
    author_email="daniel14015@gmail.com",
    description="Get a report of my porfolio",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "telegram-bot = report_calculation.telegram.bot:telegram_bot",
            # "console = report_calulation.main:console",
        ]
    },
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "dev": [
            "alembic==1.9.4",
            "bandit==1.7.0",
            "mypy==0.931",
            "pre-commit==3.1.0",
            "pylint==2.7.0",
            "black==22.10.0",
            "isort==5.10.1",
            "beautysh==6.2.1",
            "autoflake==1.7.7",
        ],
        "test": [
            "pytest==6.2.4",
            "pytest-mock==3.6.1",
            "pytest-cov==2.12.1",
            "pytest-asyncio==0.15.1",
        ],
    },
)
