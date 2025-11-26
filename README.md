# FashionBench 👗✨

**The world's first domain-specific benchmark suite for evaluating LLM performance in the global fashion industry.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 🌟 What is FashionBench?

FashionBench is a comprehensive evaluation suite designed to test Large Language Models (LLMs) on tasks critical to the fashion industry. Unlike general-purpose benchmarks, FashionBench focuses on domain-specific capabilities that fashion brands, influencers, and e-commerce platforms need most.

### Why Fashion Needs Domain-Specific Evals

The fashion industry has unique requirements that general LLM benchmarks don't capture:

- **Trend Detection**: Understanding viral aesthetics, runway signals, and cultural movements
- **Product Knowledge**: Extracting structured data from unstructured content (brands, prices, links)
- **Style Understanding**: Classifying complex aesthetics (quiet luxury, dopamine dressing, etc.)
- **Content Creation**: Writing engaging captions that resonate with fashion audiences
- **Social Media Fluency**: Decoding hashtags, affiliate links, and influencer marketing tactics
- **Brand Voice**: Maintaining consistency across luxury, streetwear, sustainable fashion contexts

FashionBench fills this gap by providing targeted evaluations that matter for real-world fashion applications.

---

## 📊 Evaluation Categories

| Evaluation | Description | Examples |
|-----------|-------------|----------|
| **Trend Detection** | Identify emerging fashion trends from social media, runway shows, and market signals | Barbiecore, quiet luxury, Y2K revival |
| **Product Extraction** | Extract structured product information (brand, price, links, codes) from posts | Parse "Zara blazer $89.99 code STYLE15" |
| **Style Classification** | Classify outfits into aesthetic categories | Corporate, streetwear, boho, athleisure |
| **Fashion Writing** | Generate engaging, on-brand fashion content and captions | Transform "cute outfit" into compelling copy |
| **Hashtag Understanding** | Decode fashion-specific hashtags and their cultural context | #OOTD, #GRWM, #LTK, #ThriftFlip |
| **Affiliate Detection** | Identify monetization strategies and sponsored content | Detect LTK links, discount codes, #ad |

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fashionbench.git
cd fashionbench

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

Run all evaluations on a model:

```bash
python run_fashionbench.py --model claude-3-sonnet
```

Run a specific evaluation:

```bash
python run_fashionbench.py --model gpt-4 --eval trend_detection
```

List all available evaluations:

```bash
python run_fashionbench.py --list
```

Show verbose output:

```bash
python run_fashionbench.py --model simulated --verbose
```

Get information about FashionBench:

```bash
python run_fashionbench.py info
```

---

## 📁 Repository Structure

```
fashionbench/
├── datasets/                      # Synthetic evaluation datasets
│   ├── trend_detection.jsonl
│   ├── product_extraction.jsonl
│   ├── style_classification.jsonl
│   ├── hashtag_understanding.jsonl
│   ├── caption_rewriting.jsonl
│   └── affiliate_detection.jsonl
├── evals/                         # Evaluation scripts
│   ├── trend_detection_eval.py
│   ├── product_extraction_eval.py
│   ├── style_eval.py
│   ├── writing_eval.py
│   ├── hashtag_eval.py
│   └── affiliate_eval.py
├── scoring/                       # Scoring metrics
│   └── metrics.py
├── run_fashionbench.py           # Main runner script
├── requirements.txt              # Python dependencies
├── LICENSE                       # MIT License
└── README.md                     # This file
```

---

## 🎯 How It Works

### 1. Dataset Format

All datasets are in JSONL format with the following structure:

```json
{
  "id": 1,
  "text": "Input text or context",
  "expected": "Expected output or structured result",
  "category": "evaluation_category"
}
```

### 2. Evaluation Process

Each evaluation:
1. Loads its corresponding dataset
2. Queries the specified model (simulated by default)
3. Compares model output to expected results
4. Calculates scores using domain-specific metrics
5. Returns pass/fail status and detailed results

### 3. Scoring Metrics

FashionBench uses custom metrics tailored to fashion content:

- **Exact Match**: Binary exact string matching
- **Partial Match**: Word overlap with Jaccard similarity
- **Fashion Similarity**: Domain-aware matching with fashion synonym understanding
  - Recognizes "luxury" ↔ "high-end", "boho" ↔ "bohemian", etc.
  - Accounts for fashion terminology variations

---

## 🔧 Adding Custom Evaluations

To add a new evaluation:

1. **Create a dataset** in `datasets/your_eval.jsonl`:
```json
{"id": 1, "text": "Your input", "expected": "Expected output", "category": "your_category"}
```

2. **Create an evaluation script** in `evals/your_eval.py`:
```python
def evaluate_your_task(model_name: str = "simulated", dataset_path: str = None) -> dict:
    # Load dataset
    # Run model
    # Score results
    # Return metrics
    pass
```

