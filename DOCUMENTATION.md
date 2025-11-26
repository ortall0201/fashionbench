# FashionBench Documentation

## Repository Overview

**FashionBench** is the world's first domain-specific benchmark suite for evaluating LLM performance in the global fashion industry. Created by Ortal (Vibe Coder & Vibe Solver) at OnSight Analytics.

---

## 📁 Complete File Structure

```
fashionbench/
├── datasets/                          (6 JSONL files with synthetic data)
│   ├── trend_detection.jsonl         (8 examples)
│   ├── product_extraction.jsonl      (8 examples)
│   ├── style_classification.jsonl    (10 examples)
│   ├── hashtag_understanding.jsonl   (10 examples)
│   ├── caption_rewriting.jsonl       (10 examples)
│   └── affiliate_detection.jsonl     (10 examples)
├── evals/                            (6 Python evaluation scripts)
│   ├── trend_detection_eval.py       - Identifies emerging fashion trends
│   ├── product_extraction_eval.py    - Extracts brands, prices, links, codes
│   ├── style_eval.py                 - Classifies fashion aesthetics
│   ├── writing_eval.py               - Evaluates caption quality
│   ├── hashtag_eval.py               - Understands fashion hashtags
│   └── affiliate_eval.py             - Detects monetization strategies
├── scoring/
│   └── metrics.py                    - Custom fashion-specific metrics
├── run_fashionbench.py               - Main CLI runner (Typer + Rich)
├── requirements.txt                  - Python dependencies
├── LICENSE                           - MIT License
├── README.md                         - Main documentation
└── DOCUMENTATION.md                  - This file
```

**Total: 17 files, 56 evaluation examples across 6 categories**

---

## 🎯 What Was Built

### 1. Datasets (6 JSONL files)

Each dataset contains 5-10 synthetic examples in JSONL format:

