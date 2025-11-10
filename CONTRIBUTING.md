# Contributing to DMWG Code Instructions

Thank you for your interest in contributing to the DMWG Code Instructions repository! This document provides guidelines for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Contribution Guidelines](#contribution-guidelines)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior by opening an issue.

## How Can I Contribute?

### Reporting Bugs

If you find a bug or error in the documentation:

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear, descriptive title
   - Steps to reproduce the problem
   - Expected vs actual behavior
   - Your environment (OS, software versions)
   - Screenshots if applicable

### Suggesting Enhancements

We welcome suggestions for:

- New tool documentation
- Improved setup instructions
- Additional examples and use cases
- Better organization of content

Please create an issue with:
- Clear description of the enhancement
- Use cases and benefits
- Example implementation (if applicable)

### Contributing Documentation

Documentation contributions are highly valued! You can:

- Fix typos and grammatical errors
- Improve clarity and readability
- Add missing information
- Update outdated content
- Add examples and tutorials
- Translate content

### Contributing Code Examples

If you have working examples or scripts:

- Ensure they are well-commented
- Include clear usage instructions
- Test them thoroughly
- Provide example input/output
- Follow existing code style

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/DMWG-code-instructions.git
   cd DMWG-code-instructions
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** following the guidelines below
5. **Commit your changes** with clear commit messages
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Submit a pull request** to the main repository

## Contribution Guidelines

### Documentation Standards

- Use clear, concise language
- Follow Markdown formatting conventions
- Include code blocks with syntax highlighting
- Add links to external resources where appropriate
- Keep line length reasonable (80-100 characters preferred)
- Use relative links for internal references

### Code Examples

- Test all code examples before submitting
- Include necessary imports and dependencies
- Add comments explaining non-obvious steps
- Follow language-specific best practices
- Include expected output or results

### File Organization

- Place files in appropriate directories
- Create new subdirectories if needed for organization
- Update main README.md if adding new sections
- Maintain consistent naming conventions

### Tool Documentation Template

When adding new tool documentation, include:

1. **Overview**: Brief description of the tool
2. **Installation**: Step-by-step installation instructions
3. **Configuration**: Required configuration steps
4. **Usage**: Basic usage examples
5. **Advanced Topics**: Complex scenarios (if applicable)
6. **Troubleshooting**: Common issues and solutions
7. **Resources**: Links to official documentation
8. **Citation**: How to cite the tool

## Style Guidelines

### Markdown

- Use ATX-style headers (`#`, `##`, `###`)
- Use fenced code blocks with language specification
- Use bullet lists for unordered items
- Use numbered lists for sequential steps
- Use **bold** for emphasis, *italics* for technical terms
- Use `code` formatting for commands, file names, and code elements

### Code Blocks

```bash
# Good: Include language specifier and comments
# This command installs the package
pip install package-name
```

### Links

- Use descriptive link text: `[MadDM Documentation](https://example.com)`
- Not just: `Click [here](https://example.com)`

## Commit Messages

Write clear, descriptive commit messages:

### Format

```
Short summary (50 chars or less)

More detailed explanatory text, if necessary. Wrap it to 72 characters.
Explain the problem that this commit is solving and why this approach
was chosen.

- Bullet points are okay
- Use present tense: "Add feature" not "Added feature"
- Use imperative mood: "Fix bug" not "Fixes bug"
```

### Examples

Good:
```
Add MadAnalysis5 installation guide

Include detailed steps for installing MadAnalysis5 on Ubuntu and CentOS.
Add troubleshooting section for common installation issues.
```

Not ideal:
```
updated docs
```

## Pull Request Process

1. **Update documentation** - Ensure README.md and relevant docs reflect your changes
2. **Check for conflicts** - Rebase your branch if needed
3. **Test thoroughly** - Verify all code examples work
4. **Describe your changes** - Use the PR template (if available)
5. **Link related issues** - Reference issues using #issue-number
6. **Be responsive** - Address review comments promptly

### PR Title Format

Use clear, descriptive titles:
- `Add: CheckMATE installation instructions`
- `Fix: Broken link in MadDM README`
- `Update: micrOMEGAs version information`
- `Docs: Improve clarity in DMWG_codes README`

### PR Description

Include:
- **What**: Brief summary of changes
- **Why**: Motivation and context
- **How**: Approach taken (if non-obvious)
- **Testing**: How you verified the changes
- **Related Issues**: Links to related issues

## Review Process

- Maintainers will review PRs within a reasonable timeframe
- Reviewers may suggest changes or ask questions
- Once approved, maintainers will merge the PR
- Contributors will be acknowledged in release notes

## Recognition

All contributors will be:
- Listed in release notes
- Acknowledged in the repository
- Part of the growing DMWG community

## Questions?

If you have questions:
- Check existing issues and discussions
- Open a new issue with the "question" label
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the GNU General Public License v3.0, the same license as the project.

---

Thank you for contributing to DMWG Code Instructions! Your efforts help the entire HEP community.
