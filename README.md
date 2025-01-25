# 🧠 RAT (Retrieval Augmented Thinking)

> *Enhancing AI responses through structured reasoning and knowledge retrieval*

RAT is a powerful tool that improves AI responses by leveraging Google Gemini 2.0's Flash Thinking capabilities to guide other models through a structured thinking process.

## 💡 Origin & Ideation

The idea for RAT emerged from exploring ways to separate the reasoning process from response generation. Using Gemini 2.0's Flash Thinking feature, we can access the model's internal thought process before generating the final response. This insight led to the development of a two-stage approach that combines Gemini's exceptional reasoning abilities with various response models.

## How It Works

RAT employs a two-stage approach:
1. **Reasoning Stage** (Gemini 2.0): Generates detailed reasoning and analysis for each query using Flash Thinking
2. **Response Stage** (OpenRouter): Utilizes the reasoning context to provide informed, well-structured answers

This approach ensures more thoughtful, contextually aware, and reliable responses.

## 🎯 Features

- 🤖 **Model Selection**: Flexibility to choose from various OpenRouter models
- 🧠 **Reasoning Visibility**: Toggle visibility of the AI's thinking
- 🔄 **Context Awareness**: Maintains conversation context for more coherent interactions

## ⚙️ Requirements

• Python 3.11 or higher  
• A .env file containing:
  ```plaintext
  GEMINI_API_KEY=your_gemini_api_key_here
  OPENROUTER_API_KEY=your_openrouter_api_key_here
  ```

## 🚀 Installation
Standalone installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Doriandarko/RAT-retrieval-augmented-thinking.git
   cd RAT-retrieval-augmented-thinking
   ```


2. Install as a local package:
   ```bash
   pip install -e .
   ```

This will install RAT as a command-line tool, allowing you to run it from anywhere by simply typing `rat`!

## 📖 Usage

1. Ensure your .env file is configured with:
   ```plaintext
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

2. Run RAT from anywhere:
   ```bash
   rat
   ```

3. Available commands:
   - Enter your question to get a reasoned response
   - Use "model <name>" to switch OpenRouter models
   - Type "reasoning" to show/hide the thinking process
   - Type "quit" to exit



## 🚀 Versions
You can run the script using:
```bash
uv run rat.py
```

## 🤝 Contributing

Interested in improving RAT?

1. Fork the repository
2. Create your feature branch
3. Make your improvements
4. Submit a Pull Request

## 📜 License

This project is available under the MIT License. See the [LICENSE](LICENSE) file for details.

If you use this codebase in your projects, please include appropriate credits:

```plaintext
This project uses RAT (Retrieval Augmented Thinking) by Skirano
GitHub: https://github.com/yourusername/rat
```
---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Doriandarko/RAT-retrieval-augmented-thinking&type=Date)](https://star-history.com/#Doriandarko/RAT-retrieval-augmented-thinking&Date)
