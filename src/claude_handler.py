import os
from datetime import datetime
from typing import Dict, List

from anthropic import Anthropic


class ClaudeHandler:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.debug_dir = "debug_logs"
        os.makedirs(self.debug_dir, exist_ok=True)

    def read_file_content(self, file_paths: List[str]) -> List[Dict[str, str]]:
        """Read content from multiple files"""
        file_contents = []
        for file_path in file_paths:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    file_contents.append(
                        {"file_name": os.path.basename(file_path), "content": content}
                    )
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        return file_contents

    def create_initial_prompt(self, file_contents: List[Dict[str, str]]) -> str:
        """Create initial prompt with file contents"""
        prompt = "I have the following files:\n\n"
        for file_data in file_contents:
            prompt += f"File: {file_data['file_name']}\n"
            prompt += "```\n"
            prompt += file_data["content"]
            prompt += "\n```\n\n"
        prompt += "Please analyze these files and write E2E tests for the code in Jest. Always return the code without any additional text or statements. This is required to run code directly."
        return prompt

    def save_debug_output(self, prompt: str, response: str) -> str:
        """Save debugging output to a file"""
        debug_file = f"{self.debug_dir}/claude_debug.txt"
        with open(debug_file, "w", encoding="utf-8") as f:
            f.write(str(response))
        return debug_file

    def process_files(self, file_paths: List[str]) -> Dict:
        """Process files with Claude"""
        try:
            # Read file contents
            file_contents = self.read_file_content(file_paths)

            # Create initial prompt
            prompt = self.create_initial_prompt(file_contents)

            # Get response from Claude
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            )

            msg = message.content[0]
            msg_text = msg.text
            # Save debug output
            debug_file = self.save_debug_output(prompt, msg_text)

            return {
                "status": "success",
                "response": message.content,
                "debug_file": debug_file,
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}
