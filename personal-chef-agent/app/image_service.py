"""Image generation and Cloud Storage upload service for personal-chef-agent."""

import uuid
from google import genai
from google.genai import types
from google.cloud import storage
from google.adk.tools import ToolContext

PROJECT_ID = "qwiklabs-gcp-04-b54b139415f4"
BUCKET_NAME = "chef-gemini-recipes-b54b1394"
IMAGE_MODEL = "gemini-3.1-flash-lite-image"
LOCATION = "global"


async def generate_dish_image(
    dish_name: str,
    tool_context: ToolContext,
    style_description: str = "",
) -> str:
    """Generates an image of a dish using gemini-3.1-flash-lite-image in the global region.

    Saves the image as a session artifact for the Playground's Artifacts panel,
    uploads the image bytes to a public Cloud Storage bucket, and returns its public HTTPS URL.

    Args:
        dish_name: The name or description of the dish to visualize (e.g. 'Avocado & Black Bean Fiesta Salad').
        tool_context: ToolContext provided automatically by the ADK runtime.
        style_description: Optional presentation or plating style details (e.g. 'served in a rustic ceramic bowl, natural morning light').

    Returns:
        The public HTTPS URL of the uploaded image (https://storage.googleapis.com/<bucket>/<object>).
    """
    prompt = f"Professional food photography of {dish_name}."
    if style_description:
        prompt += f" Presentation style: {style_description}."

    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=prompt,
    )

    image_bytes = None
    mime_type = "image/jpeg"

    if response.candidates and response.candidates[0].content:
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                image_bytes = part.inline_data.data
                mime_type = part.inline_data.mime_type or "image/jpeg"
                break

    if not image_bytes:
        return "Failed to generate dish image: No image data returned by model."

    # Determine extension
    ext = "png" if "png" in mime_type else "jpg"
    unique_id = uuid.uuid4().hex[:12]
    filename = f"{dish_name.lower().replace(' ', '_')[:30]}_{unique_id}.{ext}"

    # 1. Save as artifact in Playground Artifacts panel
    artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    await tool_context.save_artifact(filename=filename, artifact=artifact_part)

    # 2. Upload same bytes to public Cloud Storage bucket
    gcs_object_name = f"dishes/{filename}"
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(gcs_object_name)
    blob.upload_from_string(image_bytes, content_type=mime_type)

    # Return public HTTPS URL
    return f"https://storage.googleapis.com/{BUCKET_NAME}/{gcs_object_name}"
