# Contributing to Student Eye Drowsiness Detection System (SEDDS)

First off, thank you for considering contributing to SEDDS! It's people like you that make this project better for everyone.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, screenshots, etc.)
- **Describe the behavior you observed** and what you expected
- **Include your environment details** (OS, Python version, browser, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any similar features** in other projects if applicable

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the coding style** used throughout the project
3. **Write clear commit messages** describing your changes
4. **Include tests** if you're adding new functionality
5. **Update documentation** as needed
6. **Ensure all tests pass** before submitting

## 💻 Development Setup

1. Fork and clone the repository
```bash
git clone https://github.com/yourusername/Student-Eye-Drowsiness-Detection-System.git
cd Student-Eye-Drowsiness-Detection-System
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Create a new branch for your feature
```bash
git checkout -b feature/your-feature-name
```

## 📝 Coding Standards

### Python Code Style

- Follow **PEP 8** style guide
- Use **meaningful variable and function names**
- Add **docstrings** to all functions and classes
- Keep functions **small and focused** (single responsibility)
- Use **type hints** where appropriate

Example:
```python
def calculate_ear(eye_points: list) -> float:
    """
    Calculate Eye Aspect Ratio for given eye points.
    
    Args:
        eye_points: List of (x, y) coordinates for eye landmarks
        
    Returns:
        float: Calculated EAR value
    """
    # Implementation here
    pass
```

### JavaScript Code Style

- Use **ES6+ syntax** where appropriate
- Use **const** and **let** instead of **var**
- Add **comments** for complex logic
- Keep functions **small and focused**

### HTML/CSS

- Use **semantic HTML5** elements
- Follow **Bootstrap conventions** for styling
- Keep CSS **organized and commented**
- Ensure **responsive design** principles

## 🧪 Testing

- Write tests for new features
- Ensure existing tests pass
- Test on multiple browsers (Chrome, Firefox, Edge)
- Test camera functionality on different devices

## 📚 Documentation

- Update README.md if you change functionality
- Add docstrings to new functions/classes
- Update API documentation if applicable
- Include code comments for complex logic

## 🔄 Git Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when relevant

Examples:
```
Add MediaPipe integration for face detection
Fix timezone issue in session start time
Update README with installation instructions
Refactor drowsiness detection algorithm
```

## 🎯 Priority Areas for Contribution

We especially welcome contributions in these areas:

1. **Performance Optimization**
   - GPU acceleration support
   - Further algorithm optimization
   - Memory usage reduction

2. **New Features**
   - Mobile app development
   - Advanced analytics dashboard
   - Export functionality (CSV/PDF)
   - Multi-user support

3. **Testing**
   - Unit tests
   - Integration tests
   - Browser compatibility tests

4. **Documentation**
   - API documentation
   - Video tutorials
   - Translation to other languages

5. **Bug Fixes**
   - Camera compatibility issues
   - Cross-platform bugs
   - UI/UX improvements

## 📋 Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the version number following [Semantic Versioning](https://semver.org/)
3. The PR will be merged once you have approval from maintainers

## 🐛 Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `performance`: Performance improvements
- `question`: Further information requested

## 💬 Communication

- Be respectful and constructive
- Ask questions if something is unclear
- Provide context in discussions
- Be patient with response times

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in all interactions.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Unacceptable behavior includes:**
- Harassment or discriminatory language
- Trolling or insulting comments
- Public or private harassment
- Publishing others' private information

## 📞 Questions?

Feel free to reach out:
- Open an issue with the `question` label
- Email: kmglm04718@gmail.com

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

---

**Happy Coding! 🚀**
