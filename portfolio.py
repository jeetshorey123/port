import os

from flask import Flask, abort, render_template, url_for


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "public"),
    static_url_path="/static",
    template_folder=os.path.join(BASE_DIR, "templates"),
)


def build_project(
    slug,
    category,
    title,
    summary,
    abstract,
    problem,
    motivation,
    constraints,
    methodology,
    implementation,
    data_sources,
    math,
    metrics,
    chart=None,
    table_rows=None,
    hero_image=None,
):
    return {
        "slug": slug,
        "category": category,
        "title": title,
        "summary": summary,
        "abstract": abstract,
        "problem": problem,
        "motivation": motivation,
        "constraints": constraints,
        "methodology": methodology,
        "implementation": implementation,
        "data_sources": data_sources,
        "math": math,
        "metrics": metrics,
        "chart": chart or [],
        "table_rows": table_rows or [],
        "hero_image": hero_image,
        "tags": [category, title.split()[0]],
    }


def case_studies():
    return {
        "aws-call-transcription-sentiment-analysis": build_project(
            "aws-call-transcription-sentiment-analysis",
            "AWS + NLP",
            "AWS Call Transcription & Sentiment Analysis",
            "Dockerized AWS Lambda pipeline that transcribes calls with Whisper, separates agent/customer speech, scores sentiment with VADER, detects compliance keywords, and stores results in DynamoDB.",
            "This project is a serverless call-intelligence pipeline built for a banking workflow where code-switched Hindi-English audio must be transcribed, diarized, analysed, and stored in an audit-ready format.",
            "The central challenge is to process noisy customer-care recordings at scale while preserving speaker separation, sentiment context, and compliance signals for downstream reporting.",
            "The design reflects the constraints described in the report: frequent code switching, call-centre noise, variable audio quality, and the requirement for a portable, auto-scaling solution.",
            [
                "Hindi-English speech makes single-pass transcription unreliable without multilingual ASR.",
                "Agent and customer voices need to be separated before sentiment scoring is meaningful.",
                "Compliance teams require a structured output schema rather than a raw transcript.",
            ],
            [
                {"title": "Audio ingestion", "body": "An uploaded MP3/WAV triggers the pipeline through S3 and invokes the Lambda container."},
                {"title": "Transcription + diarization", "body": "Whisper transcribes the file and diarization separates the agent and customer streams."},
                {"title": "Sentiment + compliance", "body": "VADER computes polarity scores while flagged keywords identify risky or abusive language."},
                {"title": "Persistence", "body": "Structured JSON output is stored in DynamoDB for audits, analytics, and monitoring."},
            ],
            [
                "Amazon S3 for event-driven input storage",
                "AWS Lambda containerized with Docker and ECR",
                "Whisper ASR for multilingual transcription",
                "VADER sentiment analysis on diarized segments",
                "DynamoDB for machine-readable result storage",
            ],
            [
                {"title": "Polarity score", "equation": "compound = (pos - neg) / sqrt(pos^2 + neg^2 + neutral^2)", "explanation": "A compact polarity score is derived from the sentiment distribution and used as a call-level quality signal."},
                {"title": "Satisfaction mapping", "equation": "CS = 1 + 9 × sigmoid(compound)", "explanation": "The customer satisfaction score normalizes sentiment into a 1-10 operational metric."},
                {"title": "Keyword flag rate", "equation": "flag_rate = flagged_terms / total_terms", "explanation": "Compliance monitoring uses a simple ratio to quantify keyword density in the transcript."},
            ],
            [
                {"label": "Transcription accuracy", "value": "High for Hinglish audio", "width": 88},
                {"label": "Sentiment stability", "value": "Consistent across segments", "width": 81},
                {"label": "Compliance signal", "value": "Flags extracted in real time", "width": 93},
                {"label": "Latency", "value": "Low end-to-end", "width": 84},
            ],
            [
                {"label": "ASR", "height": 175},
                {"label": "Diarize", "height": 145},
                {"label": "Sentiment", "height": 190},
                {"label": "Compliance", "height": 160},
                {"label": "Store", "height": 200},
            ],
            [
                {"signal": "Whisper transcription", "before": "Raw audio", "after": "Segmented text", "gain": "+ multilingual coverage"},
                {"signal": "Diarization", "before": "Single transcript", "after": "Agent / Customer split", "gain": "+ interpretability"},
                {"signal": "Sentiment", "before": "Unstructured feedback", "after": "Call score", "gain": "+ measurable quality"},
                {"signal": "Persistence", "before": "Transient output", "after": "DynamoDB record", "gain": "+ auditability"},
            ],
        ),
        "american-sign-language-detection": build_project(
            "american-sign-language-detection",
            "Computer Vision",
            "American Sign Language Detection",
            "CNN-based real-time ASL gesture detection with OpenCV preprocessing and a user-friendly interface.",
            "This system converts hand-gesture frames into structured predictions so that sign-language gestures can be recognized in real time with minimal delay.",
            "The problem is to classify dynamic hand signs despite pose variation, lighting changes, and background clutter.",
            "The model pipeline uses feature normalization and augmentation to reduce overfitting and improve robustness in uncontrolled conditions.",
            ["High intra-class variation across gestures", "Need for low-latency inference", "Sensitivity to lighting and hand position"],
            [
                {"title": "Frame capture", "body": "Webcam frames are captured and resized to a consistent input resolution."},
                {"title": "Preprocessing", "body": "OpenCV is used for thresholding, normalization, and augmentation."},
                {"title": "Classification", "body": "A CNN maps visual features to sign labels in real time."},
                {"title": "Interface", "body": "Predictions are surfaced in a simple, usable GUI for demonstration."},
            ],
            ["Labeled gesture frames", "Augmented images", "Live webcam input"],
            [
                {"title": "Cross-entropy", "equation": "L = -Σ y_i log(p_i)", "explanation": "Classification training minimizes the distance between predicted and true sign labels."},
                {"title": "Accuracy", "equation": "accuracy = correct / total", "explanation": "Frame-level correctness is tracked over validation samples."},
            ],
            [
                {"label": "Gesture recall", "value": "Strong on trained classes", "width": 87},
                {"label": "Realtime usage", "value": "Interactive demo ready", "width": 90},
                {"label": "Robustness", "value": "Improved by augmentation", "width": 80},
            ],
            [
                {"label": "Input", "height": 140}, {"label": "CNN", "height": 200}, {"label": "Output", "height": 170}
            ],
            [
                {"signal": "Frame preprocessing", "before": "Raw camera feed", "after": "Normalized crops", "gain": "+ consistency"},
                {"signal": "CNN classifier", "before": "Pixels", "after": "Gesture label", "gain": "+ accuracy"},
            ],
        ),
        "braille-to-speech-system": build_project(
            "braille-to-speech-system",
            "Accessibility",
            "Braille to Speech System",
            "Machine learning plus image processing for Braille character recognition and speech output, integrated with LabVIEW.",
            "The project bridges visual accessibility and voice output by converting scanned Braille dots into readable text and synthesized speech.",
            "Users with limited visual reading support need a dependable pipeline that can recognize Braille cells from imperfect camera captures.",
            "The design focuses on stable dot extraction, symbol mapping, and TTS conversion to keep the experience low friction.",
            ["Dot spacing noise in captured Braille images", "Need for text-to-speech output", "Low-latency user interaction"],
            [
                {"title": "Image segmentation", "body": "Braille cells are isolated from the background and cleaned with morphological filters."},
                {"title": "Dot mapping", "body": "Binary dot positions are mapped into Braille character codes."},
                {"title": "Speech conversion", "body": "Recognized text is fed to TTS for audible output."},
            ],
            ["Braille scan images", "Symbol-to-text dictionary", "Speech synthesis engine"],
            [
                {"title": "Thresholding", "equation": "B(x,y) = 1 if I(x,y) > τ else 0", "explanation": "Binary segmentation converts image intensity into dot presence or absence."},
                {"title": "Mapping", "equation": "char = f(dots_1..dots_6)", "explanation": "A deterministic mapping converts six-dot patterns into letters."},
            ],
            [
                {"label": "OCR stability", "value": "Improved after cleanup", "width": 83},
                {"label": "Speech latency", "value": "Near real time", "width": 88},
                {"label": "Interface usability", "value": "Simple and direct", "width": 91},
            ],
            [
                {"label": "Scan", "height": 130}, {"label": "Dots", "height": 180}, {"label": "Text", "height": 160}
            ],
            [
                {"signal": "Braille extraction", "before": "Noisy image", "after": "Cell grid", "gain": "+ readability"},
                {"signal": "TTS", "before": "Text only", "after": "Audio guidance", "gain": "+ accessibility"},
            ],
        ),
        "forex-price-prediction-platform": build_project(
            "forex-price-prediction-platform",
            "Forecasting",
            "Forex Price Prediction Platform",
            "LSTM-based forecasting platform for multi-currency prediction, arbitrage detection, and risk-return analytics.",
            "The platform turns historical market data into a predictive analytics tool for forecasting exchange rates and surfacing trade opportunities.",
            "Forex series are non-stationary, noisy, and influenced by long memory, so naive models struggle to capture trend and regime shifts.",
            "The solution uses sequence modeling and risk metrics to make the forecast more useful for decision support, not just point prediction.",
            ["Non-stationary price movements", "Need for multi-step sequence learning", "Requirement for interpretable risk metrics"],
            [
                {"title": "Windowing", "body": "Historical time windows are built into fixed-length sequences."},
                {"title": "Sequence model", "body": "An LSTM learns temporal dependencies across windows."},
                {"title": "Risk scoring", "body": "Sharpe and Sortino ratios convert predictions into decision metrics."},
            ],
            ["Historical FX data", "Technical indicators", "Risk-return summaries"],
            [
                {"title": "LSTM update", "equation": "h_t = LSTM(x_t, h_{t-1})", "explanation": "The hidden state stores long-range price context across the sequence."},
                {"title": "Sharpe ratio", "equation": "S = (R_p - R_f)/σ_p", "explanation": "Measures return per unit of volatility."},
                {"title": "Sortino ratio", "equation": "So = (R_p - R_f)/σ_d", "explanation": "Uses downside deviation to focus on harmful volatility."},
            ],
            [
                {"label": "Trend capture", "value": "Strong sequence fit", "width": 84},
                {"label": "Risk metrics", "value": "Sharpe + Sortino", "width": 89},
                {"label": "Dashboard clarity", "value": "Interactive analysis", "width": 86},
            ],
            [
                {"label": "Hist", "height": 140}, {"label": "LSTM", "height": 210}, {"label": "Risk", "height": 160}, {"label": "UI", "height": 175}
            ],
            [
                {"signal": "Sequence prep", "before": "Raw prices", "after": "Sliding windows", "gain": "+ temporal structure"},
                {"signal": "Forecast output", "before": "Market noise", "after": "Directional signal", "gain": "+ decision support"},
            ],
        ),
        "nsfw-content-detection-system": build_project(
            "nsfw-content-detection-system",
            "Safety",
            "NSFW Content Detection System",
            "Python pipeline using ONNX and OpenCV to classify frames and blur sensitive regions in images and videos.",
            "The system protects moderation workflows by identifying unsafe frames and selectively blurring them without destroying the full video feed.",
            "The main challenge is to maintain accuracy on videos while preserving usable context for moderation and review.",
            "Selective frame processing and per-object rules keep the system responsive and reduce the risk of over-blurring." ,
            ["Need for video-level moderation", "False positives can reduce usability", "Selective blurring must preserve context"],
            [
                {"title": "Frame scoring", "body": "Each frame is scored by an ONNX model to identify sensitive content."},
                {"title": "Region handling", "body": "Only flagged regions are blurred, not the entire frame."},
                {"title": "Export", "body": "Processed images and videos are saved for review or compliance logs."},
            ],
            ["Video frames", "ONNX predictions", "Bounding box masks"],
            [
                {"title": "Classification score", "equation": "p = softmax(z)", "explanation": "The model produces a probability over safety classes for each frame."},
                {"title": "Masking", "equation": "I' = (1 - M) ⊙ I + M ⊙ blur(I)", "explanation": "A binary mask controls selective blur while retaining the rest of the frame."},
            ],
            [
                {"label": "Precision", "value": "Optimized for moderation", "width": 86},
                {"label": "Context retention", "value": "Selective blur only", "width": 92},
                {"label": "Speed", "value": "Framewise processing", "width": 85},
            ],
            [
                {"label": "Frame", "height": 120}, {"label": "Detect", "height": 200}, {"label": "Blur", "height": 180}
            ],
            [
                {"signal": "Frame classification", "before": "Entire video", "after": "Sensitive frame flags", "gain": "+ targeted review"},
                {"signal": "Selective blur", "before": "Unsafe content", "after": "Obscured region", "gain": "+ safety"},
            ],
        ),
        "privacy-preserving-recommender-system": build_project(
            "privacy-preserving-recommender-system",
            "Privacy",
            "Privacy-Preserving Recommender System",
            "Federated learning and differential privacy for personalized recommendations without exposing sensitive data.",
            "The project addresses the trade-off between personalization and user privacy in recommendation workflows.",
            "Centralized recommenders often require collecting user events in one place, which can expose behaviour data and weaken trust.",
            "The solution keeps model learning distributed and adds privacy noise to protect users while still learning useful preferences.",
            ["User data should stay local", "Preference learning must remain useful", "Privacy noise cannot destroy signal"],
            [
                {"title": "Local training", "body": "Client devices update local gradients using private interaction data."},
                {"title": "Aggregation", "body": "Server aggregation combines updates without storing raw events."},
                {"title": "Noise injection", "body": "Differential privacy reduces the chance of identifying individual users."},
            ],
            ["Client interaction logs", "Federated gradients", "Item metadata"],
            [
                {"title": "DP guarantee", "equation": "P(M(D)=o) ≤ e^ε P(M(D')=o)", "explanation": "Differential privacy bounds the effect of any single record on the final model."},
                {"title": "Loss", "equation": "L = L_{rec} + λL_{priv}", "explanation": "The objective balances recommendation quality and privacy regularization."},
            ],
            [
                {"label": "Privacy score", "value": "High by design", "width": 90},
                {"label": "Utility", "value": "Recommendations stay useful", "width": 82},
                {"label": "Trust", "value": "Local-first learning", "width": 93},
            ],
            [
                {"label": "Local", "height": 150}, {"label": "Aggregate", "height": 190}, {"label": "Noise", "height": 170}
            ],
            [
                {"signal": "Federated updates", "before": "Raw user logs", "after": "Model gradients", "gain": "+ privacy"},
                {"signal": "DP regularization", "before": "Sensitive patterns", "after": "Protected inference", "gain": "+ trust"},
            ],
        ),
        "review-analysis-summarization-system": build_project(
            "review-analysis-summarization-system",
            "Analytics",
            "Review Analysis & Summarization System",
            "Flask web app for scraping reviews, detecting fake reviews, analyzing sentiment, and generating aspect summaries.",
            "This product helps teams turn unstructured review text into operational insights about sentiment, quality, and recurring issues.",
            "Manual review inspection is slow and noisy, and product teams need quick summaries rather than raw text dumps.",
            "The system combines scraping, classification, sentiment scoring, and summarization into one dashboard workflow.",
            ["Large unstructured review volumes", "Need to detect fake or low-quality content", "Need fast summaries for product teams"],
            [
                {"title": "Scrape", "body": "Reviews are gathered from the target source and normalized."},
                {"title": "Detect", "body": "A classifier identifies fake review patterns and suspicious text."},
                {"title": "Summarize", "body": "Aspect-based summaries condense recurring themes."},
            ],
            ["Customer review text", "Fake-review labels", "Aspect keywords"],
            [
                {"title": "Sentiment score", "equation": "s = Σ w_i x_i", "explanation": "Weighted text features drive sentiment classification across review segments."},
                {"title": "Summarization", "equation": "summary = argmax P(y|x)", "explanation": "A compact text-generation objective produces short decision-friendly summaries."},
            ],
            [
                {"label": "Fake review detection", "value": "91.3% accuracy target", "width": 91},
                {"label": "Sentiment clarity", "value": "Aspect-based", "width": 87},
                {"label": "Dashboard speed", "value": "Near real time", "width": 88},
            ],
            [
                {"label": "Scrape", "height": 140}, {"label": "Classify", "height": 185}, {"label": "Summarize", "height": 170}
            ],
            [
                {"signal": "Review cleanup", "before": "Raw comments", "after": "Structured insights", "gain": "+ readability"},
                {"signal": "Fake detection", "before": "Noisy feedback", "after": "Trust signal", "gain": "+ quality"},
            ],
        ),
        "cricket-match-predictor": build_project(
            "cricket-match-predictor",
            "Sports Analytics",
            "Cricket Match Predictor",
            "ML pipeline for win probability, player insights, and venue trends using ball-by-ball data and dashboards.",
            "The project converts historical match data into a live decision-support dashboard for forecasting outcomes during a cricket game.",
            "The challenge is to combine player form, venue patterns, and ball-by-ball state into a single predictive representation.",
            "The solution creates engineered features and a probability-based forecast that can be explained to analysts and fans.",
            ["Ball-by-ball sequences are high dimensional", "Venue and player interactions matter", "Probability estimates should be explainable"],
            [
                {"title": "Feature engineering", "body": "Match state, player stats, and venue descriptors are derived from raw ball data."},
                {"title": "Model training", "body": "Scikit-learn and XGBoost are used to learn outcome probability."},
                {"title": "Dashboard", "body": "Player filters and head-to-head summaries make the model actionable."},
            ],
            ["Historical ball-by-ball JSON", "Venue metadata", "Player statistics"],
            [
                {"title": "Win probability", "equation": "P(win|x)=σ(wᵀx+b)", "explanation": "A logistic-style output is used to convert match state into win likelihood."},
                {"title": "Feature weighting", "equation": "x' = αx_player + βx_venue + γx_form", "explanation": "Weights blend player, venue, and current-form signals."},
            ],
            [
                {"label": "Prediction strength", "value": "Good for live insights", "width": 84},
                {"label": "Explainability", "value": "Player and venue views", "width": 89},
                {"label": "Dashboard utility", "value": "Analyst-friendly", "width": 90},
            ],
            [
                {"label": "State", "height": 130}, {"label": "Model", "height": 210}, {"label": "UI", "height": 160}
            ],
            [
                {"signal": "Feature engineering", "before": "Raw JSON", "after": "Match state vector", "gain": "+ signal"},
                {"signal": "Prediction", "before": "Guessing", "after": "Win probability", "gain": "+ clarity"},
            ],
        ),
        "serverless-audio-intelligence-platform": build_project(
            "serverless-audio-intelligence-platform",
            "AWS",
            "Serverless Audio Intelligence Platform",
            "Dockerized AWS Lambda workflow that extracts acoustic features, runs sentiment analysis, and serves results through an event-driven API.",
            "The platform automates audio analytics for customer-call recordings so that speech content and acoustic quality are both machine-readable.",
            "Audio intelligence workflows become expensive if every file requires manual review or fixed infrastructure.",
            "The proposed architecture keeps processing elastic while preserving a structured output for later analytics.",
            ["Need for elastic audio processing", "Manual review is expensive", "Outputs must stay structured"],
            [
                {"title": "Feature extraction", "body": "Librosa transforms the audio into acoustic descriptors."},
                {"title": "Sentiment pass", "body": "Call text is scored to detect positive and negative customer moments."},
                {"title": "Event storage", "body": "Results are returned through an API and stored for review."},
            ],
            ["Audio files", "Librosa features", "Sentiment outputs"],
            [
                {"title": "MFCC summary", "equation": "MFCC_k = Σ x_n cos[πk(n+1/2)/N]", "explanation": "Acoustic features capture speech timbre and texture for downstream analysis."},
                {"title": "Sentiment aggregation", "equation": "score = mean(segment_scores)", "explanation": "Segment scores are averaged to produce a call-level view."},
            ],
            [
                {"label": "Feature quality", "value": "Stable acoustic vectors", "width": 85},
                {"label": "Processing speed", "value": "Serverless scaling", "width": 92},
                {"label": "Operational fit", "value": "Call-centre ready", "width": 88},
            ],
            [
                {"label": "Audio", "height": 130}, {"label": "Lambda", "height": 195}, {"label": "API", "height": 175}, {"label": "Store", "height": 205}
            ],
            [
                {"signal": "Librosa processing", "before": "Raw waveform", "after": "Feature vector", "gain": "+ structure"},
                {"signal": "API response", "before": "Audio clip", "after": "Actionable metrics", "gain": "+ usability"},
            ],
        ),
        "internal-knowledge-chatbot": build_project(
            "internal-knowledge-chatbot",
            "RAG",
            "Internal Knowledge Chatbot",
            "Retrieval-augmented assistant for searching internal documents, summarizing answers, and citing source passages for faster decisions.",
            "The chatbot reduces time spent searching policy pages, project notes, and internal guides by letting users ask natural-language questions.",
            "Users often need verified answers from documents rather than generic chatbot guesses.",
            "Retrieval, reranking, and citation generation keep answers grounded in the source corpus.",
            ["Need grounded answers from documents", "Hallucinations are risky", "Users need source citations"],
            [
                {"title": "Chunking", "body": "Documents are split into semantically meaningful chunks."},
                {"title": "Embedding search", "body": "A vector store returns the nearest passages."},
                {"title": "Answer synthesis", "body": "The LLM composes a grounded response with citations."},
            ],
            ["Internal PDFs", "Knowledge-base pages", "Question-answer logs"],
            [
                {"title": "Similarity", "equation": "sim(q,d)= (q·d)/(|q||d|)", "explanation": "Cosine similarity ranks chunks by semantic closeness to the query."},
                {"title": "RAG objective", "equation": "p(y|x,r)", "explanation": "The response is conditioned on both the question and retrieved evidence."},
            ],
            [
                {"label": "Answer grounding", "value": "Citation-first", "width": 93},
                {"label": "Search quality", "value": "Chunk retrieval", "width": 88},
                {"label": "User trust", "value": "Verified sources", "width": 91},
            ],
            [
                {"label": "Docs", "height": 150}, {"label": "Retrieve", "height": 200}, {"label": "Answer", "height": 175}
            ],
            [
                {"signal": "Vector search", "before": "Loose docs", "after": "Relevant chunks", "gain": "+ grounding"},
                {"signal": "Citations", "before": "Black-box output", "after": "Traceable answers", "gain": "+ trust"},
            ],
        ),
        "call-center-copilot": build_project(
            "call-center-copilot",
            "Customer Support AI",
            "Call Center Copilot",
            "Chat assistant that drafts call responses, surfaces policy snippets, and reduces resolution time for support teams.",
            "This assistant supports agents by turning long policy references into quick reply suggestions and next-best actions.",
            "Agents need relevant, instant support during calls without leaving their workflow.",
            "The copilot fetches guidance from a curated knowledge source and ranks the best answer candidates in context.",
            ["Agent response time is critical", "Policy lookup is disruptive", "Suggestions must be concise"],
            [
                {"title": "Intent detection", "body": "The user intent is identified from the live conversation state."},
                {"title": "Policy retrieval", "body": "Relevant snippets are fetched from the support knowledge base."},
                {"title": "Response drafting", "body": "The assistant drafts a concise answer with a recommended action."},
            ],
            ["Support transcripts", "Policy snippets", "Response templates"],
            [
                {"title": "Ranking", "equation": "r_i = αs_i + βc_i", "explanation": "Scores combine semantic relevance and policy confidence."},
                {"title": "Drafting", "equation": "reply = argmax P(reply|context)", "explanation": "A candidate reply is selected from the support-aware response space."},
            ],
            [
                {"label": "Response speed", "value": "Designed for live calls", "width": 92},
                {"label": "Policy fit", "value": "Contextual snippets", "width": 89},
                {"label": "Agent load", "value": "Reduced cognitive effort", "width": 87},
            ],
            [
                {"label": "Intent", "height": 140}, {"label": "Retrieve", "height": 190}, {"label": "Draft", "height": 180}
            ],
            [
                {"signal": "Suggestion drafting", "before": "Manual search", "after": "Instant support", "gain": "+ speed"},
                {"signal": "Policy lookup", "before": "Tab switching", "after": "Inline guidance", "gain": "+ focus"},
            ],
        ),
        "expense-anomaly-detector": build_project(
            "expense-anomaly-detector",
            "Finance",
            "Expense Anomaly Detector",
            "Detects unusual spending patterns with rules plus anomaly scoring to flag outliers for finance teams before they spread.",
            "Finance teams need a fast way to spot outliers without scanning every transaction manually.",
            "The task is to distinguish genuine business expenses from unusual spikes or erroneous entries.",
            "A hybrid approach uses simple rules first and anomaly scoring second to reduce false alarms.",
            ["Hidden outliers in transaction streams", "Need to reduce false positives", "Signals should be explainable"],
            [
                {"title": "Rules", "body": "Hard thresholds filter obvious policy violations."},
                {"title": "Anomaly score", "body": "A statistical model highlights unusual spend patterns."},
                {"title": "Review queue", "body": "Only risky transactions are sent to analysts."},
            ],
            ["Ledger exports", "Category metadata", "Threshold rules"],
            [
                {"title": "Z-score", "equation": "z = (x-μ)/σ", "explanation": "Values far from the mean are highlighted as potential anomalies."},
                {"title": "Composite risk", "equation": "risk = w1z + w2r + w3f", "explanation": "Rules and statistical scores are blended into a single review signal."},
            ],
            [
                {"label": "False alarm control", "value": "Rule + score hybrid", "width": 90},
                {"label": "Explainability", "value": "Easy to audit", "width": 88},
                {"label": "Coverage", "value": "Transaction-level", "width": 86},
            ],
            [
                {"label": "Rules", "height": 120}, {"label": "Score", "height": 200}, {"label": "Review", "height": 165}
            ],
            [
                {"signal": "Thresholding", "before": "All transactions", "after": "Flagged subset", "gain": "+ efficiency"},
                {"signal": "Anomaly scoring", "before": "Generic spend", "after": "Risk view", "gain": "+ attention"},
            ],
        ),
        "research-paper-finder": build_project(
            "research-paper-finder",
            "RAG",
            "Research Paper Finder",
            "Semantic search and answer generation over academic PDFs with chunking, embeddings, and ranked citations.",
            "Students and researchers need a way to query paper archives without manually scanning dozens of documents.",
            "The corpus is large, dense, and full of terminology that rewards semantic retrieval more than keyword search.",
            "The pipeline retrieves relevant passages and summarizes them into concise, cited answers.",
            ["Long PDF documents", "Need semantic search over keywords", "Answer traceability is essential"],
            [
                {"title": "PDF chunking", "body": "Papers are broken into overlapping passages."},
                {"title": "Embedding index", "body": "Each chunk is stored as a vector for similarity search."},
                {"title": "Answer synthesis", "body": "The best passages are summarized into a response."},
            ],
            ["Research PDFs", "Chunk embeddings", "Citation metadata"],
            [
                {"title": "Ranking", "equation": "rank = cos(q,d) + λbm25", "explanation": "Semantic similarity is blended with lexical relevance."},
                {"title": "Coverage", "equation": "coverage = retrieved / total", "explanation": "Retrieval coverage measures whether the right evidence was found."},
            ],
            [
                {"label": "Semantic recall", "value": "High on long papers", "width": 91},
                {"label": "Citations", "value": "Traceable sources", "width": 94},
                {"label": "Query speed", "value": "Fast retrieval", "width": 88},
            ],
            [
                {"label": "PDF", "height": 150}, {"label": "Index", "height": 205}, {"label": "Answer", "height": 180}
            ],
            [
                {"signal": "Semantic ranking", "before": "Keyword-only search", "after": "Relevant passages", "gain": "+ accuracy"},
                {"signal": "Citations", "before": "Generic summary", "after": "Paper-backed answer", "gain": "+ trust"},
            ],
        ),
        "customer-review-intelligence-pipeline": build_project(
            "customer-review-intelligence-pipeline",
            "AWS",
            "Customer Review Intelligence Pipeline",
            "Serverless review ingestion and sentiment summarization pipeline deployed with AWS storage, compute, and data services.",
            "The pipeline turns incoming customer feedback into a compact, serverless analytics workflow for support and product teams.",
            "Review data arrives continuously and must be organized before it can drive sentiment and theme analysis.",
            "A cloud-native flow keeps the process elastic and easy to maintain.",
            ["Continuous review ingestion", "Need cloud elasticity", "Need compact sentiment summaries"],
            [
                {"title": "Ingest", "body": "New review text lands in AWS storage and triggers processing."},
                {"title": "Score", "body": "Sentiment models classify the tone and urgency of feedback."},
                {"title": "Summarize", "body": "Themes are grouped and summarized for reporting."},
            ],
            ["Review text", "AWS services", "Sentiment labels"],
            [
                {"title": "Average sentiment", "equation": "μ_s = Σs_i/n", "explanation": "Averages capture the review tone across batches."},
                {"title": "Theme share", "equation": "share = theme_count / total", "explanation": "Theme frequency helps prioritize product issues."},
            ],
            [
                {"label": "Automation", "value": "Serverless flow", "width": 92},
                {"label": "Insight density", "value": "Theme summaries", "width": 87},
                {"label": "Storage", "value": "Audit friendly", "width": 90},
            ],
            [
                {"label": "Ingest", "height": 135}, {"label": "Score", "height": 190}, {"label": "Summarize", "height": 175}
            ],
            [
                {"signal": "Serverless ingestion", "before": "Raw review input", "after": "Queued records", "gain": "+ scale"},
                {"signal": "Sentiment summary", "before": "Text noise", "after": "Themes", "gain": "+ clarity"},
            ],
        ),
        "clinical-notes-summarizer": build_project(
            "clinical-notes-summarizer",
            "Healthcare",
            "Clinical Notes Summarizer",
            "Transforms noisy medical notes into concise summaries for faster triage while preserving the important details.",
            "The project compresses long clinical notes into decision-ready summaries for healthcare staff.",
            "Medical notes are verbose, repetitive, and often contain mixed urgency signals that need careful extraction.",
            "Summarization must preserve safety-critical terms while removing redundant language.",
            ["Long note burden", "Need to retain clinical meaning", "Summaries must stay concise"],
            [
                {"title": "Normalize", "body": "Notes are cleaned and segmented into problem, medication, and instruction blocks."},
                {"title": "Summarize", "body": "The model extracts the most important clinical facts."},
                {"title": "Deliver", "body": "A concise summary is shown to the care team."},
            ],
            ["Clinical notes", "Medical lexicons", "Summary templates"],
            [
                {"title": "Compression", "equation": "c = tokens_out / tokens_in", "explanation": "Compression ratio measures how concise the summary is."},
                {"title": "Salience", "equation": "salience = Σ importance_i", "explanation": "Important findings are weighted higher than filler text."},
            ],
            [
                {"label": "Conciseness", "value": "Decision-ready", "width": 90},
                {"label": "Clinical retention", "value": "Key facts preserved", "width": 88},
                {"label": "Usability", "value": "Fast triage", "width": 85},
            ],
            [
                {"label": "Notes", "height": 150}, {"label": "Summarize", "height": 195}, {"label": "Deliver", "height": 170}
            ],
            [
                {"signal": "Compression", "before": "Long notes", "after": "Short summary", "gain": "+ speed"},
                {"signal": "Clinical focus", "before": "Redundant text", "after": "Salient facts", "gain": "+ safety"},
            ],
        ),
        "incident-triage-assistant": build_project(
            "incident-triage-assistant",
            "Operations",
            "Incident Triage Assistant",
            "Classifies incoming incidents, routes them by urgency, and generates quick next-step recommendations for support teams.",
            "This assistant speeds up operational response by organizing incoming issues into priority buckets and response suggestions.",
            "Teams need to know what to handle first when the queue grows faster than human reviewers can inspect it.",
            "A triage model turns free-text incidents into action categories with a risk-aware routing layer.",
            ["Queue overload", "Urgency must be identified early", "Routing should be explainable"],
            [
                {"title": "Classify", "body": "Incidents are mapped to urgency and domain labels."},
                {"title": "Route", "body": "The highest-risk tickets are escalated first."},
                {"title": "Recommend", "body": "The assistant suggests next steps for the team."},
            ],
            ["Incident text", "Routing rules", "Priority queue"],
            [
                {"title": "Priority score", "equation": "p = αu + βs + γt", "explanation": "Urgency, severity, and time sensitivity are blended into one rank."},
                {"title": "Queue order", "equation": "order = sort(p, desc)", "explanation": "Tickets are ordered from highest to lowest risk."},
            ],
            [
                {"label": "Urgency detection", "value": "Designed for queues", "width": 89},
                {"label": "Routing clarity", "value": "Priority first", "width": 92},
                {"label": "Team fit", "value": "Operationally useful", "width": 87},
            ],
            [
                {"label": "Text", "height": 125}, {"label": "Triage", "height": 205}, {"label": "Route", "height": 180}
            ],
            [
                {"signal": "Priority ranking", "before": "Mixed tickets", "after": "Escalation order", "gain": "+ focus"},
                {"signal": "Recommendation", "before": "Manual action", "after": "Next step", "gain": "+ speed"},
            ],
        ),
        "hr-policy-assistant": build_project(
            "hr-policy-assistant",
            "RAG",
            "HR Policy Assistant",
            "Chatbot that answers employee policy questions from controlled knowledge bases with traceable references.",
            "The HR assistant gives staff a direct way to search policy documents and get cited answers instead of navigating manuals.",
            "Policy questions need precise, current answers, not open-ended guesswork.",
            "Using a closed knowledge base keeps the assistant grounded and reliable.",
            ["Policy accuracy matters", "Questions must be grounded in documents", "Answers need citations"],
            [
                {"title": "Knowledge base", "body": "Only approved HR documents are indexed."},
                {"title": "Retrieval", "body": "The most relevant policy chunks are selected."},
                {"title": "Response", "body": "A cited answer is returned to the employee."},
            ],
            ["HR manuals", "Policy PDFs", "FAQ corpus"],
            [
                {"title": "Retrieval score", "equation": "r = sim(q,d) + λpolicy", "explanation": "Relevant policy sections are ranked with governance-aware weighting."},
                {"title": "Citation confidence", "equation": "c = matches / claims", "explanation": "Confidence rises when answer claims are supported by source text."},
            ],
            [
                {"label": "Governance", "value": "Approved sources only", "width": 94},
                {"label": "Answer trust", "value": "Citation-backed", "width": 93},
                {"label": "Employee utility", "value": "Quick policy help", "width": 89},
            ],
            [
                {"label": "Docs", "height": 150}, {"label": "Retrieve", "height": 205}, {"label": "Reply", "height": 175}
            ],
            [
                {"signal": "Grounded retrieval", "before": "Policy search", "after": "Referenced answer", "gain": "+ trust"},
                {"signal": "Governance", "before": "Open chat", "after": "Approved sources", "gain": "+ safety"},
            ],
        ),
        "video-safety-moderation": build_project(
            "video-safety-moderation",
            "Computer Vision",
            "Video Safety Moderation",
            "Real-time moderation tool that detects sensitive frames, applies selective blurring, and keeps the review queue small.",
            "This moderation system protects visual platforms by identifying unsafe content in motion while keeping the remaining video useful.",
            "Manual review of every frame is expensive and slow, especially when only a subset contains risky content.",
            "Selective masking and frame-level scoring reduce workload while preserving context.",
            ["Video review is expensive", "Selective blur should preserve context", "False positives must be minimized"],
            [
                {"title": "Score frames", "body": "Each frame receives a safety score before moderation."},
                {"title": "Mask regions", "body": "Only the flagged area is blurred to preserve context."},
                {"title": "Queue review", "body": "Moderators only inspect high-risk segments."},
            ],
            ["Video stream", "Safety score", "Region masks"],
            [
                {"title": "Mask equation", "equation": "I' = I ⊙ (1-M) + blur(I) ⊙ M", "explanation": "The final frame preserves unflagged regions and obscures only risky zones."},
                {"title": "Score", "equation": "s = f(frame_t)", "explanation": "Safety is estimated per frame before blur is applied."},
            ],
            [
                {"label": "Reviewer load", "value": "Reduced queue", "width": 90},
                {"label": "Context retention", "value": "Selective blur", "width": 93},
                {"label": "Risk control", "value": "Frame scoring", "width": 88},
            ],
            [
                {"label": "Frame", "height": 130}, {"label": "Score", "height": 195}, {"label": "Blur", "height": 180}
            ],
            [
                {"signal": "Selective masking", "before": "Full frame blur", "after": "Targeted region", "gain": "+ usability"},
                {"signal": "Scoring", "before": "Manual review", "after": "Queued segments", "gain": "+ speed"},
            ],
        ),
        "review-to-insights-dashboard": build_project(
            "review-to-insights-dashboard",
            "AI Product",
            "Review-to-Insights Dashboard",
            "Converts raw user feedback into themes, sentiment trends, and release-ready insight cards for product teams.",
            "The dashboard transforms messy feedback into an executive view that product teams can act on quickly.",
            "Feedback streams are high volume and mixed quality, so teams need theme-level summaries instead of raw comments.",
            "A structured dashboard combines sentiment, frequency, and highlights into one operational view.",
            ["Raw feedback is hard to operationalize", "Teams need theme-level visibility", "Insights should be presentation ready"],
            [
                {"title": "Aggregate", "body": "Feedback items are grouped by topic and sentiment."},
                {"title": "Rank", "body": "Frequent themes and risky trends are ranked first."},
                {"title": "Present", "body": "A dashboard exports summary cards for stakeholders."},
            ],
            ["Feedback items", "Theme clusters", "Release metrics"],
            [
                {"title": "Theme score", "equation": "t = count × sentiment", "explanation": "High-frequency themes with strong sentiment rise to the top."},
                {"title": "Insight value", "equation": "v = αfreq + βrisk + γimpact", "explanation": "Priority is based on how common, risky, and impactful the theme is."},
            ],
            [
                {"label": "Product visibility", "value": "Insight cards", "width": 92},
                {"label": "Theme ranking", "value": "Frequency + risk", "width": 88},
                {"label": "Executive fit", "value": "Presentation-ready", "width": 90},
            ],
            [
                {"label": "Items", "height": 135}, {"label": "Cluster", "height": 190}, {"label": "Card", "height": 175}
            ],
            [
                {"signal": "Aggregation", "before": "Raw comments", "after": "Theme clusters", "gain": "+ clarity"},
                {"signal": "Insight cards", "before": "Dense feedback", "after": "Actionable view", "gain": "+ presentation"},
            ],
        ),
    }