- **trend_detection.jsonl**: Fashion trend identification from social media, runway shows, market signals
- **product_extraction.jsonl**: Structured product info extraction (brand, price, links, discount codes)
- **style_classification.jsonl**: Outfit style categorization (corporate, streetwear, boho, etc.)
- **hashtag_understanding.jsonl**: Fashion hashtag interpretation (#OOTD, #GRWM, #LTK, etc.)
- **caption_rewriting.jsonl**: Transform basic captions into engaging fashion content
- **affiliate_detection.jsonl**: Identify affiliate links, sponsored content, discount codes

### 2. Evaluation Scripts (6 Python files)

Each evaluation script includes:
- Dataset loading functionality
- Simulated model response (can be replaced with real API calls)
- Scoring using custom metrics
- Detailed output and pass/fail determination
- Command-line interface support
- Complete documentation and comments

**Key Functions:**
- `load_dataset()` - Loads JSONL data
- `simulate_model_response()` - Mock implementation (replace with real LLM API)
- `evaluate_*()` - Main evaluation function
- Individual scoring logic tailored to each task

### 3. Scoring Metrics (metrics.py)

Custom fashion-specific scoring functions:

**Core Metrics:**
- `exact_match()` - Binary exact string matching
- `partial_match()` - Word overlap using Jaccard similarity
- `fashion_similarity()` - Domain-aware matching with fashion synonyms
  - Recognizes: luxury ↔ high-end, boho ↔ bohemian, trendy ↔ fashionable
  - Accounts for fashion terminology variations
- `list_overlap_score()` - Compare lists of items
- `calculate_accuracy()` - Overall accuracy from results
- `weighted_score()` - Weighted average of multiple scores

**Fashion Synonym Groups:**
```python
luxury → [high-end, premium, upscale, designer]
casual → [relaxed, laid-back, comfortable, easy]
elegant → [sophisticated, refined, polished, chic]
trendy → [fashionable, stylish, on-trend, contemporary]
vintage → [retro, classic, throwback, timeless]
minimalist → [simple, clean, understated, minimal]
bohemian → [boho, hippie, free-spirited, eclectic]
streetwear → [urban, street-style, casual-cool]
```

### 4. Main Runner (run_fashionbench.py)

Beautiful CLI interface using Typer and Rich:

**Features:**
- Command-line argument parsing
- Model selection
- Individual or full suite evaluation
- Rich formatted output (tables, colors, status indicators)
- Progress tracking with spinners
- Grading system (A/B/C/D based on average score)
- Detailed results tables

**Commands:**
```bash
# Run evaluations
python run_fashionbench.py run [OPTIONS]

# Show information
python run_fashionbench.py info
```

---

## 🚀 Installation & Usage

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fashionbench.git
cd fashionbench

# Install dependencies
pip install -r requirements.txt
```

### Usage Commands

```bash
# List all available evaluations
python run_fashionbench.py run --list

# Run all evaluations on a model
python run_fashionbench.py run --model claude-3-sonnet

# Run specific evaluation
python run_fashionbench.py run --model gpt-4 --eval trend_detection

# Show verbose output (detailed)
python run_fashionbench.py run --model simulated --verbose

# Show information about FashionBench
python run_fashionbench.py info

# Get help
python run_fashionbench.py run --help
```

---

## 📊 Evaluation Categories Explained

### 1. Trend Detection
**Purpose**: Test LLM ability to identify emerging fashion trends from various data sources.

**Examples:**
- Social media signals (barbiecore, Y2K revival)
- Runway show analysis (oversized tailoring, power dressing)
- Market trends (luxury streetwear fusion)

**Metrics**: Partial match + fashion similarity

### 2. Product Extraction
**Purpose**: Extract structured product information from unstructured text.

**Examples:**
- Brand: "Zara oversized blazer"
- Price: "$89.99"
- Discount codes: "STYLE15"
- Links and affiliate platforms: "LTK", "ShopLTK"

**Metrics**: Field-level accuracy scoring

### 3. Style Classification
**Purpose**: Classify outfit descriptions into aesthetic categories.

**Categories:**
- Corporate/Professional
- Grunge/Rock
- Bohemian/Boho
- Athleisure/Sporty
- Quiet Luxury/Minimalist
- Streetwear/Urban
- Coquette/Feminine
- Hypebeast
- Coastal/Resort
- Classic/Timeless

**Metrics**: Exact match with fashion similarity fallback

### 4. Fashion Writing
**Purpose**: Evaluate quality of fashion content generation and caption rewriting.

**Evaluation Criteria:**
- Length and substance (50+ characters)
- Elevated vocabulary usage
- Structure (multiple sentences/clauses)
- Semantic similarity to expected output

**Metrics**: Composite quality score

### 5. Hashtag Understanding
**Purpose**: Test knowledge of fashion-specific hashtags and their meanings.

**Examples:**
- #OOTD → Outfit Of The Day
- #GRWM → Get Ready With Me
- #LTK → LikeToKnowIt (affiliate)
- #ThriftFlip → Thrifted item upcycle

**Metrics**: Multi-component scoring (meaning, category, purpose)

### 6. Affiliate Detection
**Purpose**: Identify affiliate marketing and monetization strategies.

**Detection Targets:**
- Affiliate platforms (LTK, Amazon)
- Discount codes
- Sponsored content markers (#ad, #gifted)
- Brand partnerships
- Organic vs. monetized content

**Metrics**: Component-based accuracy

---

## 🔧 Extending FashionBench

### Adding a New Evaluation

**Step 1: Create Dataset**
Create `datasets/your_eval.jsonl`:
```json
{"id": 1, "text": "Your input", "expected": "Expected output", "category": "your_category"}
{"id": 2, "text": "Another input", "expected": "Another output", "category": "your_category"}
```

**Step 2: Create Evaluation Script**
Create `evals/your_eval.py`:
```python
import jsonlines
from pathlib import Path
from scoring.metrics import exact_match, fashion_similarity

def load_dataset(dataset_path: str) -> list:
    examples = []
    with jsonlines.open(dataset_path) as reader:
        for obj in reader:
            examples.append(obj)
    return examples

def simulate_model_response(example: dict, model_name: str) -> str:
    # Your model logic here
    return "model output"

def evaluate_your_task(model_name: str = "simulated", dataset_path: str = None) -> dict:
    if dataset_path is None:
        dataset_path = Path(__file__).parent.parent / "datasets" / "your_eval.jsonl"

    examples = load_dataset(str(dataset_path))
    results = []
    total_score = 0

    for example in examples:
        model_output = simulate_model_response(example, model_name)
        expected = example["expected"]
        score = exact_match(model_output, expected)
        total_score += score

        results.append({
            "id": example["id"],
            "expected": expected,
            "model_output": model_output,
            "score": score
        })

    avg_score = total_score / len(examples) if examples else 0
    passed = sum(1 for r in results if r["score"] >= 0.7)

    return {
        "eval_name": "Your Task",
        "model": model_name,
        "total_examples": len(examples),
        "passed": passed,
        "avg_score": avg_score,
        "results": results
    }
```

**Step 3: Register Evaluation**
Edit `run_fashionbench.py` and add to `EVALUATIONS` dict:
```python
from evals.your_eval import evaluate_your_task

EVALUATIONS["your_eval"] = {
    "name": "Your Evaluation",
    "description": "What it tests",
    "function": evaluate_your_task
}
```

### Adding Real LLM API Integration

Replace the `simulate_model_response()` function in any eval script:

```python
# Example with Anthropic Claude
import anthropic

def simulate_model_response(example: dict, model_name: str) -> str:
    client = anthropic.Anthropic(api_key="your-api-key")

    message = client.messages.create(
        model=model_name,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": example["text"]}
        ]
    )

    return message.content[0].text
