# EDUSENSE AI

## Explainable Student Learning Outcome Prediction from Tutoring Conversations

### Project Type

**Applied Machine Learning + Natural Language Processing + Explainable AI**

### Domain

**Educational AI / Intelligent Tutoring Systems**

### Proposed System

**EduSense — AI-powered tutoring conversation analysis and student learning outcome prediction platform**

---

# 1. Brief Project Description

**EduSense** is an AI-powered educational analytics system designed to analyze tutor–student conversations and predict whether a student is likely to answer the next question correctly.

The system combines **ModernBERT-based conversational language understanding** with structured interaction features extracted from tutoring sessions. Instead of treating a tutoring conversation as plain text only, EduSense considers both the linguistic content and measurable conversational characteristics such as student participation, response patterns, tutor questioning behavior, dialogue structure, and session-level statistics.

The system will provide:

* Student outcome prediction
* Prediction probability and confidence
* Conversation analytics
* Learning-objective-level performance analysis
* False-positive and false-negative analysis
* Model performance visualization
* Explainable insights
* Potential learning recommendations

The final system will expose the trained model through a **FastAPI backend** and provide an interactive **Next.js frontend dashboard**.

---

# 2. Problem Statement

Traditional tutoring systems generally focus on delivering learning content, while determining whether a student has actually understood a concept often requires manual interpretation by a teacher.

A tutoring conversation contains many signals:

```text
Student answers
Student reasoning
Tutor questions
Response length
Interaction patterns
Dialogue structure
Learning objective
```

However, these signals are difficult to analyze consistently at scale.

The problem addressed by EduSense is therefore:

> **Can an AI model analyze a tutoring conversation and predict whether the student is likely to answer the next question correctly?**

A successful system could help identify students or learning objectives that may require additional attention.

---

# 3. Motivation

The motivation behind EduSense is to move from simple educational analytics toward **conversation-aware learning analytics**.

Instead of asking only:

> "Did the student get this question right?"

EduSense attempts to learn from the **interaction leading up to that outcome**.

This makes the problem interesting from an NLP/ML perspective because the model must deal with:

* Long conversational context
* Noisy speech transcripts
* Tutor/student interaction
* Different learning objectives
* Numerical and categorical behavioral features
* Class imbalance
* Model uncertainty

---

# 4. Dataset

The project uses a tutoring-conversation dataset containing structured session information and transcript-derived features.

### Current training data

```text
Training samples: 35,072
Validation samples: 7,015
```

The dataset contains approximately **398 distinct learning objectives**.

Each response/session contains information including:

### Textual information

* `learning_objective`
* `tutor_text`
* `student_text`
* `transcript_text`

### Session information

* `total_turns`
* `total_words`
* `session_duration_minutes`
* `turns_per_minute`

### Student interaction features

* `student_turns`
* `student_turn_ratio`
* `student_word_ratio`
* `avg_student_words_per_turn`
* `student_short_turn_ratio`
* `student_long_turn_ratio`
* `student_numeric_turn_ratio`
* `student_question_ratio`

### Tutor interaction features

* `tutor_question_ratio`
* `student_response_after_tutor_question_ratio`
* `longest_tutor_streak_ratio`

### Dialogue features

* `speaker_switch_rate`
* `longest_student_streak_ratio`
* `background_turn_ratio`

Additional categorical/binned features are also available.

---

# 5. Target Variable

The prediction target is binary:

```text
0 → Incorrect
1 → Correct
```

The model outputs a probability:

```text
P(student answers correctly)
```

For example:

```text
Probability = 0.87
```

means the model estimates an approximately 87% probability of a correct outcome.

---

# 6. Data Preparation

The original conversation information was transformed into a structured input representation for ModernBERT.

The current best text representation follows this structure:

```text
TASK

[Learning Objective]

==============================

TUTOR

[Tutor Conversation]

==============================

STUDENT

[Student Conversation]

==============================

Predict whether the student's final answer is correct.
```

Noise such as:

```text
[unclear]
[background]
```

was cleaned during text construction.

---

# 7. Why 2048 Tokens?

Initial experiments were conducted with shorter context.

The project moved to **2048 tokens** to preserve more information from longer tutoring conversations.

The 2048-token configuration became part of the current best-performing setup.

---

# 8. Machine Learning Approach

The primary language model is:

## ModernBERT-base

ModernBERT is used to encode the tutoring conversation into contextual representations.

The architecture combines:

```text
                 Tutoring Conversation
                         │
                         ▼
                    Tokenizer
                         │
                         ▼
                    ModernBERT
                         │
                         ▼
                 Text Representation
                         │
             ┌───────────┴───────────┐
             │                       │
       Numerical Features      Categorical Features
             │                       │
             └───────────┬───────────┘
                         ▼
                    Feature Fusion
                         │
                         ▼
                    Classifier
                         │
                         ▼
                    Probability
```

