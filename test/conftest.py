"""Pytest configuration and fixtures for hifimagnet.paraview test suite."""

import shutil
import tarfile
from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def test_data():
    """
    Extract test data from archive before running tests.

    This fixture automatically runs once per test session and extracts
    the test data archive (data.tar.gz) into the test directory.

    The archive contains:
    - cases/: Test simulation data in EnSight format
    - models/: JSON configuration files and mesh files
    - Pictures/: Reference images for visual regression testing

    For CI environments, the extracted data can be cached to avoid
    repeated extraction across test runs.
    """
    test_dir = Path(__file__).parent
    archive_path = test_dir / "data.tar.gz"
    extract_marker = test_dir / ".data_extracted"

    # Check if data is already extracted (useful for local development and CI caching)
    if extract_marker.exists():
        print(f"\n✓ Test data already extracted (marker found: {extract_marker})")
        yield
        return

    # Verify archive exists
    if not archive_path.exists():
        pytest.fail(f"Test data archive not found: {archive_path}")

    print(f"\n→ Extracting test data from {archive_path.name}...")

    # Extract archive
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=test_dir)

        # Move contents from unzip_for_pytest/ to test/ directory
        extracted_dir = test_dir / "unzip_for_pytest"
        if extracted_dir.exists():
            # Move each subdirectory (cases, models, Pictures)
            for item in extracted_dir.iterdir():
                dest = test_dir / item.name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.move(str(item), str(dest))

            # Remove empty extracted directory
            extracted_dir.rmdir()

        # Create marker file to indicate successful extraction
        extract_marker.touch()
        print("✓ Test data extracted successfully")

    except Exception as e:
        pytest.fail(f"Failed to extract test data: {e}")

    yield

    # Optional: Cleanup after all tests complete
    # Uncomment if you want to remove extracted data after tests
    # This is typically NOT desired in CI (to leverage caching)
    # cleanup = os.getenv("PYTEST_CLEANUP_DATA", "false").lower() == "true"
    # if cleanup:
    #     for item in ["cases", "models", "Pictures", ".data_extracted"]:
    #         path = test_dir / item
    #         if path.is_dir():
    #             shutil.rmtree(path)
    #         elif path.is_file():
    #             path.unlink()
    #     print("\n✓ Test data cleaned up")
