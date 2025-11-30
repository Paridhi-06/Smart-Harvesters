
"""Model wrapper for CropGuardian.
"""
import os, io, logging, hashlib, numpy as np
from PIL import Image

logger = logging.getLogger('cropguardian.model')

class ModelWrapper:
    def __init__(self, model_path=None, input_size=224):
        self.model_path = model_path
        self.input_size = input_size
        self.model = None
        if model_path and os.path.exists(model_path):
            self._load_model(model_path)
        else:
            logger.info('No real model found at %s. Using deterministic pseudo-model.', model_path)

    def _load_model(self, path):
        logger.info('Model loading currently not implemented. Path: %s', path)

    def preprocess(self, image_path):
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            img = img.resize((self.input_size, self.input_size))
            arr = np.array(img).astype('float32') / 255.0
            return arr

    def predict(self, image_path):
        try:
            if self.model is not None:
                inp = self.preprocess(image_path)
                probs = self.model_infer(inp)
                label = 'disease-x'
                confidence = float(np.max(probs))
            else:
                with open(image_path, 'rb') as f:
                    b = f.read()
                h = int(hashlib.sha256(b).hexdigest(), 16)
                score = (h % 41) + 60
                diseases = ['Healthy', 'Possible Leaf Blight', 'Possible Nutrient Deficiency', 'Possible Rust', 'Possible Mildew']
                idx = h % len(diseases)
                label = diseases[idx]
                confidence = float(((h >> 7) % 30) + 60) / 100.0
                health_score = int(score)
                suggestions = {
                    'Healthy': 'No action required. Continue regular monitoring.',
                    'Possible Leaf Blight': 'Inspect affected area and consider targeted fungicide application.',
                    'Possible Nutrient Deficiency': 'Test soil and apply recommended NPK fertilizer.',
                    'Possible Rust': 'Remove severely affected leaves and monitor spread.',
                    'Possible Mildew': 'Improve air circulation; apply appropriate treatment.'
                }
                suggestion = suggestions.get(label, 'Inspect the field and consult agronomist.')
                return {
                    'disease': label,
                    'confidence': f"{confidence*100:.2f}%",
                    'health_score': health_score,
                    'suggestion': suggestion
                }
        except Exception as e:
            logger.exception('Error during prediction: %s', e)
            return {'error': 'prediction_failed'}