---

# 9. Multimodal Feature Representation

The model does not depend exclusively on textual information.

Three information groups are used:

### A. Text representation

Generated using ModernBERT.

### B. Numerical features

Examples:

```text
student_word_ratio
student_turn_ratio
student_numeric_turn_ratio
speaker_switch_rate
session_duration
student_response_length
```

### C. Categorical features

Examples include discretized/binned conversational characteristics such as:

```text
session duration band
student response length band
student turn share band
tutor questioning band
dialogue switch band
```

This allows the system to combine **semantic information + behavioral interaction information**.

---

# 10. Experimental Development

Several text-representation experiments were performed.

### Original ModernBERT

Validation LogLoss:

**0.5446**

---

### Better Structured Text — 2048 tokens

Validation result:

```text
LogLoss : 0.5416
AUROC   : 0.7242
Accuracy: 0.7294
```

This became the strongest initial configuration.

---

### Student Final Answer Focus

The conversation was modified to explicitly emphasize the later portion of student responses.

Result:

```text
LogLoss : 0.5461
AUROC   : 0.7179
Accuracy: 0.7237
```

Therefore this experiment was rejected.

This is an important research finding because it suggests that simply emphasizing the final student portion did not improve the model.

---

### Repeated Better Structured Text Training

A subsequent run using the same Better Structured Text configuration produced:

```text
Validation LogLoss : 0.5408
Validation AUROC   : 0.7254
Validation Accuracy: 0.7307
```

Therefore the current **best observed validation result** is:

# **LogLoss = 0.5408**

with:

```text
AUROC   = 0.7254
Accuracy = 0.7307
```

Because repeated training produced slightly different results, this difference is treated as training variability rather than automatically attributing the improvement to a new architecture.

---

# 11. Current Model Performance

### Current Best Validation Result

| Metric              |     Result |
| ------------------- | ---------: |
| Validation LogLoss  | **0.5408** |
| Validation AUROC    | **0.7254** |
| Validation Accuracy | **0.7307** |

The validation set contains:

**7,015 samples.**

---

# 12. Classification Analysis

For the current model, the classification report showed:

| Class     | Precision | Recall |     F1 |
| --------- | --------: | -----: | -----: |
| Incorrect |    0.5749 | 0.3474 | 0.4331 |
| Correct   |    0.7633 | 0.8912 | 0.8223 |

Overall:

```text
Accuracy = 0.7294
```

This indicates that the model is considerably better at identifying **correct responses** than **incorrect responses**.

That imbalance becomes an important research observation for the project.

---

# 13. Error Analysis

A dedicated error-analysis pipeline was developed.

The validation predictions include:

```text
true_label
prediction
probability
correct_prediction
```

This allows analysis of:

### False Positives

The model predicts:

```text
Correct
```

but the actual label is:

```text
Incorrect
```

The analysis showed many high-confidence false positives.

For example, some incorrect samples received probabilities above **0.90**.

This suggests that the model can sometimes interpret plausible student reasoning as evidence of correctness even when the final outcome is incorrect.

---

### False Negatives

The model predicts:

```text
Incorrect
```

while the actual label is:

```text
Correct
```

The false-negative analysis showed that many such cases had low predicted probabilities.

This indicates that noisy, incomplete, or short student responses can make correct outcomes difficult to recognize.

---

# 14. Learning Objective Analysis

EduSense also evaluates performance by learning objective.

Examples of objectives with relatively high false-positive rates included topics involving:

* Fractions
* Percentages
* Multiplication
* Decimal reasoning
* Factors
* Rounding
* Ratio
* Sequences

Some objectives showed substantially lower error rates.

This provides an opportunity to identify **topic-specific model weaknesses** rather than evaluating only one overall score.

---

# 15. Confidence Analysis

The model's predicted probability is treated as a confidence signal.

Instead of only showing:

```text
Correct / Incorrect
```

EduSense can show:

```text
Prediction
────────────
87.4%

Confidence
────────────
High
```

This is important because educational AI should distinguish between:

> "The model predicts correct with high confidence"

and

> "The model is uncertain."

---

# 16. Hard Sample Analysis

The current analysis pipeline can identify:

### Highest-confidence false positives

Cases where:

```text
Actual = Incorrect
Prediction probability ≈ 0.90+
```

### Lowest-probability false negatives

Cases where:

```text
Actual = Correct
Prediction probability ≈ 0.30
```

These examples can be displayed in the final dashboard for model auditing.

---

# 17. Explainability

The final system will include an explainability layer.

The goal is not simply:

> "Prediction = 0.87"

but:

> "What signals contributed to this prediction?"

Possible explanation categories include:

