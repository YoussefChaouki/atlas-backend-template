import logging

from atlas_template.core.database import AsyncSessionLocal
from atlas_template.repositories import notes as repo
from atlas_template.services import ai

logger = logging.getLogger(__name__)


async def process_note_embedding(note_id: int) -> None:
    """
    Tâche d'arrière-plan :
    1. Ouvre une NOUVELLE session DB (indépendante de la requête HTTP).
    2. Récupère la note.
    3. Génère l'embedding (OpenAI ou Mock).
    4. Sauvegarde.
    """
    async with AsyncSessionLocal() as session:
        try:
            # 1. Fetch note
            note = await repo.get_by_id(session, note_id)
            if not note:
                logger.warning(f"Note {note_id} not found for embedding processing.")
                return

            # 2. Generate embedding
            # Si le texte est vide, on peut décider de skipper ou mettre un vecteur nul.
            text_to_embed = f"{note.title} {note.content}"
            vector = await ai.get_embedding(text_to_embed)

            # 3. Update DB
            await repo.update_embedding(session, note_id, vector)
            logger.info(f"Embedding generated and saved for note {note_id}")

        except Exception as e:
            logger.error(f"Error processing embedding for note {note_id}: {e}")