3. **Register it** in `run_fashionbench.py`:
```python
EVALUATIONS["your_eval"] = {
    "name": "Your Evaluation",
    "description": "What it tests",
    "function": evaluate_your_task
}
```

---

## 📈 Example Output

```
    ╔═══════════════════════════════════════════════════════════╗
    ║                     FASHIONBENCH                          ║
    ║          Fashion Industry LLM Evaluation Suite            ║
    ╚═══════════════════════════════════════════════════════════╝

Model: claude-3-sonnet
Mode: Full Suite

✓ Trend Detection completed
✓ Product Extraction completed
✓ Style Classification completed
✓ Fashion Writing completed
✓ Hashtag Understanding completed
✓ Affiliate Detection completed

                        FashionBench Results
╭────────────────────────┬──────────┬─────────┬───────────┬──────────────╮
│ Evaluation             │ Examples │ Passed  │ Avg Score │ Status       │
├────────────────────────┼──────────┼─────────┼───────────┼──────────────┤
│ Trend Detection        │    8     │   7/8   │   0.850   │ ✓ Excellent  │
│ Product Extraction     │    8     │   6/8   │   0.775   │ ✓ Excellent  │
│ Style Classification   │   10     │   9/10  │   0.920   │ ✓ Excellent  │
│ Fashion Writing        │   10     │   8/10  │   0.780   │ ○ Good       │
│ Hashtag Understanding  │   10     │   9/10  │   0.890   │ ✓ Excellent  │
│ Affiliate Detection    │   10     │   8/10  │   0.825   │ ✓ Excellent  │
├────────────────────────┼──────────┼─────────┼───────────┼──────────────┤
│ OVERALL                │   56     │  47/56  │   0.840   │ Summary      │
╰────────────────────────┴──────────┴─────────┴───────────┴──────────────╯

╭─────────────────────────────────────────────────────────╮
│ Summary                                                 │
├─────────────────────────────────────────────────────────┤
│ Overall Grade: A                                        │
│ Average Score: 0.840                                    │
│                                                         │
│ Excellent performance on fashion domain tasks!         │
╰─────────────────────────────────────────────────────────╯
```

---

## 🎨 Use Cases

### For Fashion Brands
- Evaluate LLMs before deploying for product descriptions
- Test content generation quality for social media
- Validate trend analysis capabilities

### For Influencers & Creators
- Assess AI writing tools for caption generation
- Benchmark hashtag understanding
- Test product information extraction accuracy

### For E-commerce Platforms
- Validate product data parsing
- Test style classification for recommendation engines
- Evaluate affiliate link detection systems

### For AI Researchers
- Benchmark domain-specific performance
- Compare models on fashion-industry tasks
- Develop fashion-focused fine-tuning datasets

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Add new evaluation categories**: Submit PRs with new datasets and eval scripts
2. **Improve metrics**: Propose better scoring functions for fashion content
3. **Expand datasets**: Contribute more diverse examples
4. **Fix bugs**: Report issues and submit fixes
5. **Documentation**: Improve guides and examples

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Creator

**Ortal** - Vibe Coder & Vibe Solver

Building tools at the intersection of AI and fashion.

- Email: ortal@onsight-analytics.com
- Company: OnSight Analytics

---

## 🙏 Acknowledgments

- Fashion industry professionals who provided domain expertise
- The open-source community for foundational tools
- All contributors who help improve FashionBench

---

## 📚 Citation

If you use FashionBench in your research, please cite:

```bibtex
@software{fashionbench2025,
  author = {Ortal},
  title = {FashionBench: Domain-Specific LLM Evaluation for Fashion Industry},
  year = {2025},
  url = {https://github.com/yourusername/fashionbench}
}
```

---

## 🗺️ Roadmap

- [ ] Add real LLM API integration (Claude, GPT-4, Gemini)
- [ ] Expand datasets to 50+ examples per category
- [ ] Add multilingual support (fashion content in multiple languages)
- [ ] Create leaderboard for model comparisons
- [ ] Add visual evaluation (outfit assessment from images)
- [ ] Integrate with popular fashion APIs
- [ ] Build web interface for easier testing

---

## ❓ FAQ

**Q: Can I use my own LLM API keys?**
A: Yes! The evaluation scripts are designed to be extended. Simply modify the `simulate_model_response` functions to call your actual API.

**Q: Are the datasets real influencer data?**
A: No, all datasets are synthetic to protect privacy and avoid copyright issues.

**Q: How do I interpret the scores?**
A: Scores range from 0.0 to 1.0:
- 0.8+: Excellent
- 0.7-0.8: Good
- 0.6-0.7: Moderate
- <0.6: Needs improvement

**Q: Can I use this commercially?**
A: Yes, FashionBench is MIT licensed and free for commercial use.

---

**Built with ❤️ for the fashion community**