```

---

## 📈 Scoring & Grading

### Score Interpretation

**Individual Example Scores** (0.0 to 1.0):
- 1.0 = Perfect match
- 0.8+ = Excellent
- 0.7-0.8 = Good
- 0.6-0.7 = Moderate
- <0.6 = Needs improvement

**Pass Threshold**: 0.7 by default (0.6 for writing eval)

**Overall Grades**:
- **A** (0.8+): Excellent performance on fashion domain tasks
- **B** (0.7-0.8): Good performance with room for improvement
- **C** (0.6-0.7): Moderate performance, consider fine-tuning
- **D** (<0.6): Needs significant improvement for fashion tasks

---

## 🎨 Use Cases

### For Fashion Brands
- Evaluate LLMs before deploying for product descriptions
- Test content generation quality for social media
- Validate trend analysis capabilities
- Benchmark different models for fashion-specific tasks

### For Influencers & Creators
- Assess AI writing tools for caption generation
- Benchmark hashtag understanding
- Test product information extraction accuracy
- Validate affiliate link detection

### For E-commerce Platforms
- Validate product data parsing accuracy
- Test style classification for recommendation engines
- Evaluate affiliate link detection systems
- Build better product search and categorization

### For AI Researchers
- Benchmark domain-specific performance
- Compare models on fashion-industry tasks
- Develop fashion-focused fine-tuning datasets
- Publish research on fashion AI capabilities

---

## 💡 Technical Implementation Details

### Dependencies
- **jsonlines**: JSONL file parsing
- **python-dotenv**: Environment variable management
- **rich**: Beautiful terminal formatting
- **typer**: CLI framework

### Code Architecture

**Modular Design:**
- Datasets are decoupled from evaluation logic
- Metrics are reusable across evaluations
- Each evaluation is independently runnable
- Easy to extend with new categories

**Key Design Patterns:**
- Separation of concerns (data, logic, presentation)
- Template pattern for evaluations
- Strategy pattern for metrics
- Facade pattern for CLI

### Performance Considerations
- Datasets loaded once per evaluation
- Minimal dependencies for fast installation
- No external API calls in default mode
- Efficient scoring algorithms

---

## 🐛 Known Issues & Limitations

1. **Unicode Display Issue**: Box-drawing characters in CLI headers may not display correctly on some Windows terminals. Works fine in Windows Terminal, VS Code terminal, or Linux/Mac.

2. **Simulated Responses**: Default implementation uses keyword-based simulation. Replace with actual LLM API calls for real evaluation.

3. **Dataset Size**: Current datasets have 5-10 examples each. For production use, expand to 50+ examples per category.

4. **Language**: Currently English only. Multilingual support planned for future releases.

5. **Visual Content**: Text-only evaluation. Image-based fashion assessment not yet implemented.

---

## 🗺️ Roadmap

- [ ] Add real LLM API integration (Claude, GPT-4, Gemini)
- [ ] Expand datasets to 50+ examples per category
- [ ] Add multilingual support (fashion content in multiple languages)
- [ ] Create public leaderboard for model comparisons
- [ ] Add visual evaluation (outfit assessment from images)
- [ ] Integrate with popular fashion APIs
- [ ] Build web interface for easier testing
- [ ] Add more evaluation categories (color matching, outfit recommendations, etc.)
- [ ] Implement automated dataset generation
- [ ] Create fine-tuning datasets for fashion models

---

## 📚 Citation

If you use FashionBench in your research, please cite:

```bibtex
@software{fashionbench2025,
  author = {Ortal},
  title = {FashionBench: Domain-Specific LLM Evaluation for Fashion Industry},
  year = {2025},
  url = {https://github.com/yourusername/fashionbench},
  note = {World's first domain-specific benchmark suite for fashion industry LLMs}
}
```

---

## 👤 Creator & Contact

**Ortal** - Vibe Coder & Vibe Solver

Building tools at the intersection of AI and fashion.

- **Email**: ortal@onsight-analytics.com
- **Company**: OnSight Analytics
- **GitHub**: [fashionbench repository](https://github.com/yourusername/fashionbench)

For questions, suggestions, or collaborations, please reach out via email.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for complete details.

You are free to:
- Use commercially
- Modify
- Distribute
- Use privately

---

## 🙏 Acknowledgments

- Fashion industry professionals who provided domain expertise
- The open-source community for foundational tools (Rich, Typer, jsonlines)
- All contributors who help improve FashionBench
- Early adopters and testers providing valuable feedback

---

**Built with ❤️ for the fashion community**

*Last Updated: January 2025*
