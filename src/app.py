from flask import request, jsonify
from src.utils.video_utils import get_whisper_srt

def register_routes(app):
    @app.route('/build_srt_file/<int:project_id>', methods=['POST'])
    def build_srt_file(project_id):
        if 'file' not in request.files:
            return jsonify({'error': 'No audio file uploaded'}), 400

        audio_file = request.files['file']

        try:
            transcript = get_whisper_srt(audio_file.filename, audio_file)
            return jsonify({
                'message': 'SRT file created successfully',
                'project_id': project_id,
                'transcript': transcript 
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


