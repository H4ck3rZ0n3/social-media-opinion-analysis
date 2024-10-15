
# Social Media Opinion Analysis Project

This project aims to analyze and classify social media comments into specific categories (e.g., Claim, Counterclaim, Rebuttal, Evidence) and generate summaries and effectiveness ratings for topics. The system uses **GPU acceleration** to handle large datasets efficiently and offers both batch processing and real-time analysis through a gRPC server.

---

## Features
- **Zero-shot classification** of comments into four categories: Claim, Counterclaim, Rebuttal, and Evidence.
- **Topic similarity analysis** using sentence embeddings.
- **Summary generation** for each topic and **effectiveness scoring** (Adequate, Effective, Ineffective).
- **GPU-accelerated** processing using CUDA for fast execution.
- **Batch processing** and **real-time analysis** via a gRPC server.
- **Logging** for error handling and memory management.
- **Output results** saved as CSV files with timestamped filenames.

---

## System Overview
This system is divided into several components:

1. **comment_classifier.py**  
   - Classifies comments using `facebook/bart-large-mnli`.
   - Runs on **CUDA** for GPU-accelerated processing.
   - Handles errors and manages GPU memory cleanup.

2. **conclusion_generator.py**  
   - Summarizes topics using `facebook/bart-large-cnn`.
   - Scores the effectiveness of topics with the `TopicEffectivenessClassifier`.
   - Groups related comments by topic and generates summaries.

3. **opinion_analyzer.py**  
   - Prepares and processes CSV data.
   - Uses `CommentClassifier` and `TopicSimilarityCalculator` to classify and group comments.
   - Saves the results to CSV files with summaries and effectiveness scores.

4. **topic_similarity_calculator.py**  
   - Computes topic similarity using sentence embeddings (`all-MiniLM-L6-v2`).
   - Uses **CUDA** for matrix operations to ensure fast similarity calculations.

5. **main.py**  
   - The entry point for the application.
   - Offers two modes:
     1. **CSV Analysis**: Processes opinion and topic data from CSV files.
     2. **gRPC Server**: Starts a gRPC server for real-time comment analysis.

---

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd <your-repository>
   ```

2. **Install dependencies**:
   - Make sure to install Python and CUDA Toolkit.
   - Install required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Prepare your environment**:
   - Ensure that a **GPU** with CUDA support is available.
   - Set up the necessary data files in `data/train/`:
     - `topics.csv`
     - `opinions.csv`

4. **Run the application**:
   ```bash
   python main.py
   ```

---

## Usage

### 1. Running CSV Analysis
- Place your data in the `data/train/` directory.
- When prompted, select **Option 1** to analyze the CSV files.
- The results will be saved in the `src/outputs/` directory.

### 2. Starting the gRPC Server
- Select **Option 2** from the main menu to start the gRPC server.
- The server will run and be ready to receive real-time comment and topic data.

---

## Directory Structure
```
/data
    └── train
        ├── topics.csv
        └── opinions.csv
/src
    └── grpc_server.py
    └──comment_classifier.py
    └──conclusion_generator.py
    └──opinion_analyzer.py
    └──topic_similarity_calculator.py
    └──main.py
/src/outputs
        └── (Generated CSV files will be saved here)

README.md
.DockerFile
```

---

## Error Handling
- **Logging**: All significant actions, errors, and memory management events are logged.
- **GPU Memory Management**: Each processing batch is followed by memory cleanup.
- **Validation**: The system checks for valid input and handles unexpected errors gracefully.

---

## Dependencies
- Python 3.x
- PyTorch
- Transformers
- Sentence-Transformers
- CUDA Toolkit
- cuDF and CuPy for GPU-accelerated DataFrames

---

## Example Output
Example summary of a topic:

```
Topic: Climate Change
Effectiveness: Effective
Summary: The comments indicate strong arguments supporting the idea of human-caused climate change...
```

---

## Contributing
Feel free to fork the project, open issues, or submit pull requests for any improvements or bug fixes.

---

## License
This project is licensed under the MIT License.

---

## Contact
For any questions or issues, please reach out to:  
**Developer:** Uğur Ortaç
**Email:** info@ugurortac.com