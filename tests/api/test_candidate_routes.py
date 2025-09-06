import pytest
from unittest.mock import AsyncMock, patch, ANY

from app.schemas.candidate import CandidateRequest

@pytest.mark.asyncio
async def test_create_candidate_success(client):
    # Sample payload to send to the endpoint
    payload = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "skills": ["Python", "FastAPI"]
    }

    # Patch the CandidateService.create_candidate to return a fixed ID
    with patch("app.api.candidate_routes.CandidateService.create_candidate", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = 42  # Simulate DB returning candidate ID 42

        response = await client.post("/candidates/", json=payload)

        # Check response status
        assert response.status_code == 200
        assert response.json() == {"candidate_id": 42}

        # Confirm service was called correctly
        mock_create.assert_awaited_once_with(
            ANY,  # db_session (mocked via fixture)
            payload["full_name"],
            payload["email"],
            payload["phone"],
            payload["skills"]
        )

