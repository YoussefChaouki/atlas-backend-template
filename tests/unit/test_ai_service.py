from unittest.mock import AsyncMock, patch

import pytest

from atlas_template.services.ai import get_embedding


@pytest.mark.asyncio
async def test_get_embedding_mock():
    # Setup du mock response
    mock_vector = [0.1] * 1536
    mock_response = type(
        "Response", (), {"data": [type("Item", (), {"embedding": mock_vector})]}
    )

    # On patch 'atlas_template.services.ai.AsyncOpenAI'
    with patch("atlas_template.services.ai.AsyncOpenAI") as MockClient:
        # Configuration du client mocké
        mock_instance = MockClient.return_value
        mock_instance.embeddings.create = AsyncMock(return_value=mock_response)

        # Execution (même sans OPENAI_API_KEY réelle dans l'env, on peut setter une dummy pour passer le check)
        with patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test"}):
            vector = await get_embedding("Hello World")

        # Assertions
        assert len(vector) == 1536
        assert vector[0] == 0.1
        mock_instance.embeddings.create.assert_called_once()
        args, kwargs = mock_instance.embeddings.create.call_args
        assert kwargs["model"] == "text-embedding-3-small"
        assert kwargs["input"] == ["Hello World"]