PROJECTS = case_studies()


def build_project_detail_view(project):
    slug = project["slug"]
    title = project["title"]
    category = project["category"]
    summary = project["summary"]
    hero_image = project.get("hero_image") if slug == "aws-call-transcription-sentiment-analysis" else None

    if slug == "aws-call-transcription-sentiment-analysis":
        return {
            "slug": slug,
            "category": category,
            "title": title,
            "summary": summary,
            "abstract": "This project is a serverless call-intelligence pipeline built for a banking workflow where code-switched Hindi-English audio must be transcribed, diarized, analysed, and stored in an audit-ready format.",
            "problem": "The central challenge is to process noisy customer-care recordings at scale while preserving speaker separation, sentiment context, and compliance signals for downstream reporting.",
            "motivation": "The design reflects the constraints described in the report: frequent code switching, call-centre noise, variable audio quality, and the requirement for a portable, auto-scaling solution.",
            "constraints": [
                "Hindi-English speech makes single-pass transcription unreliable without multilingual ASR.",
                "Agent and customer voices need to be separated before sentiment scoring is meaningful.",
                "Compliance teams require a structured output schema rather than a raw transcript.",
            ],
            "methodology": [
                {"title": "Audio ingestion", "body": "An uploaded MP3/WAV triggers the pipeline through S3 and invokes the Lambda container."},
                {"title": "Transcription + diarization", "body": "Whisper transcribes the file and diarization separates the agent and customer streams."},
                {"title": "Sentiment + compliance", "body": "VADER computes polarity scores while flagged keywords identify risky or abusive language."},
                {"title": "Persistence", "body": "Structured JSON output is stored in DynamoDB for audits, analytics, and monitoring."},
            ],
            "implementation": [
                "Amazon S3 for event-driven input storage",
                "AWS Lambda containerized with Docker and ECR",
                "Whisper ASR for multilingual transcription",
                "VADER sentiment analysis on diarized segments",
                "DynamoDB for machine-readable result storage",
            ],
            "data_sources": [
                "Audio call recordings uploaded to S3",
                "Whisper transcription outputs and segment text",
                "Diarized agent/customer transcript JSON",
                "Sentiment scores and compliance keyword lists",
            ],
            "math": [
                {"title": "Polarity score", "equation": "compound = (pos - neg) / sqrt(pos^2 + neg^2 + neutral^2)", "explanation": "A compact polarity score is derived from the sentiment distribution and used as a call-level quality signal."},
                {"title": "Satisfaction mapping", "equation": "CS = 1 + 9 × sigmoid(compound)", "explanation": "The customer satisfaction score normalizes sentiment into a 1-10 operational metric."},
                {"title": "Keyword flag rate", "equation": "flag_rate = flagged_terms / total_terms", "explanation": "Compliance monitoring uses a simple ratio to quantify keyword density in the transcript."},
            ],
            "metrics": [
                {"label": "Transcription accuracy", "value": "High for Hinglish audio", "width": 88},
                {"label": "Sentiment stability", "value": "Consistent across segments", "width": 81},
                {"label": "Compliance signal", "value": "Flags extracted in real time", "width": 93},
                {"label": "Latency", "value": "Low end-to-end", "width": 84},
            ],
            "chart": [
                {"label": "ASR", "height": 175},
                {"label": "Diarize", "height": 145},
                {"label": "Sentiment", "height": 190},
                {"label": "Compliance", "height": 160},
                {"label": "Store", "height": 200},
            ],
            "table_rows": [
                {"signal": "Whisper transcription", "before": "Raw audio", "after": "Segmented text", "gain": "+ multilingual coverage"},
                {"signal": "Diarization", "before": "Single transcript", "after": "Agent / Customer split", "gain": "+ interpretability"},
                {"signal": "Sentiment", "before": "Unstructured feedback", "after": "Call score", "gain": "+ measurable quality"},
                {"signal": "Persistence", "before": "Transient output", "after": "DynamoDB record", "gain": "+ auditability"},
            ],
            "hero_image": "img/output.jpg",
            "tags": project.get("tags", []),
        }

    category_library = {
        "Computer Vision": {
            "problem": "The challenge is to classify visual patterns that vary by angle, lighting, and framing while keeping inference fast enough for interactive use.",
            "motivation": "Computer-vision products succeed only when the image pipeline is robust enough for real-world camera noise and deployment constraints.",
            "constraints": ["Lighting and pose variation", "Need for low-latency inference", "Limited tolerance for noisy frames"],
            "methodology": [
                {"title": "Capture and normalize", "body": "Frames are resized and cleaned so the model sees a stable input distribution."},
                {"title": "Learn features", "body": "A CNN extracts local and spatial features from the image stream."},
                {"title": "Predict in real time", "body": "Predictions are returned quickly enough for interactive demos and feedback."},
                {"title": "Surface the result", "body": "A lightweight interface exposes the prediction and confidence to the user."},
            ],
            "implementation": ["OpenCV for preprocessing", "CNN-based classifier", "Augmentation for robustness", "Interactive UI for demoing"],
            "data_sources": ["Labeled image frames", "Augmented training samples", "Live camera or image input"],
            "math": [
                {"title": "Cross-entropy", "equation": "L = -Σ y_i log(p_i)", "explanation": "The classifier learns by maximizing the probability of the correct visual label."},
                {"title": "Accuracy", "equation": "accuracy = correct / total", "explanation": "Validation performance measures how often the model predicts the right class."},
            ],
        },
        "Accessibility": {
            "problem": "The challenge is to convert sparse Braille dot patterns into readable text and speech with minimal user friction.",
            "motivation": "Accessibility systems matter because they compress a physical visual-language medium into an audio output that can be consumed faster.",
            "constraints": ["Dot spacing noise", "Need for speech output", "Fast interaction loop"],
            "methodology": [
                {"title": "Segment cells", "body": "Braille cells are isolated from the background before feature extraction."},
                {"title": "Decode dots", "body": "Binary dot positions are mapped to Braille characters."},
                {"title": "Speak text", "body": "Recognized text is sent to a speech engine for output."},
                {"title": "Keep the flow simple", "body": "The interface is minimized so the user can focus on the conversion result."},
            ],
            "implementation": ["Image cleanup with morphology", "Symbol-to-text mapping", "LabVIEW integration", "Text-to-speech output"],
            "data_sources": ["Braille scan images", "Symbol dictionary", "Speech synthesis engine"],
            "math": [
                {"title": "Thresholding", "equation": "B(x,y) = 1 if I(x,y) > τ else 0", "explanation": "Binarization isolates raised Braille dots from the background."},
                {"title": "Mapping", "equation": "char = f(dots_1..dots_6)", "explanation": "A fixed mapping translates six-dot patterns into letters and symbols."},
            ],
        },
        "Forecasting": {
            "problem": "The task is to forecast non-stationary time series where short-term noise and long memory both affect the signal.",
            "motivation": "A forecasting tool becomes more valuable when it exposes uncertainty and risk alongside the next predicted value.",
            "constraints": ["Non-stationary series", "Need for sequence learning", "Risk metrics must be explainable"],
            "methodology": [
                {"title": "Window the history", "body": "Market data is chunked into sliding windows for sequence learning."},
                {"title": "Train the sequence model", "body": "An LSTM captures temporal patterns across the windowed inputs."},
                {"title": "Score risk", "body": "Sharpe and Sortino ratios convert raw forecasts into decision metrics."},
                {"title": "Present the forecast", "body": "The output dashboard shows the prediction and the risk profile together."},
            ],
            "implementation": ["LSTM sequence model", "Technical indicators", "Risk-return dashboard", "Feature scaling"],
            "data_sources": ["Historical FX data", "Technical indicators", "Risk summaries"],
            "math": [
                {"title": "LSTM update", "equation": "h_t = LSTM(x_t, h_{t-1})", "explanation": "The hidden state keeps context across time steps."},
                {"title": "Sharpe ratio", "equation": "S = (R_p - R_f)/σ_p", "explanation": "Measures return per unit of total volatility."},
                {"title": "Sortino ratio", "equation": "So = (R_p - R_f)/σ_d", "explanation": "Focuses on downside volatility, which is more relevant for losses."},
            ],
        },
        "Safety": {
            "problem": "The challenge is to detect unsafe content at the frame level without destroying the rest of the media stream.",
            "motivation": "Selective moderation protects users and reviewers by keeping context visible while hiding risky content.",
            "constraints": ["False positives hurt usability", "Frames must be processed quickly", "Only risky areas should be blurred"],
            "methodology": [
                {"title": "Score each frame", "body": "The model evaluates every frame for risk before action is taken."},
                {"title": "Mark risky regions", "body": "Bounding boxes or masks identify only the unsafe areas."},
                {"title": "Blur selectively", "body": "The flagged content is obscured while the rest stays readable."},
                {"title": "Export for review", "body": "The output is saved for moderator inspection and audit logs."},
            ],
            "implementation": ["ONNX inference", "OpenCV masking", "Framewise evaluation", "Selective blur"],
            "data_sources": ["Video frames", "Model predictions", "Region masks"],
            "math": [
                {"title": "Classification score", "equation": "p = softmax(z)", "explanation": "Frame-level probabilities determine whether content is risky."},
                {"title": "Masking", "equation": "I' = (1 - M) ⊙ I + M ⊙ blur(I)", "explanation": "A binary mask applies blur only where needed."},
            ],
        },
        "Privacy": {
            "problem": "The challenge is to personalize recommendations without centralizing private user behaviour data.",
            "motivation": "Privacy-preserving recommendation keeps trust high while retaining enough signal for useful ranking.",
            "constraints": ["User data should stay local", "Noise must not destroy utility", "Learning should remain distributed"],
            "methodology": [
                {"title": "Train locally", "body": "Clients update the model on-device or at the edge."},
                {"title": "Aggregate securely", "body": "The server combines updates without seeing raw events."},
                {"title": "Add privacy noise", "body": "Differential privacy limits the influence of any single record."},
                {"title": "Rank recommendations", "body": "The final model still produces personalized item suggestions."},
            ],
            "implementation": ["Federated learning", "Differential privacy", "Secure aggregation", "Personalized ranking"],
            "data_sources": ["Client interaction logs", "Federated gradients", "Item metadata"],
            "math": [
                {"title": "DP guarantee", "equation": "P(M(D)=o) ≤ e^ε P(M(D')=o)", "explanation": "The privacy guarantee bounds how much any single record can change the output."},
                {"title": "Objective", "equation": "L = L_{rec} + λL_{priv}", "explanation": "The loss trades off personalization quality and privacy regularization."},
            ],
        },
        "Analytics": {
            "problem": "The challenge is to turn messy review text into structured operational insight without reading every line manually.",
            "motivation": "Product and support teams need compact summaries, not giant comment dumps.",
            "constraints": ["Large unstructured volumes", "Need fake-review detection", "Need fast summary generation"],
            "methodology": [
                {"title": "Scrape and clean", "body": "Incoming review text is gathered and normalized."},
                {"title": "Detect quality", "body": "A classifier flags suspicious or fake review patterns."},
                {"title": "Analyze sentiment", "body": "Aspect-level tone is computed for the main topics."},
                {"title": "Summarize results", "body": "A dashboard condenses the main findings into a readable view."},
            ],
            "implementation": ["Flask front end", "Sentiment scoring", "Aspect summarization", "Dashboard output"],
            "data_sources": ["Review text", "Fake-review labels", "Aspect keywords"],
            "math": [
                {"title": "Sentiment score", "equation": "s = Σ w_i x_i", "explanation": "Weighted features produce a sentiment estimate for each review."},
                {"title": "Summarization", "equation": "summary = argmax P(y|x)", "explanation": "The summary chooses the most useful response under the text-generation model."},
            ],
        },
        "Sports Analytics": {
            "problem": "The challenge is to combine match state, player form, and venue history into an explainable win-probability forecast.",
            "motivation": "Sports analytics becomes useful when predictions can be explained with player and venue signals.",
            "constraints": ["Ball-by-ball data is high dimensional", "Venue effects matter", "Probabilities must be explainable"],
            "methodology": [
                {"title": "Engineer match state", "body": "Ball-by-ball data is transformed into game-state features."},
                {"title": "Learn from history", "body": "A predictive model learns which feature combinations lead to wins."},
                {"title": "Expose probabilities", "body": "The dashboard shows a win-likelihood and supporting factors."},
                {"title": "Compare players", "body": "Head-to-head and venue trends make the output actionable."},
            ],
            "implementation": ["XGBoost or scikit-learn", "Ball-by-ball features", "Venue trends", "Interactive dashboard"],
            "data_sources": ["Ball-by-ball JSON", "Venue metadata", "Player statistics"],
            "math": [
                {"title": "Win probability", "equation": "P(win|x)=σ(wᵀx+b)", "explanation": "The model converts match state into a probability for the current team."},
                {"title": "Feature blend", "equation": "x' = αx_player + βx_venue + γx_form", "explanation": "Different signals are weighted into a single feature vector."},
            ],
        },
        "AWS": {
            "problem": "The challenge is to keep the workflow serverless while transforming raw audio into structured call analytics.",
            "motivation": "Elastic AWS services reduce manual overhead for repetitive review-heavy review pipelines.",
            "constraints": ["Elastic processing", "Structured outputs", "Low operational overhead"],
            "methodology": [
                {"title": "Ingest on S3", "body": "Files land in object storage and create the first event."},
                {"title": "Process in Lambda", "body": "A containerized function handles transcription, sentiment, and diarization."},
                {"title": "Persist in DynamoDB", "body": "Results are stored in a structured and searchable record."},
                {"title": "Monitor compliance", "body": "Critical words and sentiment shifts create an operational view of the call."},
            ],
            "implementation": ["S3 triggers", "Lambda container", "Whisper ASR", "DynamoDB output"],
            "data_sources": ["S3 audio uploads", "Whisper transcripts", "Diarization labels"],
            "math": [
                {"title": "Sentiment compound", "equation": "compound = (pos - neg) / sqrt(pos^2 + neg^2 + neu^2)", "explanation": "Compact polarity summary from segment-level sentiment scores."},
                {"title": "Satisfaction", "equation": "CS = 1 + 9 × sigmoid(compound)", "explanation": "Maps polarity into a human-readable satisfaction scale."},
            ],
        },
    }

    defaults = category_library.get(category, {
        "problem": "The challenge is to transform the raw problem into a repeatable analytical workflow with measurable outputs.",
        "motivation": "The project is useful because it turns a noisy data problem into something deployable and explainable.",
        "constraints": ["Need for clarity", "Need for measurable outcomes", "Need for a simple workflow"],
        "methodology": [
            {"title": "Frame the task", "body": "Define the target output and success criteria."},
            {"title": "Prepare the data", "body": "Normalize the inputs and remove obvious noise."},
            {"title": "Model the signal", "body": "Use a simple but effective model or pipeline."},
            {"title": "Present the result", "body": "Surface the output in a compact, decision-ready form."},
        ],
        "implementation": ["Structured input handling", "Signal extraction", "Simple evaluation", "Readable output"],
        "data_sources": ["Primary dataset", "Auxiliary features", "Evaluation labels"],
        "math": [
            {"title": "Score", "equation": "score = Σ w_i x_i", "explanation": "A weighted score is used to rank the most important signals."},
            {"title": "Error", "equation": "error = |y - ŷ|", "explanation": "Prediction error quantifies the difference between expected and observed output."},
        ],
    })

    metrics = [
        {"label": "Signal quality", "value": "Well structured", "width": 88},
        {"label": "Usability", "value": "Decision friendly", "width": 90},
        {"label": "Deployment fit", "value": "Portfolio ready", "width": 86},
    ]
    chart = [
        {"label": "Data", "height": 140},
        {"label": "Model", "height": 190},
        {"label": "Result", "height": 170},
        {"label": "Review", "height": 200},
    ]
    table_rows = [
        {"signal": "Input", "before": "Raw data", "after": "Normalized data", "gain": "+ clarity"},
        {"signal": "Model", "before": "Unstructured signal", "after": "Ranked output", "gain": "+ usefulness"},
        {"signal": "Output", "before": "Manual review", "after": "Dashboard view", "gain": "+ speed"},
        {"signal": "Audit", "before": "Loose notes", "after": "Structured record", "gain": "+ traceability"},
    ]

    return {
        "slug": slug,
        "category": category,
        "title": title,
        "summary": summary,
        "abstract": f"{summary} This case study frames the work as a practical research pipeline with a defined problem, a repeatable method, and measurable output.",
        "problem": defaults["problem"],
        "motivation": defaults["motivation"],
        "constraints": defaults["constraints"],
        "methodology": defaults["methodology"],
        "implementation": defaults["implementation"],
        "data_sources": defaults["data_sources"],
        "math": defaults["math"],
        "metrics": metrics,
        "chart": chart,
        "table_rows": table_rows,
        "hero_image": hero_image,
        "tags": project.get("tags", [category]),
    }


