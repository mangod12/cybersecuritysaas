"""
Database seeding functionality.

This module provides functions to populate the database with initial
sample data. This is useful for development, testing, and demonstrations.
It includes functions to create a sample admin user and sample IT assets.
"""

import asyncio # Standard library for asynchronous programming.
from sqlalchemy.ext.asyncio import AsyncSession # For type hinting and async session operations.

# Local application imports
from backend.database.db import AsyncSessionLocal # Factory for creating async database sessions.
from backend.models.user import User # User ORM model.
from backend.models.asset import Asset, AssetType # Asset ORM model and AssetType enum.
from backend.services.auth_service import get_password_hash # Utility for hashing passwords.
import logging # Standard library for logging.

# Configure logger for this module
logger = logging.getLogger(__name__)


async def create_sample_user(session: AsyncSession) -> User:
    """
    Creates a sample administrative user if one doesn't already exist.

    This function checks if a user with ID 1 (assumed to be the admin)
    exists. If not, it creates a new user with predefined credentials
    and details.

    Args:
        session: The active asynchronous SQLAlchemy session.

    Returns:
        The created or existing sample User object.
    """
    # Attempt to retrieve an existing user with primary key 1.
    # `session.get()` is an efficient way to fetch an object by its primary key.
    existing_user = await session.get(User, 1) 
    if existing_user:
        logger.info(f"Sample user '{existing_user.email}' already exists. Skipping creation.")
        return existing_user
    
    # If no user with ID 1 exists, create a new one.
    logger.info("Creating a new sample user (admin@example.com)...")
    sample_user = User(
        email="admin@example.com",
        hashed_password=get_password_hash("password123"), # Hash the password before storing.
        full_name="Admin User",
        company="Example Corp",
        is_active=True,  # User is active by default.
        is_verified=True # User is marked as verified (e.g., email verification).
    )
    
    session.add(sample_user) # Add the new user object to the session.
    await session.commit()   # Commit the transaction to save the user to the database.
    await session.refresh(sample_user) # Refresh the user object to get its generated ID and other defaults.
    
    logger.info(f"Successfully created sample user: {sample_user.email} with ID: {sample_user.id}")
    return sample_user


async def create_sample_assets(session: AsyncSession, user: User) -> list[Asset]:
    """
    Creates a predefined list of sample IT assets for a given user.

    This function populates the database with various types of assets
    (OS, hardware, software, firmware) associated with the provided user.
    It skips creation if assets for this user seem to already exist (basic check).

    Args:
        session: The active asynchronous SQLAlchemy session.
        user: The User object to associate these assets with.

    Returns:
        A list of the created Asset objects.
    """
    # Basic check: if the user already has assets, assume they've been seeded.
    # A more robust check might query for specific asset names or count.
    # Instead of accessing user.assets (which triggers a lazy load and fails in async),
    # perform an explicit async query to check if the user already has assets.
    from sqlalchemy import select
    result = await session.execute(select(Asset).where(Asset.user_id == user.id).limit(1))
    existing_asset = result.scalar_one_or_none()
    if existing_asset:
        logger.info(f"User '{user.email}' already has assets. Skipping sample asset creation.")
        return []  # Or fetch and return all assets if needed

    logger.info(f"Creating sample assets for user: {user.email}...")
    sample_assets_data = [
        {
            "name": "Windows Server 2019",
            "asset_type": AssetType.OPERATING_SYSTEM,
            "vendor": "Microsoft",
            "product": "Windows Server",
            "version": "2019",
            "description": "Main production web server running critical applications.",
            "cpe_string": "cpe:2.3:o:microsoft:windows_server_2019:-:*:*:*:*:*:*:*"
        },
        {
            "name": "Cisco ASA 5525-X",
            "asset_type": AssetType.HARDWARE,
            "vendor": "Cisco",
            "product": "ASA 5525-X", # Adaptive Security Appliance
            "version": "9.12", # Firmware version might also be tracked here or separately
            "description": "Primary network firewall protecting the internal network.",
            "cpe_string": "cpe:2.3:h:cisco:asa_5525-x:-:*:*:*:*:*:*:*"
        },
        {
            "name": "Apache HTTP Server",
            "asset_type": AssetType.SOFTWARE,
            "vendor": "Apache",
            "product": "HTTP Server",
            "version": "2.4.54",
            "description": "Web server software hosting company websites.",
            "cpe_string": "cpe:2.3:a:apache:http_server:2.4.54:*:*:*:*:*:*:*"
        },
        {
            "name": "FortiGate 60F Firmware", # Name clarified
            "asset_type": AssetType.FIRMWARE, # Corrected type if it's firmware
            "vendor": "Fortinet",
            "product": "FortiOS", # Product is often the OS/Firmware name
            "version": "7.2.0",
            "description": "Firmware for FortiGate 60F network security appliance.",
            # CPE for FortiOS, often tied to the OS rather than hardware model directly for vulnerabilities
            "cpe_string": "cpe:2.3:o:fortinet:fortios:7.2.0:*:*:*:*:*:*:*" 
        }
    ]
    
    created_assets = []
    for asset_data in sample_assets_data:
        # Create Asset instance, linking it to the user.
        asset = Asset(
            user_id=user.id, # Associate asset with the user.
            **asset_data # Unpack other asset attributes from the dictionary.
        )
        session.add(asset) # Add the new asset to the session.
        created_assets.append(asset) # Keep track of created assets.
    
    await session.commit() # Commit the transaction to save all new assets.
    # No need to refresh each asset individually unless their generated IDs are immediately needed.
    # If IDs are needed, a loop with session.refresh(asset) after commit would be required,
    # or re-fetching them. For this seeding script, it's often not necessary.
    
    logger.info(f"Successfully created {len(created_assets)} sample assets for user '{user.email}'.")
    return created_assets


async def seed_database():
    """
    Main function to seed the database with initial data.

    This function orchestrates the creation of a sample user and their
    sample assets. It uses an `AsyncSessionLocal` to manage the database
    session.
    """
    logger.info("Attempting to seed database with initial data...")
    # Create a new asynchronous session context.
    async with AsyncSessionLocal() as session:
        try:
            # Create the sample user.
            sample_user = await create_sample_user(session)
            
            # If the user was successfully created or retrieved, create sample assets for them.
            if sample_user:
                await create_sample_assets(session, sample_user)
            
            # Note: `session.commit()` is called within `create_sample_user` and `create_sample_assets`
            # so an additional commit here is not strictly necessary if those functions handle it.
            # However, if there were other operations at this level, a commit here would be needed.
            # await session.commit() # Example if other direct db operations were done here.

            logger.info("Database seeding process completed successfully.")

        except Exception as e:
            # If any error occurs during seeding, log it and roll back the transaction.
            logger.error(f"Error during database seeding: {e}", exc_info=True)
            await session.rollback() # Rollback any changes made in the current transaction.
            raise # Re-raise the exception to be handled by the caller.

# This allows the script to be run directly, for example:
# python -m backend.database.seed
if __name__ == "__main__":
    print("Running database seeder directly...")
    # Setup basic logging for direct script execution
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    asyncio.run(seed_database())
    print("Database seeder finished.")