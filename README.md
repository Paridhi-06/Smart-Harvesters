
CropGuardian - Cleaned Prototype

Summary of fixes:
- Fixed the 'same output' bug by using deterministic per-image pseudo-inference when a real model is not loaded.
- Ensured single model load via ModelWrapper.
- Added /api/predict endpoint returning JSON and frontend uses fetch().
- Input validation, secure filenames, upload size limit, and logging.
- Config file provided (config.yaml) for easy model path updates.
- Project structured for clarity (templates/, static/, models/, etc.).

How to run:
1. cd backend
2. python -m venv venv
3. venv\Scripts\activate   (Windows) or source venv/bin/activate
4. pip install -r requirements.txt
5. python app.py
6. Open http://127.0.0.1:5000/

To integrate your real model:
- Put model file in backend/models/
- Implement _load_model and model_infer in model.py