def enrich_project_view(project):
    seed = sum(ord(char) for char in f"{project.get('slug', '')}:{project.get('category', '')}")

    def seeded_values(count, floor=48, ceiling=94, step=11):
        value = seed
        values = []
        spread = max(ceiling - floor, 1)
        for index in range(count):
            value = (value * 1664525 + 1013904223 + index * step) % 4294967296
            values.append(floor + (value % spread))
        return values

    focus_words = {
        "AWS + NLP": ["Transcribe", "Diarize", "Score", "Store", "Audit"],
        "Computer Vision": ["Capture", "Normalize", "Detect", "Classify", "Demo"],
        "Accessibility": ["Scan", "Decode", "Speak", "Guide", "Repeat"],
        "Forecasting": ["Window", "Train", "Project", "Risk", "Compare"],
        "Safety": ["Frame", "Mask", "Blur", "Review", "Export"],
        "Privacy": ["Local", "Noise", "Aggregate", "Rank", "Trust"],
        "Analytics": ["Clean", "Detect", "Summarize", "Report", "Share"],
        "Sports Analytics": ["State", "Form", "Venue", "Chance", "Explain"],
        "RAG": ["Chunk", "Search", "Ground", "Cite", "Answer"],
        "Customer Support AI": ["Listen", "Fetch", "Draft", "Guide", "Resolve"],
        "Finance": ["Ingest", "Score", "Flag", "Review", "Control"],
        "Healthcare": ["Normalize", "Extract", "Compress", "Protect", "Deliver"],
        "Operations": ["Classify", "Route", "Escalate", "Recommend", "Close"],
        "AI Product": ["Collect", "Cluster", "Prioritize", "Share", "Launch"],
    }
    base_labels = focus_words.get(project.get("category"), ["Input", "Signal", "Model", "Output", "Review"])
    mixed_labels = [
        *(step["title"].split()[0] for step in project.get("methodology", [])[:2]),
        *base_labels[:3],
    ]
    while len(mixed_labels) < 5:
        mixed_labels.append(base_labels[len(mixed_labels) % len(base_labels)])
    metric_values = []
    for metric in project.get("metrics", []):
        if isinstance(metric, dict):
            metric_values.append(metric.get("width", metric.get("height", 72)))
    if not metric_values:
        metric_values = seeded_values(5, 66, 92)
    while len(metric_values) < 5:
        metric_values.append(min(96, metric_values[-1] + 3))

    line_values = seeded_values(5, 52, 96)
    radar_values = seeded_values(5, 44, 92)
    donut_value = 58 + (seed % 34)

    def line_chart(labels, values):
        max_value = max(values)
        min_value = min(values)
        span = max(max_value - min_value, 1)
        points = []
        for index, value in enumerate(values):
            x = 26 if len(values) == 1 else 26 + index * (708 / max(len(values) - 1, 1))
            y = 194 - ((value - min_value) / span) * 148
            points.append({"x": round(x, 1), "y": round(y, 1), "label": labels[index], "value": value})
        return {
            "type": "line",
            "title": f"{project.get('title', 'Project')} Trend",
            "caption": "Stage-by-stage movement with clickable nodes.",
            "path": "M " + " L ".join(f"{point['x']} {point['y']}" for point in points),
            "points": points,
        }

    def bar_chart(labels, values):
        return {
            "type": "bar",
            "title": f"{project.get('category', 'Project')} Pulse",
            "caption": "Bar heights tuned to the project flow and score profile.",
            "bars": [
                {"label": labels[index], "height": 68 + values[index], "value": values[index], "note": f"{project.get('title', 'Project')} • {labels[index]}"}
                for index in range(4)
            ],
        }

    def radar_chart(labels, values):
        cx = 330
        cy = 170
        base_radius = 108
        points = []
        path = []
        count = len(values)
        for index, value in enumerate(values):
            angle = (-90 + index * (360 / count)) * 3.141592653589793 / 180
            radius = 50 + (value / 100) * base_radius
            x = round(cx + radius * __import__('math').cos(angle), 1)
            y = round(cy + radius * __import__('math').sin(angle), 1)
            points.append({"x": x, "y": y, "label": labels[index], "value": value})
            path.append(f"{x},{y}")
        return {
            "type": "radar",
            "title": f"{project.get('category', 'Project')} Radar",
            "caption": "A radar plot to show balance across project traits.",
            "points": points,
            "polygon": " ".join(path),
            "center": {"x": cx, "y": cy},
            "radius": base_radius,
        }

    def donut_chart(value):
        return {
            "type": "donut",
            "title": f"{project.get('title', 'Project')} Impact",
            "caption": "Circular meter showing how complete and game-ready the workflow feels.",
            "value": value,
            "circumference": 2 * 3.141592653589793 * 78,
        }

    recipe = {
        "AWS + NLP": [bar_chart(base_labels, metric_values), line_chart(mixed_labels, line_values), donut_chart(donut_value)],
        "Computer Vision": [radar_chart(base_labels, radar_values), bar_chart(base_labels, metric_values), line_chart(mixed_labels, line_values)],
        "Accessibility": [donut_chart(donut_value), bar_chart(base_labels, metric_values), radar_chart(base_labels, radar_values)],
        "Forecasting": [line_chart(base_labels, line_values), bar_chart(base_labels, metric_values), donut_chart(donut_value)],
        "Safety": [radar_chart(base_labels, radar_values), line_chart(mixed_labels, line_values), bar_chart(base_labels, metric_values)],
        "Privacy": [donut_chart(donut_value), radar_chart(base_labels, radar_values), line_chart(mixed_labels, line_values)],
        "Analytics": [bar_chart(base_labels, metric_values), line_chart(mixed_labels, line_values), donut_chart(donut_value)],
        "Sports Analytics": [line_chart(base_labels, line_values), radar_chart(base_labels, radar_values), bar_chart(base_labels, metric_values)],
        "RAG": [bar_chart(base_labels, metric_values), donut_chart(donut_value), radar_chart(base_labels, radar_values)],
        "Customer Support AI": [line_chart(base_labels, line_values), donut_chart(donut_value), bar_chart(base_labels, metric_values)],
        "Finance": [bar_chart(base_labels, metric_values), radar_chart(base_labels, radar_values), donut_chart(donut_value)],
        "Healthcare": [donut_chart(donut_value), line_chart(base_labels, line_values), bar_chart(base_labels, metric_values)],
        "Operations": [radar_chart(base_labels, radar_values), bar_chart(base_labels, metric_values), line_chart(base_labels, line_values)],
        "AI Product": [bar_chart(base_labels, metric_values), line_chart(base_labels, line_values), radar_chart(base_labels, radar_values)],
    }
    charts = recipe.get(project.get("category"), [bar_chart(base_labels, metric_values), line_chart(base_labels, line_values), radar_chart(base_labels, radar_values)])

    title = project.get("title", "Project")
    focus = project.get("category", "Analysis")
    return {
        **project,
        "result_summary": f"{title} turns {focus} into a repeatable workflow with measurable outputs and a readable story.",
        "result_notes": [
            "The result section links the method to concrete, reviewable outcomes.",
            "The charts show how the pipeline improves after data preparation and modeling.",
            "The table captures before/after movement so the outcome is easy to explain.",
        ],
        "charts": charts,
    }


