# Chef Gemini — Personal Chef & Meal Architect

An autonomous agent built with **Google ADK** (Agent Development Kit), **Gemini 2.5**, and **Agent Platform** that provides personalized culinary consultation, tailored recipe creation, dietary customization, Firestore catalog queries, and realistic plating visualization.

![Chef Gemini Demo](./demo.gif)

---

## Capabilities & Architecture

* **Interactive Meal Planning & Recipe Crafting**: Interprets user ingredients, meal types, and dietary preferences to synthesize structured recipes with step-by-step cooking directions.
* **Curated Recipe Catalog (Firestore)**: Persistent backend storage in Google Cloud Firestore for curated recipes, complete with cuisine and dietary tag indexing (`search_recipes`, `get_recipe_by_id`, `add_recipe`).
* **Visual Dish Generator (`gemini-3.1-flash-lite-image`)**: Automatically visualizes dishes with realistic plating and lighting presets, uploading rendered images directly to Google Cloud Storage (`generate_dish_image`).
* **Cross-Session Memory Bank (Vertex AI Agent Engine)**: Integrated with Vertex AI Memory Bank (`PreloadMemoryTool` and callback) to remember dietary preferences, allergies, and favorite dishes across sessions.
* **FastAPI A2A Proxy & Chat UI**: Minimal, responsive web interface built on the Agent-to-Agent (A2A) protocol with inline card rendering.

---

## Project Structure

```
├── personal-chef-agent/      # ADK Agent definition, backend tools, & services
│   ├── app/
│   │   ├── agent.py          # Root agent, tools registration, memory callback
│   │   ├── firestore_service.py # Firestore recipe queries and CRUD tools
│   │   ├── image_service.py  # Vertex AI image generation and GCS upload
│   │   └── fast_api_app.py   # FastAPI ADK & A2A runtime server
│   └── pyproject.toml        # Agent dependencies
├── frontend/                 # A2A FastAPI proxy & web chat UI
│   ├── main.py               # ADC-authenticated A2A proxy
│   └── static/index.html     # Interactive chat interface & card renderer
└── project_brief.md          # Architecture and design specification
```

---

## Local Development

### 1. Run the Agent
```bash
cd personal-chef-agent
uv sync
uv run adk web . --port 8080 --reload_agents
```

### 2. Run the Frontend Proxy
```bash
cd frontend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
Open `http://localhost:8080` to interact with Chef Gemini.
