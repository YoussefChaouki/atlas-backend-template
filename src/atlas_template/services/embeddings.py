"""Background task service for processing note embeddings."""

import asyncio
import logging

from atlas_template.core.database import AsyncSessionLocal
from atlas_template.repositories import notes as repo
from atlas_template.services import ai

logger = logging.getLogger(__name__)

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2


async def process_note_embedding(
    note_id: int,
    max_retries: int = MAX_RETRIES,
) -> bool:
    """
    Background task to generate and store embedding for a note.

    Opens a NEW database session (independent from HTTP request).
    Implements retry logic for transient failures.

    Args:
        note_id: ID of the note to process
        max_retries: Maximum number of retry attempts

    Returns:
        True if embedding was successfully generated and stored
    """
    for attempt in range(max_retries):
        async with AsyncSessionLocal() as session:
            try:
                # 1. Fetch note
                note = await repo.get_by_id(session, note_id)
                if not note:
                    logger.warning(f"Note {note_id} not found for embedding processing")
                    return False

                # 2. Generate embedding
                text_to_embed = f"{note.title} {note.content}"
                vector = await ai.get_embedding(text_to_embed)

                # 3. Update database
                await repo.update_embedding(session, note_id, vector)
                logger.info(f"Embedding generated for note {note_id}")
                return True

            except Exception as e:
                logger.error(
                    f"Error processing embedding for note {note_id} "
                    f"(attempt {attempt + 1}/{max_retries}): {e}"
                )

                if attempt < max_retries - 1:
                    await asyncio.sleep(RETRY_DELAY_SECONDS * (attempt + 1))
                    continue

                logger.error(
                    f"Failed to process embedding for note {note_id} "
                    f"after {max_retries} attempts"
                )
                return False

    return False