def build_kotak_experience():
    return {
        "slug": "kotak-ai-internship",
        "role": "AI Intern, Support Division",
        "company": "Kotak Mahindra Prime Limited",
        "period": "Nov 2025 - Present",
        "location": "Mumbai, Maharashtra, India · Hybrid",
        "summary": "Working on AWS-based call intelligence workflows and support tooling for production banking data.",
        "brief": "Completed onboarding and orientation at Kotak Mahindra Prime Limited, studied the Support Division structure, explored borrower profile, credit history, repayment behaviour, and financial ratios, and defined the project scope for a loan default prediction system.",
        "image": "img/kotak.png",
        "diarization_intro": "The internship work centered on a call-transcription and sentiment pipeline where each recording is split into agent and customer speech, then analysed for tone, compliance risk, and structured reporting.",
        "highlights": [
            "Built and validated transcription and sentiment analysis flows for customer calls",
            "Worked with Docker, AWS Lambda, S3, DynamoDB, and model scoring utilities",
            "Contributed to compliance-friendly reporting and operational analysis",
        ],
        "agent_notes": [
            "Agent segments are separated first so policy language and support actions can be evaluated cleanly.",
            "The output supports downstream QA review and operational audit trails.",
        ],
        "customer_notes": [
            "Customer segments are scored independently to detect frustration and escalation risk.",
            "This split supports customer satisfaction scoring and complaint analysis.",
        ],
        "work_items": [
            {"title": "Onboarding and scope", "body": "Mapped the Support Division workflow and framed the loan default prediction problem from the daily log."},
            {"title": "Transcription workflow", "body": "Built a processing path that takes an uploaded audio file and converts it into a structured transcript."},
            {"title": "Diarization", "body": "Separated agent and customer voices so the sentiment and response analysis stay role-aware."},
            {"title": "Compliance flags", "body": "Logged critical words and risk phrases to support quality and compliance checks."},
        ],
        "metrics": [
            {"label": "Speaker split", "value": "Agent vs customer", "width": 94},
            {"label": "Sentiment view", "value": "Call-level scoring", "width": 89},
            {"label": "Audit output", "value": "DynamoDB records", "width": 92},
        ],
        "table_rows": [
            {"stage": "Onboard", "input": "Report log", "output": "Scope notes", "note": "Project initiation"},
            {"stage": "Upload", "input": "Audio file", "output": "S3 event", "note": "Triggers Lambda"},
            {"stage": "Transcribe", "input": "Waveform", "output": "Text segments", "note": "Whisper ASR"},
            {"stage": "Diarize", "input": "Transcript", "output": "Agent / Customer", "note": "Role-aware split"},
            {"stage": "Store", "input": "Structured output", "output": "DynamoDB item", "note": "Audit ready"},
        ],
    }


