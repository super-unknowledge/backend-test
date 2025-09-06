import pytest
from unittest.mock import AsyncMock

from app.services.candidate_service import CandidateService
from app.models.candidate import Candidate

@pytest.mark.asyncio
async def test_create_candidate():
    # Arrange
    mock_session = AsyncMock()
    # Mock .add() as async method (even if sync in reality)
    mock_session.add = AsyncMock()

    # Simulate DB-generated ID when adding candidate
    async def add_side_effect(candidate):
        candidate.id = "123e4567-e89b-12d3-a456-426614174000"

    mock_session.add.side_effect = add_side_effect

    # Act
    candidate_id = await CandidateService.create_candidate(
        db_session=mock_session,
        full_name="Alice Smith",
        email="alice@example.com",
        phone="+15551234567",
        skills=["Python", "Django"]
    )

    # Assert
    assert candidate_id == "123e4567-e89b-12d3-a456-426614174000"
    mock_session.add.assert_awaited_once()
    mock_session.flush.assert_awaited_once()

    added_candidate = mock_session.add.call_args[0][0]
    assert isinstance(added_candidate, Candidate)
    assert added_candidate.full_name == "Alice Smith"
    assert added_candidate.email == "alice@example.com"
    assert added_candidate.phone == "+15551234567"
    assert added_candidate.skills == "Python,Django"