```text
Student response patterns
Numerical reasoning signals
Dialogue interaction
Tutor questioning
Learning objective
Conversation characteristics
```

For the final implementation, transformer-specific explainability methods such as **Integrated Gradients** or another validated attribution approach can be used.

---

# 18. Final System Architecture

This is the architecture I recommend you actually build.

```text
                         EDUSENSE
                            │
                    ┌───────┴────────┐
                    │                │
                 Frontend          Backend
                 Next.js           FastAPI
                    │                │
                    │                ▼
                    │          Prediction API
                    │                │
                    │       ┌────────┴────────┐
                    │       │                 │
                    │   ModernBERT       Feature Pipeline
                    │       │                 │
                    │       │          ┌──────┴──────┐
                    │       │          │             │
                    │       │       Numerical    Categorical
                    │       │          │             │
                    │       └──────────┴─────────────┘
                    │                    │
                    │                    ▼
                    │               Classifier
                    │                    │
                    │              Probability
                    │                    │
                    └────────────────────┘
```

---

# 19. Backend

## FastAPI

FastAPI will act as the central backend.

Main responsibilities:

### Prediction

```text
POST /api/predict
```

Input:

```json
{
  "learning_objective": "...",
  "student_text": "...",
  "tutor_text": "..."
}
```

Output:

```json
{
  "probability": 0.874,
  "prediction": 1,
  "confidence": "high"
}
```

---

### Analytics

```text
GET /api/analytics/overview
GET /api/analytics/objectives
```

---

### Error analysis

```text
GET /api/errors/false-positive
GET /api/errors/false-negative
```

---

### Explainability

```text
POST /api/explain
```

---

# 20. Model Assets

Your current model package is already sufficient as the foundation:

```text
models/
│
├── best_model.pt
├── scaler.joblib
├── label_encoders.joblib
│
└── tokenizer/
```

These are the important inference artifacts.

### `best_model.pt`

Contains trained model weights.

### `scaler.joblib`

Applies the same numerical preprocessing used during training.

### `label_encoders.joblib`

Reproduces categorical preprocessing.

### `tokenizer/`

Ensures that inference text is tokenized consistently with training.

---

# 21. Frontend

The frontend will be built using:

* **Next.js**
* **TypeScript**
* **Tailwind CSS**
* **shadcn/ui**
* **Recharts**

The frontend should not directly load the `.pt` model.

Instead:

```text
Next.js
   │
   │ HTTP
   ▼
FastAPI
   │
   ▼
AI Model
```

---

# 22. Frontend Pages

## Dashboard

Shows:

```text
Model Accuracy
AUROC
LogLoss
Prediction Count
High-confidence predictions
```

---

## Analyze Session

Main AI interface.

```text
Learning Objective
        ↓
Tutor Conversation
        ↓
Student Conversation
        ↓
       ANALYZE
        ↓
Prediction
```

---

## Prediction Result

Example:

```text
Student Outcome

87.4%

LIKELY CORRECT

Confidence: HIGH
```

---

## Conversation Intelligence

Shows tutor/student dialogue and extracted interaction characteristics.

---

## Learning Objective Analytics

Interactive charts showing:

* Strong objectives
* Weak objectives
* False-positive rates
* False-negative rates
* Sample counts

---

## Error Analysis

Separate views for:

```text
False Positives
False Negatives
High-confidence errors
Hard samples
```

---

## Explainability

Shows model reasoning signals and feature contributions.

---

# 23. Recommended Final UI

Sidebar:

```text
EDUSENSE

Dashboard
Analyze Session
Student Insights
Learning Objectives
Error Analysis
Explainability
Model Performance
```

Main dashboard:

```text
┌───────────────────────────────────────────────┐
│ EDUSENSE AI                                   │
│                                               │
│ Analyze tutoring conversations with AI        │
│                                               │
│ [ Analyze New Session ]                       │
│                                               │
│ ┌────────┐ ┌────────┐ ┌────────┐              │
│ │ 73.1%  │ │ 72.5%  │ │ 0.541  │              │
│ │Accuracy│ │ AUROC  │ │LogLoss │              │
│ └────────┘ └────────┘ └────────┘              │
│                                               │
│ Learning Objective Performance                │
│ ──────────────────────────────────────────    │
│                                               │
│ Error Distribution                            │
│                                               │
└───────────────────────────────────────────────┘
```

---

# 24. Project Workflow

The final user flow will be:

```text
Teacher / User
      │
      ▼
Enter tutoring conversation
      │
      ▼
Next.js Frontend
      │
      ▼
FastAPI
      │
      ▼
Feature Extraction
      │
      ├───────────────┐
      ▼               ▼
ModernBERT       Structured Features
      │               │
      └───────┬───────┘
              ▼
        Feature Fusion
              │
              ▼
          Classifier
              │
              ▼
        Probability
              │
       ┌──────┴──────┐
       ▼             ▼
 Prediction      Explanation
       │             │
       └──────┬──────┘
              ▼
        EduSense UI
```