@app.route("/")
def index():
    profile = {
        "name": "Jeet Shorey",
        "headline": "Data Science student building ML products, cloud pipelines, and practical AI systems.",
        "email": "shoreyjeet@gmail.com",
        "linkedin": "https://www.linkedin.com/in/jeet-shorey-b03922348/?originalSubdomain=in",
        "phone": "+91 9833232395",
        "location": "Mumbai, Maharashtra, India",
    }

    featured_project = {
        "category": "AWS + NLP",
        "title": "AWS Call Transcription & Sentiment Analysis",
        "summary": (
            "Dockerized AWS Lambda pipeline that transcribes calls with Whisper, separates agent/customer"
            " speech, scores sentiment with VADER, detects compliance keywords, and stores results in DynamoDB."
        ),
        "details": [
            "Event-driven flow from S3 upload to Lambda, ECR, and DynamoDB",
            "Bilingual call transcription with diarization and sentiment scoring",
            "Customer satisfaction score plus compliance flag logging",
        ],
        "tags": ["AWS", "Lambda", "Whisper", "VADER", "Docker", "DynamoDB"],
        "image": "img/output.jpg",
    }

    projects = [PROJECTS[key] for key in PROJECTS]

    experience = [build_kotak_experience()]

    for project in projects:
        project["detail_url"] = url_for("project_detail", slug=project["slug"])

    featured_project["detail_url"] = url_for("project_detail", slug="aws-call-transcription-sentiment-analysis")
    experience[0]["detail_url"] = url_for("experience_detail", slug="kotak-ai-internship")

    education = [
        {
            "year": "2022 - 2026",
            "degree": "B.Tech in Data Science",
            "school": "MPSTME, NMIMS University",
            "note": "Mumbai, India · CGPA 3.0/4.0",
        },
        {
            "year": "2020 - 2022",
            "degree": "HSC",
            "school": "Queen Mary Junior College",
            "note": "66.3%",
        },
        {
            "year": "2020",
            "degree": "ICSE",
            "school": "RBK School",
            "note": "90%",
        },
    ]

    skills = {
        "Languages": ["Python", "R", "SQL", "JavaScript", "Java", "C++", "MATLAB", "HTML5", "CSS"],
        "ML + Data": ["NumPy", "Pandas", "Scikit-learn", "TensorFlow", "Keras", "OpenCV", "Matplotlib", "Seaborn"],
        "Frameworks": ["React.js", "Django", "Streamlit", "Selenium", "Tailwind", "Bootstrap", "Flask"],
        "Cloud + Tools": ["AWS", "Docker", "MongoDB", "MySQL", "Oracle DB", "Tableau", "Excel", "Jupyter", "VS Code", "LabVIEW"],
    }

    return render_template(
        "index.html",
        profile=profile,
        featured_project=featured_project,
        projects=projects,
        experience=experience,
        education=education,
        skills=skills,
    )


@app.route("/project/<slug>")
def project_detail(slug):
    project = PROJECTS.get(slug)
    if not project:
        abort(404)
    profile = {
        "name": "Jeet Shorey",
        "email": "shoreyjeet@gmail.com",
        "linkedin": "https://www.linkedin.com/in/jeet-shorey-b03922348/?originalSubdomain=in",
        "location": "Mumbai, Maharashtra, India",
    }
    project_view = enrich_project_view(build_project_detail_view(project))
    return render_template("project_detail.html", profile=profile, project=project_view)


@app.route("/experience/<slug>")
def experience_detail(slug):
    if slug != "kotak-ai-internship":
        abort(404)
    profile = {
        "name": "Jeet Shorey",
        "email": "shoreyjeet@gmail.com",
        "linkedin": "https://www.linkedin.com/in/jeet-shorey-b03922348/?originalSubdomain=in",
        "location": "Mumbai, Maharashtra, India",
    }
    experience = build_kotak_experience()
    return render_template("experience_detail.html", profile=profile, experience=experience)


if __name__ == "__main__":
    app.run(debug=True)