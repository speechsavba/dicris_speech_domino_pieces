FROM ghcr.io/tauffer-consulting/domino-base-piece:latest
# Install specific requirements to run OpenCV
RUN apt-get update

# Need to copy pieces source code
COPY config.toml domino/pieces_repository/
COPY pieces domino/pieces_repository/pieces
COPY .domino domino/pieces_repository/.domino

# Install specific dependencies in domino_env virtual environment
RUN pip install --no-cache-dir numpy==1.23.5
RUN pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir scipy librosa unidecode phonemizer Cython 
RUN pip install --no-cache-dir librosa onnxruntime
RUN pip install --no-cache-dir joblib scikit-learn==1.7.2
#RUN pip install --no-cache-dir resampy tensorflow soundfile tf-keras
RUN cd /home/domino/pieces_repository/pieces/TTSPiece/monotonic_align/ && python setup.py build_ext --inplace
RUN apt-get update && apt-get install -y wget unzip
RUN cd /home/domino/pieces_repository/pieces/TTSPiece/model && wget http://speech.savba.sk/DiCris/tts_model.zip && unzip tts_model.zip && rm tts_model.zip
RUN ls -l /home/domino/pieces_repository/pieces/TTSPiece/model/
RUN cd /home/domino/pieces_repository/pieces/TTSPiece/ && python tts_vits.py
RUN cd /home/domino/pieces_repository/ && python -c "from pieces.TTSPiece.tst_tts_piece import test_tts_piece; test_tts_piece()"
RUN cd /home/domino/pieces_repository/ && python -c "from pieces.InsulatorEnvironmentSoundsPiece.tst_insulatorenvironmentsounds_piece import test_insulatorenvironmentsounds_piece; test_insulatorenvironmentsounds_piece()"
RUN cd /home/domino/pieces_repository/ && python -c "from pieces.InsulatorHealthPiece.tst_insulatorhealth_piece import test_insulatorcontamination_piece; test_insulatorcontamination_piece()"
RUN cd /home/domino/pieces_repository/ && python -c "from pieces.DicrisDatasetPiece.test_dicrisdataset_piece import test_dicrisdataset_piece; test_dicrisdataset_piece()"
RUN ls -l /home/domino/pieces_repository/pieces/TTSPiece/tmp/
CMD ["ls","-l","/home/domino/pieces_repository/pieces/TTSPiece/tmp/"]
#CMD ["cd", "/home/domino/pieces_repository/pieces/TTSPiece/","&&","python","tst_tts_piece.py","&&","ls","-l","/home/domino/pieces_repository/pieces/TTSPiece/tmp/"