---

# 25. Evaluation Plan

Primary metric:

## LogLoss

Because the system predicts probabilities rather than only binary labels.

Secondary metrics:

* AUROC
* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix

Additional analysis:

* Confidence calibration
* False-positive rate
* False-negative rate
* Learning-objective-wise performance
* Hard-sample analysis

---

# 26. Baselines

The project already has meaningful baselines.

### Baseline 1

Traditional ML:

**TF-IDF / Logistic Regression**

### Baseline 2

ModernBERT without improved text structuring.

### Proposed model

**ModernBERT + structured tutoring conversation + numerical/categorical interaction features**

This gives the project a proper experimental progression:

```text
Traditional ML
      ↓
Transformer baseline
      ↓
Structured Transformer
      ↓
Multifeature AI system
```

---

# 27. Research Contribution

The contribution of EduSense is not simply:

> "We used ModernBERT."

The project investigates whether **combining conversational language representations with structured tutoring-interaction features** can improve prediction of student learning outcomes.

The project also studies:

1. How conversation representation affects prediction.
2. How noisy tutoring conversations influence model performance.
3. Where the model makes confident mistakes.
4. Which learning objectives are difficult for the model.
5. Whether behavioral interaction features provide useful information beyond text.

This gives the project both **applied and research-oriented value**.

---

# 28. Expected Deliverables

By the final project presentation:

### AI/ML

* Trained ModernBERT model
* Preprocessing pipeline
* Evaluation results
* Error analysis
* Explainability analysis

### Backend

* FastAPI service
* Model inference API
* Feature-processing API
* Analytics endpoints

### Frontend

* Interactive EduSense dashboard
* Session analysis interface
* Prediction visualization
* Error analysis
* Learning-objective analytics
* Explainability interface

### Documentation

* Project report
* Model methodology
* Dataset description
* Experimental results
* Limitations
* Future work

---

# 29. Future Improvements

These are **future work**, not things you need to finish before the first demo:

### Model improvements

* Cross-validation
* Better feature fusion
* Calibration
* Ensemble models
* Alternative transformer architectures

### Educational intelligence

* Student progress tracking
* Personalized lesson recommendations
* Knowledge-gap detection
* Longitudinal student modeling

### Explainability

* Integrated Gradients
* SHAP for structured features
* Counterfactual explanations

---

# 30. Limitations

We should be honest about these in the report.

The current model has:

* Moderate AUROC rather than near-perfect discrimination.
* Higher performance on correct responses than incorrect responses.
* High-confidence false positives.
* Sensitivity to transcript quality.
* Potential distribution shift between validation data and unseen competition/test data.

Therefore EduSense should be presented as a **decision-support system**, not as a replacement for teachers.

---

# 31. Project Timeline

### Phase 1 — Data & Baseline

* Dataset analysis
* Feature engineering
* Traditional ML baseline

### Phase 2 — Deep Learning

* ModernBERT implementation
* Structured text
* Numerical/categorical feature integration

### Phase 3 — Evaluation

* Error analysis
* Confidence analysis
* Learning-objective analysis

### Phase 4 — Backend

* FastAPI
* Model loading
* Preprocessing
* Prediction API

### Phase 5 — Frontend

* Dashboard
* Session analysis
* Analytics
* Explainability

### Phase 6 — Finalization

* Integration
* Testing
* Documentation
* Presentation/demo

---

# 32. Final Project Identity

### Name

# **EDUSENSE AI**

### Full Title

> **EduSense: Explainable Student Learning Outcome Prediction from Tutoring Conversations Using ModernBERT and Interaction Features**

### One-line pitch

> **EduSense analyzes tutor–student conversations using NLP and interaction features to predict learning outcomes, explain model decisions, and identify difficult learning objectives.**

---

# 33. What You Actually Need To Do Now

**Model side থেকে আবার শূন্য থেকে শুরু করার দরকার নেই।**



```text
best_model.pt          ✓
scaler.joblib          ✓
label_encoders.joblib  ✓
tokenizer/             ✓
feature definitions    ✓
validation predictions ✓
error analysis         ✓
training history       ✓
```

তাই এখন primary কাজ:

```text
                CURRENT STATUS
                     │
                     ▼
          ┌────────────────────┐
          │   ML ENGINE        │
          │   ALREADY BUILT    │
          └─────────┬──────────┘
                    │
                    ▼
               FastAPI
                    │
                    ▼
              Next.js UI
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
       Predict   Explain   Analytics
                    │
                    ▼
              EDUSENSE AI
```


Close
